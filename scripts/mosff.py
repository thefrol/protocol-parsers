from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass 

URL='https://mosff.ru/match/34549' # a good match with cards, goals, changes


page=requests.get(URL)

if page.status_code != 200:
    raise ConnectionError()

soup=BeautifulSoup(page.text,'html.parser')

def trim(f):
    def callee(*args,**kwargs):
        return f(*args,**kwargs).strip()
    return callee

@dataclass
class Player:
    """a class for parsing player data """
    def __init__(self, player_html, is_main):
        self._player_html=player_html

        self._img=player_html.img
        self._number_div=self._player_html.find('div',{'class':"structure__number"})
        self._position_div=self._player_html.find('div',{'class':"structure__position"})

        self.is_main=is_main
    
    
    @property
    def text_name(self):
        "taken from div"
        name_div=self._player_html.find('div',{'class':"structure__name-text"})
        return next(name_div.stripped_strings)

    @property
    def img_alt_name(self):
        """taken from img alt"""
        return self._img['alt']

    @property
    def name(self):
        return self.img_alt_name or self.text_name
    
    @property
    def img_url(self):
        return self._img['src']
    
    @property
    @trim
    def number(self):
        return self._number_div.text
    
    @property
    def is_capitain(self):
        if self._position_div is None:
            return False
        return True if '(к)' in self._position_div.text else False
    
    @property
    def is_goalkeeper(self):
        if self._position_div is None:
            return False
        return True if '(вр)' in self._position_div.text else False
    
    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'[{self.number}] {self.name}{" (к)" if self.is_capitain else ""}{" (в)" if self.is_goalkeeper else ""}'
    



class Team:
    "a class for holding team html_data and parsing it"

    def __init__(self, main_team_html, reserve_team_html, trainers_html):
        self._main_team_html=main_team_html
        self._reserve_team_html=reserve_team_html
        self._trainers_html=trainers_html

    def _create_player_from_html(self, html, is_main=True):
        return html
    
    @property
    def players(self):
        players=[]
        main_player_htmls=self._main_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=True) for html in main_player_htmls])

        reserve_player_htmls=self._reserve_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=False) for html in reserve_player_htmls])
        return players



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

    def __init__(self, html_text, parser='html.parser'):
        _soup= BeautifulSoup(html_text,parser)
        
        self.divs_with_names=_soup.find_all("div", {"class":"structure__top-name"})[:2]

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
            trainers_html=self.divs_with_players[self.home_team_trainers_div_index])
        
        return home_team
    
    @property
    def guest_team(self):
        guest_team=Team(
            main_team_html=self.divs_with_players[self.guest_team_main_players_div_index],
            reserve_team_html=self.divs_with_players[self.guest_team_reserve_players_div_index],
            trainers_html=self.divs_with_players[self.guest_team_trainers_div_index])
        return guest_team

m=Match(page.text)
print(m.team_names)


print(m.home_team.players)
print(m.guest_team.players)