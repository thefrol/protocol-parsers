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

Buludov=PlayerData(
    url='https://mosff.ru/player/27653',
    birth_date=(17,5,2013),
    raw_name='Булудов Аристотель Робертович',
)

Chemelkov=PlayerData(
    url='https://mosff.ru/player/28407',
    birth_date=(4,5,2013),
    raw_name='Чемельков Леонид Русланович',
)


from protocol_parsers import MosffPlayerParser

class PlayerTest(unittest.TestCase):
    players=[Ulianov,Buludov]

    def test_birth(self):
        for player in self.players:
            parser=MosffPlayerParser(player.url)
            day=parser.page.birth_date.day
            month=parser.page.birth_date.month
            year=parser.page.birth_date.year
            self.assertEqual((day,month,year),player.birth_date,'wrong birth date parsed')

    def test_raw_name(self):
        for player in self.players:
            parser=MosffPlayerParser(player.url)
            self.assertAlmostEqual(parser.page.name.raw_name, player.raw_name,'name parsed wrong')

if __name__ == '__main__':
    unittest.main()
        
