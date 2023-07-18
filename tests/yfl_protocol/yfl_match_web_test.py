import unittest
from typing import Callable

from protocol_parsers import YflParser
from protocol_parsers.yfl  import MatchPage, Team
from datetime import datetime
import yfl_protocol.base as yfl_base
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


def test_substitutions(test:unittest.TestCase, page:MatchPage):
    for event in page.events:
        if event.is_substitute:
            player_left=page.find_player_by_id(event.assist_id)
            player_entered=page.find_player_by_id(event.author_id)
            test.assertEqual(player_left.sub_to_id, player_entered.id)
            test.assertEqual(player_entered.sub_from_id,player_left.id)
            test.assertIs(player_entered.sub_in_event,player_left.sub_out_event)
            test.assertIs(player_entered.sub_in_event,event)



class BasicMatchTest(yfl_base.YFlMatch):
    url='https://yflrussia.ru/match/3409563'
    def test_promo(self):

        self.page.promo.home_team.name
        self.assertEqual(self.page.promo.home_team.name,'Рубин')
        self.assertEqual(self.page.promo.home_team.id,1311490)

        self.assertEqual(self.page.promo.guest_team.name,'ЦСКА')
        self.assertEqual(self.page.promo.guest_team.id,1246836)

        self.assertEqual(self.page.promo.home_team.tournament_id,1031676)
        self.assertEqual(self.page.promo.tournament.name,'МФЛ')

        self.assertEqual(self.page.promo.score_raw_text,'2:3')
        self.assertEqual(self.page.promo.scores,['2','3'])
        self.assertEqual(self.page.promo.home_score,2)
        self.assertEqual(self.page.promo.guest_score,3)

        self.assertEqual(self.page.promo.date.as_datetime,datetime(2023,7,7,15,0),'wrong date')

    def test_team_tab(self):
        self.assertEqual(self.page.home_team.name,'Рубин')
        
        self.assertEqual(self.page.guest_team.name,'ЦСКА')



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
        """test of events data"""
        self.assertEqual(self.page.events.yellow_cards, 7, 'total yellow cards is 7')
        self.assertEqual(self.page.home_team.events.yellow_cards, 2, 'home team yellow cards is 2')
        self.assertEqual(self.page.guest_team.events.yellow_cards, 4, 'guest team yellow cards is 4, and one for trainer not counted') # without a trainer #TODO add staff

        self.assertEqual(self.page.events.goals,5,'totally 5 goals')
        self.assertEqual(self.page.home_team.events.goals,2) # TODO add to self check if events goals are not equal to toal goals from promo
        self.assertEqual(self.page.guest_team.events.goals,3)

    def test_players(self):
        """testing separate players, goals, cards, time played"""
        lavrenkov=self.page.find_player_by_name('Артем Лавренков')

        self.assertEqual(lavrenkov.goals,2)
        self.assertEqual(lavrenkov.time_on_field,90)
        self.assertEqual(lavrenkov.time_in,0)
        self.assertEqual(lavrenkov.number,'68')
        self.assertTrue(lavrenkov.is_main_player)
        self.assertFalse(lavrenkov.is_goalkeeper)

        golybin=self.page.find_player_by_name('Ренат Голыбин')

        self.assertEqual(golybin.goals,1)
        self.assertEqual(golybin.time_on_field,77)
        self.assertEqual(golybin.time_in,0)
        self.assertEqual(golybin.number,'47')
        self.assertTrue(golybin.is_main_player)
        self.assertFalse(golybin.is_goalkeeper)

        sarraf=self.page.find_player_by_name('Максим Сарраф')

        self.assertFalse(sarraf.has_played)
        self.assertIsNone(sarraf.time_in)
        self.assertEqual(sarraf.number,'70')
        self.assertFalse(sarraf.is_main_player)
        self.assertTrue(sarraf.is_goalkeeper)

        capitain_rubin=self.page.find_player_by_name('Никита Билялютдинов')
        self.assertTrue(capitain_rubin.is_capitain)
        

        pershin=self.page.find_player_by_name('Денис Першин')

        self.assertEqual(pershin.number,'83')
        self.assertEqual(pershin.events.yellow_cards,1)

        shaih= self.page.find_player_by_name('Владимир Шайхутдинов')
        self.assertEqual(shaih.missed_goals,2)
        self.assertAlmostEqual(shaih.number,'86')
        self.assertTrue(shaih.is_goalkeeper)
        self.assertTrue(shaih.is_main_player)
        self.assertFalse(shaih.is_capitain)

        ismagilov= self.page.find_player_by_name('Артем Исмагилов')
        self.assertEqual(ismagilov.missed_goals,3)
        self.assertEqual(ismagilov.number,'99')



    def test_subbing(self):
        savva=self.page.find_player_by_name('Савва Пономарев')
        kuznecov=self.page.find_player_by_name('Максим Кузнецов')
        self.assertEqual(savva.sub_from_id, kuznecov.id)
        self.assertEqual(kuznecov.sub_to_id, savva.id)
        self.assertEqual(savva.sub_in_event.minute, 71)
        test_substitutions(self,self.page) # tests substitutions for full match


if __name__ == '__main__':
    unittest.main()