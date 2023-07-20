from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflParser

url='https://yflrussia.ru/match/3409563'

page=YflParser(url)
#a=page.page['href']
pprint(page.to_rbdata())




