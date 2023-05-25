from protocol_parsers import MosffParser
from pprint import pprint

d=MosffParser('https://mosff.ru/match/34549').to_rbdata()

pprint(d)