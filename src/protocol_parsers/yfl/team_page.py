from functools import cached_property

from ..tagminer import TagMiner
from ..regex import Regex
from ..decorators import trim,to_int, trim_or_none

class TeamPage(TagMiner):
    """A class for working with team page /team/123123"""
    #mostly identical with PlayerPageTeam class, if we  define tag classed to mine data
    @cached_property
    def name_tag(self):
        return self._find_tag('a',class_='team-promo__team-name')
    @property
    @trim_or_none
    def name_raw(self):
        if self.name_tag is not None:
            return self.name_tag.text
        else:
            raise ValueError('Cant fing name tag on the page')
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
    @cached_property
    def img(self):
        return self._find_tag('img',class_='team-promo__img')['src']
    @cached_property
    def relative_url(self):
        if self.name_tag is not None:
            return self.name_tag['href']
        else:
            raise ValueError('Cant fing name tag on the page')        
    @cached_property
    @to_int
    def team_id(self):
        _pattern=r'/team/(?P<team_id>\d+)'
        return Regex(pattern=_pattern,string=self.relative_url).get_group('team_id')
