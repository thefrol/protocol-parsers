import re
import requests
from datetime import datetime

from bs4 import BeautifulSoup

from .webparser import WebParser
from .mosff.player_page import PlayerPage
from .mosff_parser import format_player_name

class MosffPlayerParser(WebParser[PlayerPage]):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/player/\d+'
    def to_rbdata(self):
        result={}

        birth_date_parsed=self.page.birth_date

        if birth_date_parsed.is_healthy:
            date_=datetime(
                year=birth_date_parsed.year,
                month=birth_date_parsed.month,
                day=birth_date_parsed.day)
        else:
            date_=None
        

        result['birth_date_raw']=self.page.birth_date._date_string
        result['birth_date']=str(date_) if date_  else None
        result['birth_date_dict']={
            'day':birth_date_parsed.day,
            'month':birth_date_parsed.month,
            'year':birth_date_parsed.year
        }

        result['name']=format_player_name(self.page)
        result['name_raw']=self.page.name.raw_name

        result['image_url']=self.page.image_url

        result['role_raw']=self.page.amplua

        result['team_id']=self.page.team.id
        result['team_url']=self.page.team.url
        result['team_url_raw']=self.page.team.relative_url

        result['team_name']=self.page.team.name
        result['team_name_raw']=self.page.team.raw_name
        result['team_year']=str(self.page.team.year) #TODO remove str(), used for tests
        
        return result