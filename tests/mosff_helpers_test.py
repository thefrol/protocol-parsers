import unittest

from protocol_parsers.mosff.match import format_cup_round
from protocol_parsers.mosff.match import MatchPageDate

class DateTest(unittest.TestCase):
    def test_date(self):
        date='04 ИЮНЯ / ВОСКРЕСЕНЬЕ / 12:30'
        d=MatchPageDate(date)
        self.assertEqual(d.day,4)
        self.assertEqual(d.month,6)
        self.assertEqual(d.week_day,7)
        self.assertIsNone(d.year)
        self.assertEqual(d.hour,12)
        self.assertEqual(d.minute,30)

class FormatCupName(unittest.TestCase):
    def test_ro16(self):
        text='2009 г.р. (ПЛЕЙОФФ). 1/8 финала'
        self.assertEqual(format_cup_round(text),'1/8')
    def test_quaterfinal(self):
        text='2009 г.р. (ПЛЕЙОФФ). Четвертьфинал'
        self.assertEqual(format_cup_round(text),'1/4')

if __name__ == '__main__':
    unittest.main()