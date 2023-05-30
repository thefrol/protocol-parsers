import re
import requests
from datetime import datetime

from .mosff.team_page import TeamPage
from .mosff_parser import format_player_name,format_team_name

class MosffTeamParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/team/\d+'
    def __init__(self, url:str):
        if not re.fullmatch(self.url_pattern,url):
            print(f'seems like {url} is not from mosff team page')
        
        page=requests.get(url) 

        if page.status_code != 200:
            raise ConnectionError('page not retrieved')
        
        self.team_page=TeamPage(page.text)

    def to_rbdata(self):
        result={}
        result['name']=format_team_name(self.team_page.team)
        result['name_raw']=self.team_page.team.raw_name
        result['team_year']=self.team_page.team.team_year
        result['id']=self.team_page.team.team_id
        return result
