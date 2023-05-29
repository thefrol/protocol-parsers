import requests
from bs4 import BeautifulSoup
from protocol_parsers.mosff.player_page import PlayerPage


url='https://mosff.ru/player/2060'

page=requests.get(url) 

if page.status_code != 200:
    raise ConnectionError('page not retrieved')

_soup=BeautifulSoup(page.text,'html.parser')
p=PlayerPage(_soup)

print(p.name)
print(p.birth_date.day)
print(p.birth_date.month)
print(p.birth_date.year)
print(p.birth_date.years_old)

