import re
import requests
from datetime import datetime

from .yfl import TeamPage
from .webparser import WebParser

class YflTeamParser(WebParser):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://yflrussia.ru/team/\d+'
    page_class=TeamPage

    @property
    def page(self)->TeamPage:
        return self._page

    def to_rbdata(self):
        result={}
        page:TeamPage=self.page

        result['name']=f'{page.name} {page.league_name}'
        result['name_raw']=page.name_raw
        result['team_year']=page.league_name #TODO Add league property
        result['id']=page.team_id

        return result