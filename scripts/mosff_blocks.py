from protocol_parsers import MosffParser
from protocol_parsers.mosff.player_block import PlayerBlock,PlayerBlockList
from pprint import pprint


#URL='https://mosff.ru/match/34549'
URL='https://mosff.ru/match/38876' #CUP
#URL='https://mosff.ru/match/38860' #CUP 2009
#URL='https://mosff.ru/match/34540' #no minute for autogoals, add to tests

def home_players(block:PlayerBlock):
    return block.is_home_team and block.is_players

p=MosffParser(URL)
b=p.page.promo.home_team.year
#print(p.page._find_tag(class_='match__team match__team--right').text)

pprint(b)