from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass 

URL='https://mosff.ru/match/34549' # a good match with cards, goals, changes


page=requests.get(URL)

if page.status_code != 200:
    raise ConnectionError()

soup=BeautifulSoup(page.text,'html.parser')

@dataclass
class Player:
    """a class for parsing player data """
    def __init__(self, player_html):
        self._player_html=player_html

class Players:
    """a class for interacting with players data in html,
    receives player specific html and returns names, 
    minutes played and others

    is_main - a boolean property defines if theese players are in main team,
    playing from the start
    """

    def __init__(self, team_html, is_main=True):
        self._team_html=team_html

    @property
    def players(self):
        pass

class Team:
    "a class for holding team html_data and parsing it"

    def __init__(self, main_team_html, reserve_team_html, trainers_html):
        self._main_team_html=main_team_html
        self._reserve_team_html=reserve_team_html
        self._trainers_html=trainers_html

    def _create_player_from_html(self, html, is_main=True):
        return html
    
    def get_players(self):
        players=[]
        player_htmls=self._main_team_html.find_all("li", {"class":"structure__item"})
        players.extend([self._create_player_from_html(html) for html in player_htmls])
        return players




class Match:
    """
    A class for interacting with html data
    its like a data object, gets a raw hml
    has properties and functions to return
    players, match data, score and others
    """
    def __init__(self, html_text, parser='html.parser'):
        self._soup= BeautifulSoup(html_text,parser)

    @property
    def team_names(self) -> list[str]:
        "returns team names of given match"
        divs_with_names=self._soup.find_all("div", {"class":"structure__top-name"})[:2]
        return [name.string for name in divs_with_names]
    
    @property
    def home_team_name(self) -> str:
        'returns home team name, parses whole html every call'
        return self.team_names[0]

    @property
    def guest_team_name(self) -> str:
        'returns guest team name, parses whole html every call'
        return self.team_names[1]
    
    def get_teams(self):
        """retrieves html data for teams
        in former html teams are separated in three blocks
        main, reverse, and trainers
        home and guest team lies in one div, so we need to separate then and 
        collect data per team in this function"""
        protocol_tab=soup.find('div',id="match-tabs-protocol")
        divs_with_players=protocol_tab.find_all("div", {"class": "structure__unit"})
        home_team_main_players_div_index=0
        home_team_reserve_players_div_index=2
        home_team_trainers_div_index=4

        guest_team_main_players_div_index=1
        guest_team_reserve_players_div_index=3
        guest_team_trainers_div_index=5

        home_team=Team(
            main_team_html=divs_with_players[home_team_main_players_div_index],
            reserve_team_html=divs_with_players[home_team_reserve_players_div_index],
            trainers_html=divs_with_players[home_team_trainers_div_index])
        
        guest_team=Team(
            main_team_html=divs_with_players[guest_team_main_players_div_index],
            reserve_team_html=divs_with_players[guest_team_reserve_players_div_index],
            trainers_html=divs_with_players[guest_team_trainers_div_index])
        
        return home_team, guest_team
        


m=Match(page.text)
print(m.team_names)

players=m.get_teams()[0].get_players()
print(players)