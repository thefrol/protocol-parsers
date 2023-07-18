from pprint import pprint

from protocol_parsers import Exporter

url='https://mosff.ru/player/2060'

data=Exporter(url).to_rbdata()

pprint(data)