from protocol_parsers import MosffParser
from pprint import pprint


#URL='https://mosff.ru/match/34549'
#URL='https://mosff.ru/match/38876' #CUP
#URL='https://mosff.ru/match/38860' #CUP  2009
URL='https://mosff.ru/match/34540' #no minute for autogoals, add to tests


d=MosffParser(URL).to_rbdata()

pprint(d)