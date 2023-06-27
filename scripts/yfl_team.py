from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflTeamParser

#url='https://yflrussia.ru/team/1247155' # cska ufl3
url='https://yflrussia.ru/team/1246836' #mfl

page=YflTeamParser(url)

pprint(page.to_rbdata())




