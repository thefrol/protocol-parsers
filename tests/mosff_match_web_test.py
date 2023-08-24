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
    @classmethod
    def setUpClass(cls) -> None:
        cls.protocol:MosffParser=MosffParser(cls.url)
        cls.match=cls.protocol.page
        cls.home_team=cls.match.home_team
        cls.guest_team=cls.match.guest_team
    def find_by_name(self,name:str):
        strings=name.split(' ')
        if len(strings) !=2:
            raise AttributeError('names must be in format "first_name last_name" in 2 words')
        first_name=strings[0]
        last_name=strings[1]
        return self.match.find_by_name(first_name,last_name)
        
        

class AutoGoals(MatchTest):
    '''Testing match with autogoals'''
    url='https://mosff.ru/match/34858'
    def test_scores(self):
        self.assertEqual(self.match.promo.score.home,7,'Home score not right')
        self.assertEqual(self.match.promo.score.guest,2,'guest score error')
        self.assertEqual(count_team_goals(self.match.home_team,self.match.guest_team),7,'sum of players goals != team score @ home team')
        self.assertEqual(count_team_goals(self.match.guest_team,self.match.home_team),2,'sum of players goals != team score @ guest team')
    def test_autogoals(self):
        self.assertEqual(self.match.guest_team.find_player_by_name('Алексей', 'Крылов').autogoals,1, 'У Крылова должен быть один автогол')
        self.assertEqual(self.match.guest_team.find_player_by_name('Матвей', 'Кирилин').autogoals,1, 'У Кирилина должен быть один автогол')
    def test_goals(self):
        self.assertEqual(self.find_by_name('Леонид Чемельков').goals,2,'Чемельков должен забить два')
        self.assertEqual(self.find_by_name('Марк Шкурин').goals,1,'Шкурин должен забить один')


class AutoGoalsGoalKeeper(MatchTest):
    '''Testing match with autogoals in goalkeeper'''
    #insane case
    url='https://mosff.ru/match/34540'
    def test_missed(self):
        self.assertEqual(self.match.promo.score.home,2,'Home score not right')
        #self.assertEqual(self.find_by_name('Фёдор Старостин').,4,'Старостин пропустил три плюс автогол')
        #we cant count missed goals here, only in yfl

class Cards(MatchTest):
    '''Testing match with autogoals'''
    url='https://mosff.ru/match/34549'
    def count_cards_at_team(self, team:str, card_type:str):
        team=self.match.home_team if team=='home' else self.match.guest_team
        counter=0
        for player in team.players:
            counter=counter + player.yellow_cards if card_type=='yellow' else player.red_cards
        return counter
    def test_total_cards(self):
        self.assertEqual(self.count_cards_at_team('home','yellow'),1,'error in home team yellow cards')
        self.assertEqual(self.count_cards_at_team('guest','yellow'),5,'error in guest team yellow cards')
        self.assertEqual(self.count_cards_at_team('home','red'),0,'error in home team red cards')
        self.assertEqual(self.count_cards_at_team('guest','red'),0,'error in guest team red cards')

class MatchGlobalParams(MatchTest):
    url='https://mosff.ru/match/34858'
    def test_ids(self):
        self.assertEqual(self.match.promo.guest_team.id,2051,'guest team id failed')
        self.assertEqual(self.match.promo.home_team.id,2044,'home team id failed')
    def test_raw_names(self):
        self.assertEqual(self.match.promo.home_team.raw_name, 'ФШМ 2013 г.р.','home team name error')
        self.assertEqual(self.match.promo.guest_team.raw_name, 'Сокол 2013 г.р.','guest team name error')
    def test_names(self):
        self.assertEqual(self.match.promo.home_team.name, 'ФШМ 2013','home team name error')
        self.assertEqual(self.match.promo.guest_team.name, 'Сокол 2013','guest team name error')
    def test_tournament(self):
        self.assertEqual(self.match.tournament.id,484, 'tournament id failed to parse')
        self.assertEqual(self.match.tournament.year,2023)
        self.assertFalse(self.match.tournament.is_cup)
    def test_date(self):
        self.assertEqual(self.match.date.day,21)
        self.assertEqual(self.match.date.month,5)
        self.assertEqual(self.match.date.hour,11)
        self.assertEqual(self.match.date.minute,30)
        self.assertEqual(self.match.date.week_day,7)

class FancyProtocols(unittest.TestCase):
    #TODO make some parsing exceptions
    def test_no_minute_on_autogoal(self):
        """this protocol lacks minute on autogoal event, so it failed earlier"""
        url='https://mosff.ru/match/34540'
        parser=MosffParser(url)
        self.assertIsNotNone(parser.to_rbdata(), 'data not found.')
        self.assertTrue(parser.page.tournament.is_cup)

        

        
if __name__ == '__main__':
    unittest.main()