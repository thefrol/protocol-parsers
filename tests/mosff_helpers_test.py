import unittest
from datetime import datetime

from protocol_parsers.mosff.match import format_cup_round, format_tournament_year
from protocol_parsers.date import format_season
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

class YflSeasonFormatting(unittest.TestCase):
    def test_old_system(self):
        date=datetime(2023,6,11)
        self.assertEqual(format_season(date),'2022/2023')

        date=datetime(2022,6,11)
        self.assertEqual(format_season(date),'2021/2022')

        date=datetime(2022,7,11)
        self.assertEqual(format_season(date),'2022/2023')

    def test_new_system(self):
        date=datetime(2023,7,11)
        self.assertEqual(format_season(date),'2023')

        date=datetime(2024,7,11)
        self.assertEqual(format_season(date),'2024')

class FormatCupRound(unittest.TestCase):
    def test_ro16(self):
        text='2009 г.р. (ПЛЕЙОФФ). 1/8 финала'
        self.assertEqual(format_cup_round(text),'1/8')
    def test_quaterfinal(self):
        text='2009 г.р. (ПЛЕЙОФФ). Четвертьфинал'
        self.assertEqual(format_cup_round(text),'1/4')
    def test_bad_quaterfinal(self):
        text='2009 г.р. (ПЛЕЙОФФ). Чыетвертьфинал'
        self.assertEqual(format_cup_round(text),'Чыетвертьфинал')
    def test_bad_ro16(self):
        text='2009 г.р. (ПЛЕЙОФФ). 1/7 фsнала'
        self.assertEqual(format_cup_round(text),'1/7 фsнала')

class FormatCupYear(unittest.TestCase):
    def test_cup_2023(self):
        text='Кубок Москвы среди команд спортивных школ 2009, 2010 гг.р. сезон 2023 года'
        self.assertEqual(format_tournament_year(text), 2023)
    def test_cup_2022(self):
        text='Кубок Москвы среди команд спортивных школ 2009, 2010 гг.р. сезон 2022 года'
        self.assertEqual(format_tournament_year(text), 2022)
        text='Кубок Москвы среди команд спортивных школ 2009, 2010 гг.р. сызон 2021 года'
        self.assertEqual(format_tournament_year(text), 2021)
    def test_championship(self):
        text='Первенство Москвы по футболу среди команд спортшкол - Клубная лига 2012 г.р. (сезон 2023)'
        self.assertEqual(format_tournament_year(text), 2023)
        text='Первенство Москвы по футболу среди команд спортшкол - Клубная лига 2012 г.р. (сезон 2024)'
        self.assertEqual(format_tournament_year(text), 2024)



if __name__ == '__main__':
    unittest.main()