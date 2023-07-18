from typing import Callable
from functools import cached_property,cache
import datetime


from protocol_parsers.date import PageDate
from ..decorators import trim, to_int, to_int_or_none
import re
from ..regex import Regex, Regexes2

from ..tagminer import TagMiner
import protocol_parsers.yfl as yfl
import protocol_parsers.yfl.match as match
from .player import MatchProtocolTabPlayer
from .funcs import get_player_id
from protocol_parsers.yfl.events_list import Event, EventsList




class Team:
    """A class for working with protocol tab player names and others
    location may be left or right
    left team is the home team, rigth is guest team"""
    def __init__(self, html, location:str,parent_match:'match.MatchPage'):
        self._html=html
        self._location=location
        self._parent_match=parent_match
    @cached_property
    def name(self):
        """returns left or right team name"""
        return self._html.find('a',{'class':f'match-protocol__team-name--{self._location}'})['title'] #TODO failures#
    @cached_property
    def players(self)-> list[MatchProtocolTabPlayer]:
        result=[]
        tags=self._html.find_all('li',{'class':f'match-protocol__member--{self._location}'}) #TODO failures#
        for tag in tags:
            new_player=MatchProtocolTabPlayer(tag)
            new_player.events=self._parent_match.events.get_by_player_id(new_player.id)
            new_player.team=self
            result.append(new_player)
        return result
    
    def find_by_name(self, name):
        """returns a first player with a specified name,
        searches part of name as well
        case unsensitive
        маЛютин -> Стас малютин"""
        if name is None:
            print(f'trying to search None name in team {self.name}, return None')
            return None
        name=name.lower()
        for player in self.players:
            player_name=player.name
            if player_name is None: 
                continue
            player_name=player_name.lower()
            if name in player_name:
                return player
    
    @property
    def opposing_team(self):
        if self is self._parent_match.home_team:
            return self._parent_match.guest_team
        else:
            return self._parent_match.home_team
        
    @cached_property
    def events(self)->'EventsList':
        array=sum([player.events for player in self.players],start=EventsList())
        unique=set(array)
        return EventsList(unique)
