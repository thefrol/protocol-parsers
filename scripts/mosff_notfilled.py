from protocol_parsers import MosffParser
from pprint import pprint

URL='https://mosff.ru/match/37926' 

d=MosffParser(URL).to_rbdata()

pprint(d)