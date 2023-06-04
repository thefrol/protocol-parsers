import unittest
from dataclasses import dataclass

@dataclass 
class PlayerData:
    url: str
    raw_name: str
    birth_date: tuple[int,int,int]

Ulianov=PlayerData(
    url='https://mosff.ru/player/2060',
    birth_date=(30,6,2006),
    raw_name='Ульянов Иван Евгеньевич',
)

from protocol_parsers import MosffPlayerParser

class PlayerTest(unittest.TestCase):
    players=[Ulianov]

    def test_birth(self):
        for player in self.players:
            parser=MosffPlayerParser(player.url)
            day=parser.player.birth_date.day
            month=parser.player.birth_date.month
            year=parser.player.birth_date.year
            self.assertEqual((day,month,year),player.birth_date,'wrong birth date parsed')

    def test_raw_name(self):
        for player in self.players:
            parser=MosffPlayerParser(player.url)
            self.assertAlmostEqual(parser.player.name.raw_name, player.raw_name,'name parsed wrong')

if __name__ == '__main__':
    unittest.main()
        
