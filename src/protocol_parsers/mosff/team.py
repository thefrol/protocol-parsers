import re
from functools import cached_property, cache

from .player import Player
from ..decorators import trim


class Team:
    "a class for holding team html_data and parsing it"

    _team_name_pattern=r'(?P<team_name>.*) (?P<team_year>\d{4,20}) г.р.'

    def __init__(self, main_team_html, reserve_team_html, trainers_html, name):
        self._main_team_html=main_team_html
        self._reserve_team_html=reserve_team_html
        self._trainers_html=trainers_html
        self.name=name
    
    @cached_property
    def players(self) -> list[Player]:
        players=[]
        main_player_htmls=self._main_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=True) for html in main_player_htmls])
        reserve_player_htmls=self._reserve_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=False) for html in reserve_player_htmls])
        return players
        
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
    
    @cached_property
    @trim
    def name_without_year(self):
        'returns team name without year'
        m=re.fullmatch(self._team_name_pattern, self.name)
        if m:
            return m.group('team_name')
        else:
            print('cant resolve team name with year. returning full name')
            return self.name

        
    @cached_property
    def team_year(self):
        'returns team year of birth'
        m=re.fullmatch(self._team_name_pattern, self.name)
        if m:
            return m.group('team_year')
        else:
            print('cant resolve team year. returning None')
            return None     

    @cache
    def find_player_by_name(self, first_name:str,last_name:str):
        '''finds first player with specified name or None'''
        for player in self.players:
            if player.name.first_name == first_name and player.name.last_name==last_name:
                return player
        return None
