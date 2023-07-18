"""Base class for tests"""

import unittest
from protocol_parsers import YflParser
from protocol_parsers.yfl  import MatchPage, Team
from datetime import datetime

class YFlMatch(unittest.TestCase):
    url=None
    @classmethod
    def setUpClass(cls) -> None:
        if cls.url is None:
            raise AttributeError('Specify protocol URL for test class')
        parser=YflParser(cls.url)
        cls.page:MatchPage=parser.page
    def test_consistency(self):
        '''test of data, all names filled, all numbers filled and other'''
        players=self.page.home_team.players+self.page.guest_team.players
        for player in players:
            self.assertGreater(int(player.number),0)
            self.assertIsNotNone(player.name)

        for event in self.page.events:
            self.assertGreaterEqual(event.minute,0)
    def test_business_logic(self):
        home_team=self.page.home_team
        guest_team=self.page.guest_team
        self.assertIs(home_team,guest_team.opposing_team,'home team calculates opposing team wrong')
        self.assertIs(guest_team,home_team.opposing_team,'guest team calculates opposing team wrong')

        self.assertIs(home_team._parent_match,self.page,'home team has wrong parent match')
        self.assertIs(guest_team._parent_match,self.page,'guest team has wrong parent match')