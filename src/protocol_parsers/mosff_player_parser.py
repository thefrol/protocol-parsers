import re
import requests
from datetime import datetime

from .mosff.player_page import PlayerPage
from .mosff_parser import format_player_name

class MosffPlayerParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/player/\d+'
    def __init__(self, url:str):
        if not re.fullmatch(self.url_pattern,url):
            print(f'seems like {url} is not from mosff player page')
        
        page=requests.get(url) 

        if page.status_code != 200:
            raise ConnectionError('page not retrieved')
        
        self.player=PlayerPage(page.text)

    def to_rbdata(self):
        result={}

        birth_date_parsed=self.player.birth_date

        if birth_date_parsed.is_healthy:
            date_=datetime(
                year=birth_date_parsed.year,
                month=birth_date_parsed.month,
                day=birth_date_parsed.day)
        else:
            date_=None
        

        result['birth_date_raw']=self.player.birth_date.text
        result['birth_date']=str(date_) if date_  else None
        result['birth_date_dict']={
            'day':birth_date_parsed.day,
            'month':birth_date_parsed.month,
            'year':birth_date_parsed.year
        }

        result['name']=format_player_name(self.player)
        result['name_raw']=self.player.a_with_name.text
        return result