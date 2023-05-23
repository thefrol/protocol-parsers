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
    name: str
    is_capitain: bool
    is_main: bool

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
        home_main_players=divs_with_players[0]
        guest_main_players=divs_with_players[1]
        main_reserve_players=divs_with_players[2]


m=Match(page.text)
print(m.team_names)