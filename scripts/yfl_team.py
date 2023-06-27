from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflTeamParser

url='https://yflrussia.ru/team/1247155' # cska ufl3

page=YflTeamParser(url)

pprint(page.to_rbdata())




