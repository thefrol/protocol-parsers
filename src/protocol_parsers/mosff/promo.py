"""represents a promo block in protocol
<section class="match">

here scores, team names team ids"""
from functools import cached_property
from ..tagminer import TagMiner
from ..decorators import to_int,to_int_or_none,remove_spaces,trim, trim_or_none
from ..regex import Regex
from .team_stub import MosffTeam

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

class PromoTeam(MosffTeam):
    @cached_property
    @trim
    def raw_name(self):
        return self._find_tag(class_='match__title').text
    
    @cached_property
    def relative_url(self):
        return self.href
    
    @cached_property
    def image_url(self):
        return self._find_tag(class_='match__img').get_param('src')

class Promo(TagMiner):
    @cached_property
    def score(self):
        return PromoScore(self._find_tag(class_='match__score-main'))
    
    @cached_property
    def home_team(self):
        return PromoTeam(self._find_tag(class_='match__team'))
    
    @cached_property
    def guest_team(self):
        return PromoTeam(self._find_tag(class_='match__team match__team--right'))


