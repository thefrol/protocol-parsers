"""
need to know
names like a, div, li, ul represents a html tag and its info within python code

self.divs_with_names implies a collection of div tags, that stored names
"""


import re
from datetime import datetime
from functools import cached_property, cache

from protocol_parsers.mosff.promo import Promo


from .team import Team
from .player_block import PlayerBlock,PlayerBlockList
from ..date import PageDate
from ..tagminer import TagMiner
from .tournament import Tournament


        
class MatchPageDate(PageDate):
    @property
    def _date_pattern(self):
        return r'(?P<day>\d+) (?P<month>\w+) / (?P<week_day>\w+)( / (?P<hour>\d+):(?P<minute>\d+))?'
    

    

class Match(TagMiner): #TODO extract a promo block
    """
    A class for interacting with html data
    its like a data object, gets a raw hml
    has properties and functions to return
    players, match data, score and others
    """

    @cached_property
    def promo(self):
        return Promo(self._find_tag('section',class_='match'))
    
    @cached_property
    def player_blocks(self):
        block_tags=self._find_all_tags(class_='structure__unit')
        return PlayerBlockList([PlayerBlock(block) for block in block_tags])

 
    @cached_property
    def home_team(self):
        return Team(self.player_blocks.home_players)
    
    @cached_property
    def guest_team(self):
        return Team(self.player_blocks.guest_players)
    
    @property
    def teams(self):
        'returns a list of Team objects: home+guest team'
        return [self.home_team, self.guest_team]
    
    @cache
    def get_opposing_team(self, for_team:Team):
        'returns opposing team of for_team'
        for team in self.teams:
            if team is not for_team:
                return team
        print('cant find opposing team')
        return None

    @property
    def date(self):
        date_text=self._find_tag(class_='match__date').text
        return MatchPageDate(date_text)
    

    

    @cached_property
    def tournament(self):
        return Tournament(self._find_tag(class_='match__container'))


        
    def find_by_name(self, first_name, last_name):
        '''finds first player by name
        searches home team first'''
        return self.home_team.find_player_by_name(first_name,last_name) or self.guest_team.find_player_by_name(first_name,last_name)


