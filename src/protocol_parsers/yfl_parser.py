import re
import requests
import json
from itertools import chain
from datetime import datetime
from bs4 import BeautifulSoup
from abc import abstractmethod


from .yfl import MatchPage,Team


class WebParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    page_class=None
    def __init__(self, url:str):
        if not re.fullmatch(self.url_pattern,url):
            print(f'seems like {url} not fits url pattern{self.url_pattern}')
        
        page=requests.get(url) 

        if page.status_code != 200:
            raise ConnectionError('page not retrieved')
        
        self._html=BeautifulSoup(page.text, 'html.parser')
        self.page=self.page_class(self._html)
    
    @abstractmethod
    def to_rbdata(self):
        pass
    
    def to_json(self)->str:
        '''returns a json string formatted in style of rbdata'''
        return json.dumps(self.to_rbdata(),ensure_ascii=False)


class YflParser(WebParser):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://yflrussia.ru/match/\d+'
    page_class=MatchPage
    def _format_team(self, team:Team):
        try:
            result=[]
            for player in team.players:
                new_player_dict={}

                new_player_dict['name']=player.name
                new_player_dict['image']=None
                new_player_dict['id']=player.id
                new_player_dict['number']=player.number

                new_player_dict['yellow_cards']=player.events.yellow_cards
                new_player_dict['red_cards']=player.events.red_cards
                new_player_dict['goals']=player.goals
                new_player_dict['autogoals']=player.events.autogoals
                new_player_dict['goals_missed']=player.missed_goals
                new_player_dict['is_capitain']=player.is_capitain
                new_player_dict['is_goalkeeper']=player.is_goalkeeper

                new_player_dict['time_played']=player.time_on_field

                new_player_dict['time_in']=player.time_in
                new_player_dict['time_out']=player.time_out


                #relative time
                # if >0 not connected with total time
                # <0 can be computed by adding match_time
                # played_time= relative_played_time + match_time
                #TODO

                new_player_dict['relative_time_played']=None
                #new_player_dict['relative_time_in']=None
                new_player_dict['relative_time_out']=None

                  
                #events #TODO
                new_player_dict['events']=events=[]
                # for event in player.events:
                #     new_event_dict={
                #         'time':event.minute,
                #         'type':event.type_
                #     }
                #     events.append(new_event_dict)

                result.append(new_player_dict)

        except ValueError as e:
            print(f'parsing team {team.name} failed: {e}')
        return result
    def to_rbdata(self):
        result=dict()
        self.page:MatchPage=self.page

        result['tournament_name']=self.page.promo.tournament.name
        result['tournament_round']=None #TODO
        result['tournament_id']=self.page.promo.tournament.id

        result['home_team_name']=self.page.home_team.name
        result['home_team_score']='*********************'
        result['home_team_id']='*********************'

        result['guest_team_name']=self.page.guest_team.name
        result['guest_team_score']='************'
        result['guest_team_id']='************'

        result['score']='************'

        result['time_played']=self.page.time_played

        result['home_team_players']=self._format_team(self.page.home_team)
        result['guest_team_players']=self._format_team(self.page.guest_team)

        result['date']="*****"

        return result







