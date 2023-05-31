import unittest

from protocol_parsers import MosffParser

URL_match_autogoals='https://mosff.ru/match/34858'

def count_team_goals(team, opposing_team):
    '''counts'''
    goal_counter=0
    for player in team.players:
        goal_counter=goal_counter+player.goals
    for player in opposing_team.players:
        goal_counter=goal_counter+player.autogoals

    return goal_counter

class MatchTest(unittest.TestCase):
    url=''
    def setUp(self) -> None:
        self.protocol:MosffParser=MosffParser(self.url)
        self.match=self.protocol._match
        self.home_team=self.match.home_team
        self.guest_team=self.match.guest_team
        return super().setUp()
    def find_by_name(self,name:str):
        strings=name.split(' ')
        if len(strings) !=2:
            raise AttributeError('names must be in format "first_name last_name" in 2 words')
        first_name=strings[0]
        last_name=strings[1]
        return self.match.find_by_name(first_name,last_name)
        
        

class MatchWithAutoGoals(MatchTest):
    '''Testing match with autogoals'''
    url='https://mosff.ru/match/34858'
    def test_scores(self):
        self.assertEqual(self.match.home_score,7,'Home score not right')
        self.assertEqual(self.match.guest_score,2,'guest score error')
        self.assertEqual(count_team_goals(self.match.home_team,self.match.guest_team),7,'sum of players goals != team score @ home team')
        self.assertEqual(count_team_goals(self.match.guest_team,self.match.home_team),2,'sum of players goals != team score @ guest team')
    def test_ids(self):
        self.assertEqual(self.match.guest_team_id,2051,'guest team id failed')
        self.assertEqual(self.match.home_team_id,2044,'home team id failed')
    def test_autogoals(self):
        self.assertEqual(self.match.guest_team.find_player_by_name('Алексей', 'Крылов').autogoals,1, 'У Крылова должен быть один автогол')
        self.assertEqual(self.match.guest_team.find_player_by_name('Матвей', 'Кирилин').autogoals,1, 'У Кирилина должен быть один автогол')
    def test_goals(self):
        self.assertEqual(self.find_by_name('Леонид Чемельков').goals,2,'Чемельков должен забить два')
        self.assertEqual(self.find_by_name('Марк Шкурин').goals,1,'Шкурин должен забить один')

        
if __name__ == '__main__':
    unittest.main()