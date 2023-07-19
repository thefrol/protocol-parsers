import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from .webparser import WebParser
from .mosff.team_page import TeamPage
from .mosff_parser import format_player_name,format_team_name

class MosffTeamParser(WebParser):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/team/\d+'
    page_class=TeamPage

    def to_rbdata(self):
        result={}
        result['name']=format_team_name(self.page.team)
        result['name_raw']=self.page.team.raw_name
        result['team_year']=self.page.team.team_year
        result['id']=self.page.team.team_id
        return result
