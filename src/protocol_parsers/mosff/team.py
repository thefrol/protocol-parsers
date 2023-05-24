from .player import Player

class Team:
    "a class for holding team html_data and parsing it"

    def __init__(self, main_team_html, reserve_team_html, trainers_html):
        self._main_team_html=main_team_html
        self._reserve_team_html=reserve_team_html
        self._trainers_html=trainers_html
    
    @property
    def players(self):
        players=[]
        main_player_htmls=self._main_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=True) for html in main_player_htmls])

        reserve_player_htmls=self._reserve_team_html.find_all("li", {"class":"structure__item"})
        players.extend([Player(html, is_main=False) for html in reserve_player_htmls])
        return players
