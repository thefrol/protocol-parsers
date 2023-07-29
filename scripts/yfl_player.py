from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflPlayerParser

#url='https://yflrussia.ru/player/5070344' # ufl3
#url='https://yflrussia.ru/player/4609808' #acron
url='https://yflrussia.ru/player/4891177' #no birth date

page=YflPlayerParser(url)

pprint(page.to_rbdata())




