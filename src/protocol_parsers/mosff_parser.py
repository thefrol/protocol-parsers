import re
import requests
import json
from itertools import chain
from datetime import datetime
from functools import cached_property

from bs4 import BeautifulSoup

from .mosff import Match, Team, Player
from .rbdata import RbdataTounament
from .exceptions import TeamNotFound
from .webparser import WebParser

def format_team_name(team:Team):
    if team.team_year is None:
        return team.name_without_year
    else:
        return f'{team.name_without_year} {team.team_year}'
    
def format_player_name(player:Player):
    if player.name.first_name is not None:
        return f'{player.name.first_name} {player.name.last_name}'
    else:
        return player.name.last_name
    
def format_date(match:Match):
    date_=match.date
    year=match.tournament_year
    if year is None:
        print('cant get year from tournamet, returning current year')
        return datetime.now().year
    if all([date_.day,date_.month,year]):
        match_date_time=datetime(day=date_.day,month=date_.month,year=year,hour=date_.hour,minute=date_.minute)
    else:
        print('cant get match date')
        match_date_time=None

    return {
        'iso_string':str(match_date_time),
        'day':date_.day,
        'month':date_.month,
        'year':year,
        'hour':date_.hour,
        'minute':date_.minute
    }


        


    

class MosffParser(WebParser[Match]):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    _match_time=None

    @property
    def match_time(self):
        if self._match_time is None:
            return self.tournament.match_time
        else:
            return self._match_time
    
    @match_time.setter
    def match_time(self,value):
        if value<=0:
            print(f'match time must be >0, attemping to set {value}.Ignoring')
            return
        self._match_time=value

    @cached_property
    def tournament(self):
        return RbdataTounament(
            team_year=self.page.team_year,
            tournament_year=self.page.tournament_year)

    def _format_team(self, team:Team):
        try:
            result=[]
            for player in team.players:
                new_player_dict={}

                new_player_dict['name']=format_player_name(player)
                new_player_dict['image']=player.img_url
                new_player_dict['id']=player.id
                new_player_dict['number']=player.number

                new_player_dict['yellow_cards']=player.yellow_cards
                new_player_dict['red_cards']=player.red_cards
                new_player_dict['goals']=player.goals
                new_player_dict['autogoals']=player.autogoals
                new_player_dict['goals_missed']=0 # TODO
                new_player_dict['is_capitain']=player.is_capitain
                new_player_dict['is_goalkeeper']=player.is_goalkeeper

                new_player_dict['time_played']=player.time_played(self.match_time)

                if player.in_at is None:
                    #player never played
                    new_player_dict['time_in']=None
                    new_player_dict['time_out']=None
                else:
                    #player played
                    new_player_dict['time_in']=player.in_at
                    new_player_dict['time_out']=player.out_at if player.out_at is not None else self.match_time

                if player.is_goalkeeper: # count goals #TODO transfer to player class with parents to team and match
                    goals_missed=0
                    opposing_team=self.page.get_opposing_team(team)
                    for goal in chain(opposing_team.goal_events, team.autogoal_events):  # goals from opposing team + autogoals current team
                        if player.was_on_field(goal.minute):
                            goals_missed=goals_missed+1
                    new_player_dict['goals_missed']=goals_missed

                #relative time
                # if >0 not connected with total time
                # <0 can be computed by adding match_time
                # played_time= relative_played_time + match_time

                if player.in_at is None:
                    #not played
                    new_player_dict['relative_time_played']=None
                    #new_player_dict['relative_time_in']=None
                    new_player_dict['relative_time_out']=None
                else:
                    if player.out_at is None:
                        #played till end
                        new_player_dict['relative_time_played']=-player.in_at
                        #new_player_dict['relative_time_in']=player.in_at if player.in_at>0 elsew
                        new_player_dict['relative_time_out']=0
                    else:
                        #player subtituted or banned
                        new_player_dict['relative_time_played']=player.out_at-player.in_at
                        #new_player_dict['relative_time_in']=player.in_at
                        new_player_dict['relative_time_out']=player.out_at
                
                #events
                new_player_dict['events']=events=[]
                for event in player.events:
                    new_event_dict={
                        'time':event.minute,
                        'type':event.type_
                    }
                    events.append(new_event_dict)

                #subtitutions #TODO
                new_player_dict['sub_from']=None
                new_player_dict['sub_to']=None

                result.append(new_player_dict)
            return result
        except TeamNotFound:
            return []


    def to_rbdata(self):
        result=dict()

        result['tournament_name']=self.tournament.rbdata_name
        result['tournament_round']=self.page.round
        result['tournament_round_id']=None #TODO?
        result['tournament_round_url']=None
        result['tournament_id']=self.page.tournament_id

        result['home_team_name']=format_team_name(self.page.home_team)
        result['home_team_score']=self.page.promo.score.home
        result['home_team_id']=self.page.home_team_id

        result['guest_team_name']=format_team_name(self.page.guest_team)
        result['guest_team_score']=self.page.promo.score.guest
        result['guest_team_id']=self.page.guest_team_id

        result['score']=self.page.promo.score.text

        result['time_played']=self.match_time

        result['home_team_players']=self._format_team(self.page.home_team)
        result['guest_team_players']=self._format_team(self.page.guest_team)

        result['date']=format_date(self.page)

        return result
    
    def to_json(self)->str:
        '''returns a json string formatted in style of rbdata'''
        return json.dumps(self.to_rbdata(),ensure_ascii=False)




