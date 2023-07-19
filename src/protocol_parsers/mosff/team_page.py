from functools import cached_property

from ..tagminer import TagMiner
from .player_page import MosffTeam

class MosffTeamForTeamPage(MosffTeam):
    @property
    def raw_name(self):
        return self._html.a.text

class TeamPage(TagMiner):
    @cached_property
    def team(self):
        tag=self._find_tag(class_="figure-head__wrapper")
        return MosffTeamForTeamPage(tag)
