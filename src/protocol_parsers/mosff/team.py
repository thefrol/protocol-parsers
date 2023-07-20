import re
from functools import cached_property, cache

from .player import Player
from ..decorators import trim


class Team: #TODO rename to player list later
    "a class for holding team html_data and parsing it"

    def __init__(self, players:list[Player], name):
        self.players=players
        self.name=name
    
      
    @cached_property
    def goal_events(self):
        for player in self.players:
            for event in player.events:
                if event.is_goal:
                    yield event
    
    @cached_property
    def autogoal_events(self):
        for player in self.players:
            for event in player.events:
                if event.is_autogoal:
                    yield event
    
 

    @cache
    def find_player_by_name(self, first_name:str,last_name:str):
        '''finds first player with specified name or None'''
        for player in self.players:
            if player.name.first_name == first_name and player.name.last_name==last_name:
                return player
        return None
