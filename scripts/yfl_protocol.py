from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflParser

#url='https://yflrussia.ru/match/3061996'
#url='https://yflrussia.ru/match/2848878' # ufl3
#url='https://yflrussia.ru/match/3409570' # ufl3
#url='https://yflrussia.ru/match/3409563'
url='https://yflrussia.ru/match/3409643' ### No NUMBER AT PLAYER to tests

page=YflParser(url)

pprint(page.to_rbdata())




