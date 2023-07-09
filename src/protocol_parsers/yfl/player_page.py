import re
from functools import cached_property

from ..tagminer import TagMiner
from ..regex import Regex
from ..names import FioName
from ..date import PageDate
from ..decorators import trim,to_int

class YflPlayerDate(PageDate):
    _date_pattern=r'(?P<date_string>(?P<day>\d+) (?P<month>\w+) (?P<year>\d+))'

    @property
    def is_healthy(self):
        return self.day is not None and self.month is not None and self.year is not None
    
class YflPlayerPageTeam(TagMiner):
    @cached_property
    def relative_url(self):
        return self._find_tag('a',class_='table__team')['href']
    @property
    @to_int
    def team_id(self):
        _pattern=r'/team/(?P<team_id>\d+)'
        return Regex(pattern=_pattern,string=self.relative_url).get_group('team_id')
    @cached_property
    @trim
    def name_raw(self):
        return self._find_tag(None,'table__team-name').text
    @cached_property
    def __name_regex(self):
        _pattern=r'(?P<team_name>.+)\((?P<league_name>.+)\)'
        return Regex(pattern=_pattern,string=self.name_raw)
    @property
    def league_name(self):
        return self.__name_regex.get_group('league_name').replace('-','')
    @property
    @trim
    def name(self):
        return self.__name_regex.get_group('team_name')
    

class PlayerPage(TagMiner):
    @cached_property
    @trim
    def name_raw(self):
        return self._find_tag('p',class_='player-promo__name').text
    @cached_property
    def name(self):
        return FioName(self.name_raw)
    @cached_property
    def date_raw(self):
        html=self._find_tag('p','player-promo__item--birth')
        if html is None:
            print('date of birth not specified on page, returning None')
            return None
        wrapper_tag=TagMiner(html)
        value_tag=wrapper_tag._find_tag('span','player-promo__value')
        return value_tag.text
    @cached_property
    def birth_date(self):
        return YflPlayerDate(self.date_raw)
    @cached_property
    def team(self):
        return YflPlayerPageTeam(self._find_tag('tr',class_='table__team-total'))
    