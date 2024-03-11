from bs4 import BeautifulSoup
from pprint import pprint
import requests

from protocol_parsers import YflParser


url="https://yflrussia.ru/match/3794816"
with open("yfl-fixture.html",'r') as f:
    text=f.read()

page=YflParser(url=url,html_text=text)


promo= page.page.promo
print(promo.home_team.name, promo.home_team.id)
print(promo.guest_team.name,promo.guest_team.id)


# pprint(page.to_rbdata())




