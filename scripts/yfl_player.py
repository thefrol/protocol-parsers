from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers.yfl_player_parser import YflPlayerParser

url='https://yflrussia.ru/player/5070344' # ufl3

page=YflPlayerParser(url)

pprint(page.to_rbdata())




