from protocol_parsers import MosffParser
from pprint import pprint


URL='https://mosff.ru/match/34549'
#URL='https://mosff.ru/match/34858'

d=MosffParser(URL).to_rbdata()

pprint(d)