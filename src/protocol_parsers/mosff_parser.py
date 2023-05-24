import re
import requests
from .mosff import Match

class MosffParser:
    """a class that gets a link and returns a json with needed data"""
    url_pattern=r'https://mosff.ru/match/\d+'
    def __init__(self, url:str):
        if not re.fullmatch(self.url_pattern,url):
            print(f'seems like {url} is not from mosff')
        
        page=requests.get(url)

        if page.status_code != 200:
            raise ConnectionError()
        
        self._match=Match(page.text)

    def to_rbdata(self):
        pass
