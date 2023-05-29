"""a class for interacting with player web page on mosff website
link looks like this https://mosff.ru/player/2060"""

import re
from bs4 import BeautifulSoup

from .player import ImgAltName #TODO rename FIO
from ..decorators import trim, to_int


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

class MosffDate:
    _date_pattern=r'(?P<date_string>(?P<day>\d+) (?P<month>\w+) (?P<year>\d+))\s?(\((?P<years_old>\d+) \w+\))'
    _months_list=['', 'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    def __init__(self, date_string):
        self._date_string=date_string
        self._regexp_match=re.fullmatch(self._date_pattern,date_string)

    def __get_regexp_group(self,name):
        if self._regexp_match:
            return self._regexp_match.group(name)
        else:
            return None
    @property
    @to_int
    def day(self):
        return self.__get_regexp_group('day')
    @property
    def month_string(self):
        return self.__get_regexp_group('month')
    
    @property
    def month(self):
        return self._months_list.index(self.month_string[:3])

    @property
    @to_int
    def year(self):
        return self.__get_regexp_group('year')
    @property
    @to_int
    def years_old(self):
        return self.__get_regexp_group('years_old')
    @property
    def text(self):
        return self.__get_regexp_group('date_string')
    
    @property
    def is_healthy(self):
        return self.day is not None and self.month is not None and self.year is not None



class PlayerPage:

    
    def __init__(self, player_page_text,parser='html.parser'):

        self._player_page_html=BeautifulSoup(player_page_text,parser)
        self.a_with_name=self._player_page_html.find("a", {"class":"profile__title"})
        li_with_properties=self._player_page_html.find("ul", {"class":"profile__list"}).find_all("li", {"class":"profile__item"})
        self.properties=PlayerPagePropertiesList(li_with_properties)

    @property
    def name(self):
        return ImgAltName(self.a_with_name.text)

    @property
    def birth_date(self):
        return MosffDate(self.properties.birth_date.text)

    