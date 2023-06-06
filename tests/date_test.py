import unittest
from dataclasses import dataclass

from protocol_parsers.mosff.match import MatchPageDate

class MatchTest(unittest.TestCase):
    def test_date(self):
        date='04 ИЮНЯ / ВОСКРЕСЕНЬЕ / 12:30'
        d=MatchPageDate(date)
        self.assertEqual(d.day,4)
        self.assertEqual(d.month,6)
        self.assertEqual(d.week_day,7)
        self.assertIsNone(d.year)
        self.assertEqual(d.hour,12)
        self.assertEqual(d.minute,30)

if __name__ == '__main__':
    unittest.main()
        
