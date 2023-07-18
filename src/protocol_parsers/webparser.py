import re
import requests
import json
from bs4 import BeautifulSoup
from abc import abstractmethod

class WebParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    page_class:type=None
    def __init__(self, url:str,html_text=None):
        if html_text is None:
            if not re.fullmatch(self.url_pattern,url):
                print(f'seems like {url} not fits url pattern{self.url_pattern}')
            
            page=requests.get(url) 

            if page.status_code != 200:
                raise ConnectionError('page not retrieved')
            html_text=page.text
            
        self._html=BeautifulSoup(html_text, 'html.parser')
        self.page:self.page_class=self.page_class(self._html)
    
    @abstractmethod
    def to_rbdata(self):
        pass
    
    def to_json(self)->str:
        '''returns a json string formatted in style of rbdata'''
        return json.dumps(self.to_rbdata(),ensure_ascii=False)