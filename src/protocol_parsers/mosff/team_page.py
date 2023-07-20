from functools import cached_property

from ..tagminer import TagMiner
from .team_stub import MosffTeam
from ..decorators import trim

class TeamPageTeam(MosffTeam):
    @property
    @trim
    def raw_name(self):
        return self._find_tag(class_='figure-head__title').text
    
    @property
    def relative_url(self):
        return self.a['href']

class TeamPage(TagMiner):
    @cached_property
    def team(self):
        tag=self._find_tag(class_="figure-head__wrapper")
        return TeamPageTeam(tag)
