import requests
from bs4 import BeautifulSoup
from pprint import pprint

from protocol_parsers import MosffTeamParser



t=MosffTeamParser('https://mosff.ru/team/2044')

pprint(t.to_rbdata())