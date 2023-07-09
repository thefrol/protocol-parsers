import unittest
from typing import Callable

from protocol_parsers import YflParser
from protocol_parsers.yfl  import MatchPage, Team
from datetime import datetime
#test time in, time out, time played
# def lineup_status(lineup)
#    return 'bench' if lineup['time_played'] == 0
#    lineup['time_in'] == @ ? 'lineup' : 'sub'
# end
#
# test red cards and time played
# test players id
# test teams id
# test players count
# test autogoals

def count_players(team:Team, func:Callable):
    count=0
    for player in team.players:
        if func(player):
            count=count+1
    return count

class BasicMatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        url='https://yflrussia.ru/match/3409563'
        parser=YflParser(url)
        cls.page:MatchPage=parser.page
    def test_promo(self):

        self.page.promo.home_team.name
        self.assertEqual(self.page.promo.home_team.name,'Рубин')
        self.assertEqual(self.page.promo.home_team.id,1311490)

        self.assertEqual(self.page.promo.guest_team.name,'ЦСКА')
        self.assertEqual(self.page.promo.guest_team.id,1246836)

        self.assertEqual(self.page.promo.home_team.tournament_id,1031676)
        self.assertEqual(self.page.promo.tournament.name,'МФЛ')

        self.assertEqual(self.page.promo.date.as_datetime,datetime(2023,7,7,15,0),'wrong date')

    def test_team_tab(self):
        self.assertEqual(self.page.home_team.name,'Рубин')
        self.assertEqual(self.page.guest_team.name,'ЦСКА')

    def test_business_logic(self):
        home_team=self.page.home_team
        guest_team=self.page.guest_team
        self.assertIs(home_team,guest_team.opposing_team,'home team calculates opposing team wrong')
        self.assertIs(guest_team,home_team.opposing_team,'guest team calculates opposing team wrong')

        self.assertIs(home_team._parent_match,self.page,'home team has wrong parent match')
        self.assertIs(guest_team._parent_match,self.page,'guest team has wrong parent match')

    def test_main_and_bench(self):
        """counts players at main, subbed players and bench players"""
        home_team_start_players_count=count_players(
            self.page.home_team,
            lambda p: p.time_in==0
        )
        guest_team_start_players_count=count_players(
            self.page.guest_team,
            lambda p: p.time_in==0
        )

        self.assertEqual(home_team_start_players_count,11,'must be 11 players at start')
        self.assertEqual(guest_team_start_players_count,11,'must be 11 players at start')

        home_team_sub_players_count=count_players(
            self.page.home_team,
            lambda p: p.time_in is not None and p.time_in>0
        )

        guest_team_sub_players_count=count_players(
            self.page.guest_team,
            lambda p: p.time_in is not None and p.time_in>0
        )

        self.assertEqual(home_team_sub_players_count,5,'must be 5 subbed players at Rubin')
        self.assertEqual(guest_team_sub_players_count,4,'must be 4 subbed players at CSKA')

        home_team_bench_players_count=count_players(
            self.page.home_team,
            lambda p: p.time_in is None
        )

        guest_team_bench_players_count=count_players(
            self.page.guest_team,
            lambda p: p.time_in is None
        )

        self.assertEqual(home_team_bench_players_count,3,'must be 3 bench players at Rubin')
        self.assertEqual(guest_team_bench_players_count,4,'must be 4 bench players at CSKA')
    
    def test_events(self):
        self.assertEqual(self.page.events.yellow_cards, 7, 'total yellow cards is 7')
        self.assertEqual(self.page.home_team.events.yellow_cards, 2, 'home team yellow cards is 2')
        self.assertEqual(self.page.guest_team.events.yellow_cards, 4, 'guest team yellow cards is 4, and one for trainer not counted') # without a trainer

        self.assertEqual(self.page.events.goals,5,'totally 5 goals')
        self.assertEqual(self.page.home_team.events.goals,2) # TODO add to self check if events goals are not equal to toal goals from promo
        self.assertEqual(self.page.guest_team.events.goals,3)


if __name__ == '__main__':
    unittest.main()