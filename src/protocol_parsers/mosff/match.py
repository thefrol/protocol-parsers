from bs4 import BeautifulSoup
import re

from .team import Team
from ..decorators import trim

class Match:
    """
    A class for interacting with html data
    its like a data object, gets a raw hml
    has properties and functions to return
    players, match data, score and others
    """
    home_team_main_players_div_index=0
    home_team_reserve_players_div_index=2
    home_team_trainers_div_index=4

    guest_team_main_players_div_index=1
    guest_team_reserve_players_div_index=3
    guest_team_trainers_div_index=5

    round_pattern=r'(?P<round_number>\d)+ тур'
    team_year_pattern=r'(?P<team_year>\d+) +г.р.'
    tournament_year_pattern=r'\(.*(?P<tournament_year>\d{4})\)'


    def __init__(self, html_text, parser='html.parser'):
        _soup= BeautifulSoup(html_text,parser)
        
        self.divs_with_names=_soup.find_all("div", {"class":"structure__top-name"})[:2]
        self.div_with_score=_soup.find("div", {"class":"match__score-main"})
        self.a_with_round=_soup.find("a", {"class":"match__round"})
        self.a_with_tournament=_soup.find("a", {"class":"match__tournament"})

        protocol_tab=_soup.find('div',id="match-tabs-protocol")
        self.divs_with_players=protocol_tab.find_all("div", {"class": "structure__unit"})
        

    @property
    def team_names(self) -> list[str]:
        "returns team names of given match"
        return [name.string for name in self.divs_with_names]
    
    @property
    def home_team_name(self) -> str:
        'returns home team name, parses whole html every call'
        return self.team_names[0]

    @property
    def guest_team_name(self) -> str:
        'returns guest team name, parses whole html every call'
        return self.team_names[1]
    

                    
    @property
    def home_team(self):
        """retrieves html data for team
        in former html teams are separated in three blocks
        main, reverse, and trainers
        home and guest team lies in one div, so we need to separate then and 
        collect data per team in this function"""
        home_team=Team(
            main_team_html=self.divs_with_players[self.home_team_main_players_div_index],
            reserve_team_html=self.divs_with_players[self.home_team_reserve_players_div_index],
            trainers_html=self.divs_with_players[self.home_team_trainers_div_index],
            name=self.home_team_name)
        
        return home_team
    
    @property
    def guest_team(self):
        """retrieves html data for team
        in former html teams are separated in three blocks
        main, reverse, and trainers
        home and guest team lies in one div, so we need to separate then and 
        collect data per team in this function"""
        guest_team=Team(
            main_team_html=self.divs_with_players[self.guest_team_main_players_div_index],
            reserve_team_html=self.divs_with_players[self.guest_team_reserve_players_div_index],
            trainers_html=self.divs_with_players[self.guest_team_trainers_div_index],
            name=self.guest_team_name)
        return guest_team
    
    @property
    def scores(self):
        try:
            scores=[int(score.strip()) for score in self.div_with_score.text.split(':')]
            return scores
        except Exception as e:
            print(f'cant get score {e}')
            return [0,0]

        
    @property
    def home_score(self):
        return self.scores[0]
    
    @property
    def guest_score(self):
        return self.scores[1]
    
    @property
    def round(self):
        """Return round number from the tournament
        6 тур - returns 6"""
        m=re.search(self.round_pattern, self.a_with_round.text)
        if m:
            return m.group('round_number')
        else:
            return None
        
    @property
    @trim
    def tournament(self):
        return self.a_with_tournament.text
    
    @property
    def tournament_year(self) -> int:
        """year when tournament hosted ex. 2023, 2024"""
        m=re.search(self.tournament_year_pattern,self.tournament)
        if m is None:
            print('cant find tournament year')
            return None
        else:
            try:
                return int(m.group('tournament_year'))
            except Exception as e:
                print(f'cant convert tournament year to int:{e}')
                return None

    @property
    def team_year(self) ->int:
        """year of born players ex. 2013, 2014"""
        m=re.search(self.team_year_pattern,self.tournament)
        if m is None:
            print('cant find team year')
            return None
        else:
            try:
                return int(m.group('team_year'))
            except Exception as e:
                print(f'cant convert team year to int:{e}')
                return None

