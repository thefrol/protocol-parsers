import re
import requests
from .mosff import Match
from .rbdata import RbdataTounament



class MosffParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    def __init__(self, url:str):
        if not re.fullmatch(self.url_pattern,url):
            print(f'seems like {url} is not from mosff')
        
        page=requests.get(url) 

        if page.status_code != 200:
            raise ConnectionError('page not retrieved')
        
        self._match=Match(page.text)

    def to_rbdata(self, match_time):
        result=dict()

        result['tournament_name']=RbdataTounament(
            team_year=self._match.team_year,
            tournament_year=self._match.tournament_year).rbdata_name
                
        result['tournament_round']=self._match.round

        result['home_team_name']=self._match.home_team_name
        result['home_team_score']=self._match.home_score

        result['guest_team_name']=self._match.guest_team_name
        result['guest_team_score']=self._match.guest_score

        result['home_team_players']=home_team_players=[]

        result['time_played']=match_time

        for player in self._match.home_team.players:
            new_player_dict={}

            new_player_dict['name']=player.name #TODO first and second name
            new_player_dict['image']=player.img_url
            new_player_dict['yellow_cards']=player.yellow_cards
            new_player_dict['red_cards']=player.red_cards
            new_player_dict['time_played']=player.time_played(match_time)
            new_player_dict['goals']=player.goals
            new_player_dict['autogoals']=player.autogoals
            new_player_dict['goals_missed']=0 # TODO
            new_player_dict['is_capitain']=player.is_capitain
            new_player_dict['is_goalkeeper']=player.is_goalkeeper

            if player.is_goalkeeper: # count goals
                goals_missed=0
                for goal in self._match.guest_team.goal_events:
                    if player.was_on_field(goal.minute):
                        goals_missed=goals_missed+1
                new_player_dict['goals_missed']=goals_missed

            home_team_players.append(new_player_dict)

        result['guest_team_players']=guest_team_players=[]

        for player in self._match.guest_team.players:
            new_player_dict={}

            new_player_dict['name']=player.name #TODO first and second name
            new_player_dict['image']=player.img_url
            new_player_dict['yellow_cards']=player.yellow_cards
            new_player_dict['red_cards']=player.red_cards
            new_player_dict['time_played']=player.time_played(match_time)
            new_player_dict['goals']=player.goals
            new_player_dict['autogoals']=player.autogoals
            new_player_dict['goals_missed']=0 # TODO
            new_player_dict['is_capitain']=player.is_capitain
            new_player_dict['is_goalkeeper']=player.is_goalkeeper

            if player.is_goalkeeper: # count goals
                goals_missed=0
                for goal in self._match.home_team.goal_events:
                    if player.was_on_field(goal.minute):
                        goals_missed=goals_missed+1
                new_player_dict['goals_missed']=goals_missed
            
            guest_team_players.append(new_player_dict)

        return result




