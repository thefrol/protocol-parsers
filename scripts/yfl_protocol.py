from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflParser

#url='https://yflrussia.ru/match/3061996'
#url='https://yflrussia.ru/match/2848878' # ufl3
#url='https://yflrussia.ru/match/3409570' # ufl3
url='https://yflrussia.ru/match/3794816'

page=YflParser(url)



print(page.page.promo)

# pprint(page.to_rbdata())




