import unittest

from protocol_parsers import MosffParser

URL='https://mosff.ru/match/34858'

class MatchWithAutoGoals(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol:MosffParser=MosffParser(URL)
        self.match=self.protocol._match
        return super().setUp()
    def test_scores(self):
        self.assertEqual(self.match.home_score,7,'Home score not right')
        self.assertEqual(self.match.guest_score,2,'guest score error')
    def test_ids(self):
        self.assertEqual(self.match.guest_team_id,2051,'guest team id failed')
        self.assertEqual(self.match.home_team_id,2044,'home team id failed')
        

if __name__ == '__main__':
    unittest.main()