"""Here most shared team object, useful for many mosff parsers"""
from abc import abstractproperty
from functools import cached_property

from ..stubs import TeamStub
from ..regex import Regex
from ..decorators import trim,to_int_or_none
from ..tagminer import TagMiner


class MosffTeam(TeamStub, TagMiner):
    """Most shared functions for team naming and getting ids
    override name_raw and relative_url property in your classes"""
    raw_name=abstractproperty()
    relative_url=abstractproperty()

    @cached_property
    def __regex(self):
        return Regex(
            pattern='(?P<team_name>.*) (?P<team_year>\d{4,20}) г.р.',
            string=self.raw_name
        )

    @cached_property
    @trim
    def name_without_year(self):
        'returns team name without year'
        return self.__regex.get_group('team_name')
        
    @cached_property
    def year(self):
        'returns team year of birth'
        return self.__regex.get_group('team_year')
    
    @cached_property
    def name(self):
        """returns name in style of rbdata"""
        if self.year is None or self.name_without_year is None:
            return self.raw_name
        else:
            return f'{self.name_without_year} {self.year}'
    
   
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