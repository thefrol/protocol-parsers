import unittest

from protocol_parsers import YflParser
from protocol_parsers.yfl  import MatchPage
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




if __name__ == '__main__':
    unittest.main()