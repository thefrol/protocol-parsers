from pprint import pprint

from protocol_parsers import Exporter

url='https://yflrussia.ru/match/3409563'

data=Exporter(url).to_rbdata()

pprint(data)