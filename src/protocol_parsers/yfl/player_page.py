import re
from functools import cached_property

from ..tagminer import TagMiner
from ..regex import Regex
from ..names import FioName
from ..date import PageDate
from ..decorators import trim,to_int, trim_or_none

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
        league_name=self.__name_regex.get_group('league_name')
        if league_name is not None:
            return league_name.replace('-','')
        else:
            return None #TODO neeed new logic
    @property
    @trim_or_none
    def name(self):
        return self.__name_regex.get_group('team_name')
    

class PlayerPage(TagMiner):
    @cached_property
    @trim
    def name_raw(self):
        return self._find_tag(class_='player-promo__name-main').text
    @cached_property
    def name(self):
        return FioName(self.name_raw)
    @cached_property
    def date_raw(self):
        html=self._find_tag('li','player-promo__item--birth')
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
        tag=self._find_tag('tr',class_='table__team-total')
        if tag is None and 'Биджилов' in self.name_raw:
            class Object(object):
                pass
            ret=Object()
            ret.relative_url='/team/1084185'
            ret.team_id=1084185
            ret.name='ЦСКА ЮФЛ1'
            ret.league_name='ЮФЛ1'
            ret.name_raw='ЦСКА (ЮФЛ-1)'
            return ret # a empty blob if no team found for player #TODO           
        if tag is None:
            class Object(object):
                pass
            ret=Object()
            ret.relative_url=None
            ret.team_id=None
            ret.name=None
            ret.league_name=None
            ret.name_raw=None
            return ret # a empty blob if no team found for player #TODO
        return YflPlayerPageTeam(self._find_tag('tr',class_='table__team-total'))
    
    @cached_property
    def image_url(self):
        return self._find_tag(class_='player-promo__img').get_param('src')
    