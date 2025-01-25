import re
import requests
from datetime import datetime

from bs4 import BeautifulSoup

from .webparser import WebParser
from .mosff.player_page import PlayerPage
from .mosff_parser import format_player_name

# class MosffPlayerParser(WebParser[PlayerPage]):
#     """a class that gets a link and returns a json with needed data"""
#     url_pattern=r'https://mosff.ru/player/\d+'
#     def to_rbdata(self):
#         result={}

#         birth_date_parsed=self.page.birth_date

#         if birth_date_parsed.is_healthy:
#             date_=datetime(
#                 year=birth_date_parsed.year,
#                 month=birth_date_parsed.month,
#                 day=birth_date_parsed.day)
#         else:
#             date_=None
        

#         result['birth_date_raw']=self.page.birth_date._date_string
#         result['birth_date']=str(date_) if date_  else None
#         result['birth_date_dict']={
#             'day':birth_date_parsed.day,
#             'month':birth_date_parsed.month,
#             'year':birth_date_parsed.year
#         }

#         result['name']=format_player_name(self.page)
#         result['name_raw']=self.page.name.raw_name

#         result['image_url']=self.page.image_url

#         result['role_raw']=self.page.amplua

#         result['team_id']=self.page.team.id
#         result['team_url']=self.page.team.url
#         result['team_url_raw']=self.page.team.relative_url

#         result['team_name']=self.page.team.name
#         result['team_name_raw']=self.page.team.raw_name
#         result['team_year']=str(self.page.team.year) #TODO remove str(), used for tests
        
#         return result

class MosffPlayerParser(WebParser[PlayerPage]):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/player/(\d+)'
    def __init__(self, url: str):
        match = re.search(self.url_pattern, url)
        if match is None: 
            raise "Cat parse url"
        player_id = match.group(1)

        api_url = f"https://mosff.ru/api/player-profile.get?id={player_id}"
        resp = requests.get(api_url, headers={"User-Agent":"https://mosff.ru/api/player-profile.get?id=58975"})
        if not resp.ok:
            raise "cant get player info"
        player_data = resp.json()

        self.player_data = player_data["playerInfo"]
        # Example:
        # // 20250124221905
        # // https://mosff.ru/api/player-profile.get?id=58975
        #
        # {
        # "success": true,
        # "playerInfo": {
        #     "id": 58975,
        #     "name": "Глазовский Глеб Сергеевич",
        #     "birthDate": "25.03.2010",
        #     "teamName": "Динамовец 2010 г.р.",
        #     "teamUrl": "/team/370",
        #     "amplua": "Защитник",
        #     "photo": "https://hb.bizmrg.com/st.mosmff.ru/player/58975/photo/6786d04c871c2_thumb.png",
        #     "socialLinks": {
        #     "vk": "",
        #     "telegram": "",
        #     "tikTok": ""
        #     },
        #     "overallStats": {
        #     "goals": 0,
        #     "minutes": 45,
        #     "victories": 0,
        #     "games": 1
        #     },
        #     "clubColor": "#FFFFFF"
        # }
        # }

    @property
    def birth_date(self):
        date_string = self.player_data["birthDate"]
        if not date_string:
            return None
        date = datetime.strptime(date_string, '%d.%m.%Y')
        return date


    @property
    def raw_name(self) -> str:
        """ A raw name received from mosff
        
        Фамилия Имя Отчество"""
        return self.player_data["name"]

    @property
    def name(self):
        """ A prepared player name
        First Name + Last Name
        a standard for rbdata"""

        parts = self.raw_name.split(" ")

        # returning first and last
        # 
        # may be can be done smarter
        if len(parts)==1:
            return parts[0]
        else:
            last_name = parts[0] # goes first in string
            first_name = parts[1] # goes second
            return f"{first_name} {last_name}"
    
    @property
    def team_url(self)-> str | None:
        return self.player_data["teamUrl"]
    
    @property
    def team_id(self):
        if self.team_url is None:
            return None
        return self.team_url.split("/")[-1]
    
    @property
    def team_name(self):
        return self.player_data["teamName"]
    
    @property
    def team_year(self):
        regexp = r"\d\d\d\d"
        m = re.search(regexp, self.team_name)
        if m is None:
            return None
        return m.group(0)
        
    def to_rbdata(self):
        result={}
        

        result['birth_date_raw']=self.player_data["birthDate"]
        result['birth_date']=str(self.birth_date) if self.birth_date  else None
        result['birth_date_dict']={
            'day': self.birth_date.day,
            'month': self.birth_date.month,
            'year': self.birth_date.year
        }

        result['name']= self.name
        result['name_raw']=self.raw_name

        result['image_url']=self.player_data["photo"]

        result['role_raw']=self.player_data["amplua"]

        result['team_id']=self.team_id
        result['team_url']=f"https://mosff.ru{self.team_url}"
        result['team_url_raw']=self.team_url

        result['team_name']=self.team_name
        result['team_name_raw']=self.team_name
        result['team_year']=self.team_year
        
        return result