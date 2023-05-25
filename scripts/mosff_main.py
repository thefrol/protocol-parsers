from protocol_parsers import MosffParser

d=MosffParser('https://mosff.ru/match/34549').to_rbdata(80)

print(d)