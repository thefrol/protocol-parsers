"""represents a promo block in protocol
<section class="match">

here scores, team names team ids"""
from functools import cached_property
from ..tagminer import TagMiner
from ..decorators import to_int,to_int_or_none,remove_spaces,trim, trim_or_none
from ..regex import Regex
from ..stubs import TeamStub

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

class PromoTeam(TeamStub,TagMiner):
    @cached_property
    @trim
    def name_raw(self):
        return self._find_tag(class_='match__title').text

    @cached_property
    def __regex(self):
        return Regex(
            pattern='(?P<team_name>.*) (?P<team_year>\d{4,20}) г.р.',
            string=self.name_raw
        )

    @cached_property
    @trim
    def name_without_year(self):
        'returns team name without year'
        return self.__regex.get_group('team_name')
        
    @cached_property
    def team_year(self):
        'returns team year of birth'
        return self.__regex.get_group('team_year')
    
    @cached_property
    def name(self):
        """returns name in style of rbdata"""
        if self.team_year is None or self.name_without_year is None:
            return self.name_raw
        else:
            return f'{self.name_without_year} {self.team_year}'
    
    @cached_property
    def relative_url(self):
        return self.href
    
    @cached_property
    def url(self):
        return 'https://mosff.ru'+self.relative_url
    
    @cached_property
    @to_int_or_none
    def id(self):
        return Regex(
            pattern=r'/team/(?P<team_id>\d+)',
            string=self.relative_url
        ).get_group('team_id')

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


