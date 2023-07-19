import unittest
from dataclasses import dataclass

from protocol_parsers import MosffTeamParser

@dataclass 
class TeamData:
    url: str
    raw_name: str
    team_year: str
    name_without_year: str

FSM2013=TeamData(
    url='https://mosff.ru/team/2044',
    raw_name='ФШМ 2013 г.р.',
    team_year=2013,
    name_without_year='ФШМ'
    

)

class TeamTest(unittest.TestCase):
    teams=[FSM2013]

    def test_params(self):
        for team in self.teams:
            parser=MosffTeamParser(team.url)
            self.assertEqual(parser.page.team.raw_name, team.raw_name,'name parsed wrong')
            self.assertEqual(parser.page.team.team_year, str(team.team_year),'team_year parsed wrong')
            self.assertEqual(parser.page.team.name_without_year, team.name_without_year,'name_withou_year parsed wrong')

if __name__ == '__main__':
    unittest.main()
        
