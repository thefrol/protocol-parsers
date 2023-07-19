"""a class for interacting with player web page on mosff website
link looks like this https://mosff.ru/player/2060"""

import re

from .player import FioName #TODO rename FIO
from ..date import PageDate
from ..decorators import trim


class PlayerPageProperty:
    """a class for interacting with profile properties
    like amplue or bitrh date gets html return propery name and value"""
    def __init__(self, property_html):
        self._property_html=property_html

    @property
    @trim
    def name(self)->str:
        return self._property_html.find('div',{'class':'profile__property'}).text
    
    @property
    @trim
    def text(self)->str:
        return self.value_tag.text

    @property
    def value_tag(self):
        return self._property_html.find('div',{'class':'profile__value'})

    @property
    def is_birth_date(self):
        return 'рожден' in self.name
    
    @property
    def is_amplua(self):
        return 'амплуа' in self.name.lower()
    
    @property
    def is_team(self):
        return 'команда' in self.name.lower()
    
class PlayerPagePropertiesList:
    def __init__(self, properties_htmls):
        self._list:list[PlayerPageProperty]=[PlayerPageProperty(html) for html in properties_htmls]
    @property
    def birth_date(self):
        for item in self._list:
            if item.is_birth_date:
                return item
        return None
    @property
    def amplua(self):
        for item in self._list:
            if item.is_amplua:
                return item
        return None
    @property
    def team(self):
        for item in self._list:
            if item.is_team:
                return item
        return None



class MosffDate(PageDate):
    @property
    def _date_pattern(self):
        return r'(?P<date_string>(?P<day>\d+) (?P<month>\w+) (?P<year>\d+))\s?(\((?P<years_old>\d+) \w+\))'
    
    @property
    def is_healthy(self):
        return self.day is not None and self.month is not None and self.year is not None

class MosffTeam: #TODO implement to team.py
    _team_name_pattern=r'(?P<team_name>.*) (?P<team_year>\d{4,20}) г.р.' #TODO intersects with team.py
    _team_id_pattern=r'/team/(?P<team_id>\d+)\Z'
    def __init__(self, team_html_tag):
        self._team_tag=team_html_tag

    @property
    def raw_name(self):
        return self._team_tag.text
    
    @property
    def name_without_year(self):
        'returns team name without year'
        m=re.fullmatch(self._team_name_pattern, self.raw_name)
        if m:
            return m.group('team_name')
        else:
            print('cant resolve team name with year. returning full name')
            return self.raw_name

    @property
    def team_year(self):
        'returns team year of birth'
        m=re.fullmatch(self._team_name_pattern, self.raw_name)
        if m:
            return m.group('team_year')
        else:
            print('cant resolve team year. returning None')
            return None  
    @property
    def relative_url(self):
        return self._team_tag.a['href']
    @property
    def url(self):
        return 'https://mosff.ru'+self.relative_url
    @property
    def team_id(self):
        m=re.fullmatch(self._team_id_pattern,self.relative_url)
        if m:
            return int(m.group('team_id'))
        else:
            print('cant parse home team id')
            return None        

class PlayerPage:

    
    def __init__(self, player_page_text,parser='html.parser'):

        self._player_page_html=player_page_text
        self.a_with_name=self._player_page_html.find("a", {"class":"profile__title"})
        li_with_properties=self._player_page_html.find("ul", {"class":"profile__list"}).find_all("li", {"class":"profile__item"})
        self.properties=PlayerPagePropertiesList(li_with_properties)

    @property
    def name(self):
        return FioName(self.a_with_name.text)

    @property
    def birth_date(self):
        return MosffDate(self.properties.birth_date.text)
    
    @property
    def amplua(self):
        property_= self.properties.amplua
        if property_:
            return property_.text
        else:
            return None

    @property
    def team(self):
        property_=self.properties.team
        if property_:
            return MosffTeam(property_.value_tag)
        else:
            return None
    
    