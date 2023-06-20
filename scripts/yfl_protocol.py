from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers.yfl_parser import YflParser

#url='https://yflrussia.ru/match/3061996'
url='https://yflrussia.ru/match/2848878' # ufl3

page=YflParser(url)

pprint(page.to_rbdata())




