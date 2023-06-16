"""
need to know
names like a, div, li, ul represents a html tag and its info within python code

self.divs_with_names implies a collection of div tags, that stored names
"""

from bs4 import BeautifulSoup
import re
from datetime import datetime
from functools import cached_property, cache

from .team import Team
from .date import PageDate
from ..decorators import trim, to_int
from ..exceptions import TeamNotFound
        
class MatchPageDate(PageDate):
    @property
    def _date_pattern(self):
        return r'(?P<day>\d+) (?P<month>\w+) / (?P<week_day>\w+) / (?P<hour>\d+):(?P<minute>\d+)'
    

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
    _team_id_pattern=r'/team/(?P<team_id>\d+)\Z'
    _tournament_id_pattern=r'/tournament/(?P<tournament_id>\d+)\Z'


    def __init__(self, html_text, parser='html.parser'):
        _soup= BeautifulSoup(html_text,parser)
        
        self.divs_with_names=_soup.find_all("div", {"class":"structure__top-name"})[:2]
        self.a_with_urls=_soup.find_all("a", {"class":"match__team"})[:2]
        self.div_with_score=_soup.find("div", {"class":"match__score-main"})
        self.a_with_round=_soup.find("a", {"class":"match__round"})
        self.a_with_tournament=_soup.find("a", {"class":"match__tournament"})
        self.div_with_date=_soup.find("div", {"class":"match__date"})

        protocol_tab=_soup.find('div',id="match-tabs-protocol")
        self.divs_with_players=protocol_tab.find_all("div", {"class": "structure__unit"})

        #lazy init of home team. !important we need to get the same object every time for comparison in match.opposing_team()
        self._home_team=None
        self._guest_team=None
        

    @property
    def team_names(self) -> list[str]:
        "returns team names of given match"
        if len(self.divs_with_names)<2:
            print('error parsing team names')
            return [None, None]
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
    def team_relative_urls(self) -> list[str]:
        "returns team urls of given match"
        if len(self.a_with_urls)<2:
            print('error parsing team names')
            return [None, None]
        return [a['href'] for a in self.a_with_urls]
    
    @property
    def home_team_relative_url(self):
        return self.team_relative_urls[0]
    
    @property
    def guest_team_relative_url(self):
        return self.team_relative_urls[1]
    
    @property
    def home_team_id(self):
        m=re.fullmatch(self._team_id_pattern,self.home_team_relative_url)
        if m:
            return int(m.group('team_id'))
        else:
            print('cant parse home team id')
            return None
        
    @property
    def guest_team_id(self):
        m=re.fullmatch(self._team_id_pattern,self.guest_team_relative_url)
        if m:
            return int(m.group('team_id'))
        else:
            print('cant parse guest team id')
            return None
                    
    @property
    def home_team(self):
        """retrieves html data for team
        in former html teams are separated in three blocks
        main, reverse, and trainers
        home and guest team lies in one div, so we need to separate then and 
        collect data per team in this function"""
        try:
            if not self._home_team:
                self._home_team=Team(
                    main_team_html=self.divs_with_players[self.home_team_main_players_div_index],
                    reserve_team_html=self.divs_with_players[self.home_team_reserve_players_div_index],
                    trainers_html=self.divs_with_players[self.home_team_trainers_div_index],
                    name=self.home_team_name)
            
            return self._home_team
        except Exception as e:
            print('no home team')
            raise TeamNotFound()
    
    @property
    def guest_team(self):
        """retrieves html data for team
        in former html teams are separated in three blocks
        main, reverse, and trainers
        home and guest team lies in one div, so we need to separate then and 
        collect data per team in this function"""
        try:
            if not self._guest_team:
                self._guest_team=Team(
                    main_team_html=self.divs_with_players[self.guest_team_main_players_div_index],
                    reserve_team_html=self.divs_with_players[self.guest_team_reserve_players_div_index],
                    trainers_html=self.divs_with_players[self.guest_team_trainers_div_index],
                    name=self.guest_team_name)
            return self._guest_team
        except Exception as e:
            print('no guest team')
            raise TeamNotFound()
    
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
    def date(self):
        return MatchPageDate(self.div_with_date.text)
    
    @property
    def round(self):
        """Return round number from the tournament
        6 тур - returns 6
        
        1/8 кубка - 1/8"""
        if self.tournament_is_cup:
            return '1/8'
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
    def tournament_relative_url(self):
        return self.a_with_tournament['href']
    
    @property
    def tournament_url(self):
        return 'https://mosff.ru'+self.tournament_relative_url
    
    @property
    def tournament_id(self):
        m=re.fullmatch(self._tournament_id_pattern,self.tournament_relative_url)
        if m:
            return int(m.group('tournament_id'))
        else:
            print('cant parse tournament id')
            return None
        
    @property
    def tournament_is_cup(self):
        '''returns True if match played in cup'''
        return 'кубок' in self.tournament.lower()
        
    @property
    def tournament_year(self) -> int:
        """year when tournament hosted ex. 2023, 2024"""
        m=re.search(self.tournament_year_pattern,self.tournament)
        if m is None:
            print('cant find tournament year, falling back to current year')
            return datetime.now().year
        else:
            try:
                return int(m.group('tournament_year'))
            except Exception as e:
                print(f'cant convert tournament year to int:{e}, returning current year')
                return datetime.now().year

    @cached_property
    @to_int
    def team_year(self) ->int:
        """year of born players ex. 2013, 2014"""
        m=re.search(self.team_year_pattern,self.tournament)
        if m is None:
            print('cant find team year, falling back to year of teams')
            if self.home_team.team_year or self.guest_team_year:
                return self.home_team.team_year or self.guest_team_year
            else:
                print('year in teams cant be found')
                return None
        else:
            try:
                return int(m.group('team_year'))
            except Exception as e:
                print(f'cant convert team year to int:{e}')
                return None
        
    def find_by_name(self, first_name, last_name):
        '''finds first player by name
        searches home team first'''
        return self.home_team.find_player_by_name(first_name,last_name) or self.guest_team.find_player_by_name(first_name,last_name)


