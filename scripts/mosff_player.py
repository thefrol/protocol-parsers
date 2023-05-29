import requests
from bs4 import BeautifulSoup
from pprint import pprint

from protocol_parsers import MosffPlayerParser



p=MosffPlayerParser('https://mosff.ru/player/2060')

pprint(p.to_rbdata())