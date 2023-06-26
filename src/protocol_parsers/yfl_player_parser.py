import re
import requests
from datetime import datetime

from .yfl import PlayerPage
from .webparser import WebParser

class YflPlayerParser(WebParser):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://yflrussia.ru/player/\d+'
    page_class=PlayerPage

    def to_rbdata(self):
        result={}
        page:PlayerPage=self.page

        birth_date_parsed=page.birth_date

        if birth_date_parsed.is_healthy:
            date_=datetime(
                year=birth_date_parsed.year,
                month=birth_date_parsed.month,
                day=birth_date_parsed.day)
        else:
            date_=None
        

        result['birth_date_raw']=page.birth_date._date_string
        result['birth_date']=str(date_) if date_  else None
        result['birth_date_dict']={
            'day':birth_date_parsed.day,
            'month':birth_date_parsed.month,
            'year':birth_date_parsed.year
        }

        result['name']=page.name.format_basic
        result['name_raw']=page.name_raw

        result['role_raw']=None

        result['team_id']=None
        result['team_url']=None
        result['team_url_raw']=None

        result['team_name']=None
        result['team_name_raw']=None
        result['team_year']=None
        
        return result