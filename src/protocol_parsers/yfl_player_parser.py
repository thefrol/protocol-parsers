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

        if birth_date_parsed.is_healthy: #TODO looks ungly, needs refactor
            date_=datetime(
                year=birth_date_parsed.year,
                month=birth_date_parsed.month,
                day=birth_date_parsed.day)

            result['birth_date_raw']=page.birth_date._date_string
            result['birth_date']=str(date_) if date_  else None
            result['birth_date_dict']={
                        'day':birth_date_parsed.day,
                        'month':birth_date_parsed.month,
                        'year':birth_date_parsed.year
                        }
        else:
            date_=None

            result['birth_date_raw']=None
            result['birth_date']=None
            result['birth_date_dict']=None
        



        result['name']=page.name.format_basic
        result['name_raw']=page.name_raw

        result['role_raw']=None

        result['team_id']=page.team.team_id
        result['team_url']=f'https://yflrussia.ru/{page.team.relative_url}'
        result['team_url_raw']=page.team.relative_url

        result['team_name']=f'{page.team.name} {page.team.league_name}'
        result['team_name_raw']=page.team.name_raw
        result['team_year']=page.team.league_name
        
        return result