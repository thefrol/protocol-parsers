import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from .webparser import WebParser
from .mosff.team_page import TeamPage

class MosffTeamParser(WebParser[TeamPage]):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/team/\d+'

    def to_rbdata(self):
        result={}
        result['name']=self.page.team.name
        result['name_raw']=self.page.team.raw_name
        result['team_year']=self.page.team.year
        result['id']=self.page.team.id
        return result
