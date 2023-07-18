import re
import requests
import json
from itertools import chain
from datetime import datetime


from .mosff import Match, Team, Player
from .rbdata import RbdataTounament
from .exceptions import TeamNotFound

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


        


    

class MosffParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    def __init__(self, url:str, html_text=None, match_time=None):
        if all([url, html_text]):
            print(f'specified url and html_text in parser. url will be ignored')
        if html_text is None:
            if not re.fullmatch(self.url_pattern,url):
                print(f'seems like {url} is not from mosff')
            
            page=requests.get(url) 

            if page.status_code != 200:
                raise ConnectionError('page not retrieved')
            html_text=page.text
        
        self._match=Match(html_text)

        self.tournament=RbdataTounament(
            team_year=self._match.team_year,
            tournament_year=self._match.tournament_year)
        
        self.match_time=match_time
        if self.match_time is None:
            self.match_time=self.tournament.match_time # if not match time specified try to get match time from tournament data

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
                    opposing_team=self._match.get_opposing_team(team)
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
        result['tournament_round']=self._match.round
        result['tournament_id']=self._match.tournament_id

        result['home_team_name']=format_team_name(self._match.home_team)
        result['home_team_score']=self._match.home_score
        result['home_team_id']=self._match.home_team_id

        result['guest_team_name']=format_team_name(self._match.guest_team)
        result['guest_team_score']=self._match.guest_score
        result['guest_team_id']=self._match.guest_team_id

        result['score']=f'{self._match.home_score}:{self._match.guest_score}'

        result['time_played']=self.match_time

        result['home_team_players']=self._format_team(self._match.home_team)
        result['guest_team_players']=self._format_team(self._match.guest_team)

        result['date']=format_date(self._match)

        return result
    
    def to_json(self)->str:
        '''returns a json string formatted in style of rbdata'''
        return json.dumps(self.to_rbdata(),ensure_ascii=False)




