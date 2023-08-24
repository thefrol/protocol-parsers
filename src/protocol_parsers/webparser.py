import re
import requests
import json
from typing import TypeVar, Generic, get_args

from bs4 import BeautifulSoup
from abc import abstractmethod

TParser=TypeVar('TParser')

class WebParser(Generic[TParser]):
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    def __init__(self, url:str,html_text=None):
        if all([url, html_text]):
            print(f'specified url and html_text in parser. Url will be ignored')
        if html_text is None:
            if not re.fullmatch(self.url_pattern,url):
                print(f'seems like {url} not fits url pattern{self.url_pattern}')
            try:
                page=requests.get(url)
            except ConnectionError as e:
                raise ConnectionError(f"Невозможно подключиться к серверу {url}: {e}")

            if page.status_code != 200:
                raise ConnectionError(f'Запрос не выполнился с кодом 200. Запрос был на адрес {url}')
            html_text=page.text
            
        self._html=BeautifulSoup(html_text, 'html.parser')
        self._page:TParser=self.create_parser_instance(self._html)
    def create_parser_instance(self,*args,**kwargs)->TParser:
        """returns a new instance of TParser
        passes args ang kwargs to __init__()"""
        from .mosff import Match
        base_generic_class=self.__orig_bases__[0]
        parser_class_=get_args(base_generic_class)[0]
        return parser_class_(*args,**kwargs)
    
    @property
    def page(self)->TParser:
        return self._page
    
    @abstractmethod
    def to_rbdata(self):
        pass
    
    def to_json(self)->str:
        '''returns a json string formatted in style of rbdata'''
        return json.dumps(self.to_rbdata(),ensure_ascii=False)