from .player_page import MosffTeam

class MosffTeamForTeamPage(MosffTeam):
    @property
    def raw_name(self):
        return self._team_tag.a.text

class TeamPage:

    
    def __init__(self, team_page_text,parser='html.parser'):
        self._html=team_page_text
        self.div_with_name=self._html.find("div", {"class":"figure-head__wrapper"})
    
    @property
    def team(self):
        return MosffTeamForTeamPage(self.div_with_name)
