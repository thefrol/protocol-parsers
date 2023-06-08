from protocol_parsers import MosffParser
from pprint import pprint


#URL='https://mosff.ru/match/34549'
#URL='https://mosff.ru/match/38876' CUP
URL='https://mosff.ru/match/38860' #CUP 2009

d=MosffParser(URL).to_rbdata()

pprint(d)