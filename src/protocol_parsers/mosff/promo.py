"""represents a promo block in protocol
<section class="match">

here scores, team names team ids"""
from functools import cached_property
from ..tagminer import TagMiner
from ..decorators import to_int,remove_spaces

class PromoScore(TagMiner):
    @property
    @remove_spaces
    def text(self)->str:
        return self.tag_text()
    @property
    def _scores_list(self)->list[str]:
        return self.text.split(':')
    @property
    @to_int
    def home(self):
        return self._scores_list[0]
    @property
    @to_int
    def guest(self):
        return self._scores_list[1]
    def health_check(self):
        if ":" not in self.tag_text():
            print('score has no ":" sign')

class Promo(TagMiner):
    @cached_property
    def score(self):
        return PromoScore(self._find_tag(class_='match__score-main'))


