from bs4 import BeautifulSoup

from .team import Team

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
