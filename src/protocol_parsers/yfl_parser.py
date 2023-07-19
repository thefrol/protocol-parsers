from datetime import datetime

from .webparser import WebParser
from .yfl import MatchPage,Team
from .date import format_season




class YflParser(WebParser):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://yflrussia.ru/match/\d+'
    page_class=MatchPage
    def _format_team(self, team:Team):
            result=[]
            for player in team.players:
                try:
                    new_player_dict={}

                    new_player_dict['name']=player.name
                    new_player_dict['image']=None
                    new_player_dict['id']=player.id
                    new_player_dict['number']=player.number

                    new_player_dict['yellow_cards']=player.events.yellow_cards
                    new_player_dict['red_cards']=player.events.red_cards if player.events.yellow_cards<2 else 0
                    new_player_dict['goals']=player.goals
                    new_player_dict['autogoals']=player.events.autogoals
                    new_player_dict['goals_missed']=player.missed_goals
                    new_player_dict['is_capitain']=player.is_capitain
                    new_player_dict['is_goalkeeper']=player.is_goalkeeper

                    new_player_dict['time_played']=player.time_on_field

                    new_player_dict['time_in']=player.time_in
                    new_player_dict['time_out']=player.time_out

                    #substitutions
                    sub_in_event=player.sub_in_event
                    sub_from= team._parent_match.find_player_by_id(player.sub_from_id)
                    if sub_from is not None:
                        new_player_dict['sub_from']={
                            'id':sub_from.id,
                            'number':sub_from.number,
                            'minute':sub_in_event.minute
                        }
                    else:
                        new_player_dict['sub_from']=None

                    sub_out_event= player.sub_out_event
                    sub_to= team._parent_match.find_player_by_id(player.sub_to_id)
                    if sub_to is not None:
                        new_player_dict['sub_to']={
                            'id':sub_to.id,
                            'number':sub_to.number,
                            'minute':sub_out_event.minute
                        }
                    else:
                        new_player_dict['sub_to']=None



                    #relative time
                    # if >0 not connected with total time
                    # <0 can be computed by adding match_time
                    # played_time= relative_played_time + match_time
                    #TODO

                    if player.time_in is None:
                        #not played
                        new_player_dict['relative_time_played']=None
                        #new_player_dict['relative_time_in']=None
                        new_player_dict['relative_time_out']=None
                    else:
                        if player.played_till_end:
                            #played till end
                            new_player_dict['relative_time_played']=-player.time_in
                            #new_player_dict['relative_time_in']=player.in_at if player.in_at>0 elsew
                            new_player_dict['relative_time_out']=0
                        else:
                            #player subtituted or banned
                            new_player_dict['relative_time_played']=player.time_out-player.time_in ##TODO TESTS
                            #new_player_dict['relative_time_in']=player.in_at
                            new_player_dict['relative_time_out']=player.time_out

                    
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
                        print(f'parsing players in team {team.name} failed, player {player}: {e}')
            return result
    
    def format_date(self):
        date_=self.page.promo.date
        #year=match.tournament_year
        year=datetime.now().year #TODO get match year not current
        if all([date_.day,date_.month,year]):
            match_date_time=datetime(day=date_.day,month=date_.month,year=year,hour=date_.hour,minute=date_.minute)
        else:
            print('cant get match date')
            match_date_time=None

        return {
            'iso_string':str(match_date_time) if match_date_time is not None else None,
            'day':date_.day,
            'month':date_.month,
            'year':year,
            'hour':date_.hour,
            'minute':date_.minute
        }
    
   

    def to_rbdata(self):
        result=dict()
        self.page:MatchPage=self.page

        result['tournament_name']=self.page.promo.tournament.name.replace("-","")
        result['tournament_round']=None #TODO
        result['tournament_id']=self.page.promo.tournament.id
        result['tournament_season']=format_season(self.page.promo.date.as_datetime) #TODO if month>june season=current_year/next_year

        result['home_team_name']=f'{self.page.home_team.name} {self.page.promo.tournament.name.replace("-","")}'
        result['home_team_score']=self.page.promo.home_score
        result['home_team_id']=self.page.promo.home_team.id

        result['guest_team_name']=f'{self.page.guest_team.name} {self.page.promo.tournament.name.replace("-","")}'
        result['guest_team_score']=self.page.promo.guest_score
        result['guest_team_id']=self.page.promo.guest_team.id

        result['score']=self.page.promo.score_raw_text

        result['time_played']=self.page.time_played

        result['home_team_players']=self._format_team(self.page.home_team)
        result['guest_team_players']=self._format_team(self.page.guest_team)

        result['date']=self.format_date()

        return result







