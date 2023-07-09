import re
from abc import abstractmethod

from .decorators import trim, to_int, lower, to_int_or_none

from datetime import datetime

class PageDate:
    """a class for parsing string from MAtch Page
    date is showed is such style
    04 ИЮНЯ / ВОСКРЕСЕНЬЕ / 12:30"""

    _months_dict={
        'янв':1,
        'фев':2,
        'мар':3,
        'апр':4, 
        'май':5, 'мая':5, 
        'июн':6, 
        'июл':7, 
        'авг':8, 
        'сен':9, 
        'окт':10, 
        'ноя':11, 
        'дек':12}
    
    _weekday_list=['','пон','вто','сре','чет','пят','суб','вос']
            
    def __init__(self, date_string):
        self._date_string=date_string
        if date_string is None:
            self._regex_match=None
        else:
            self._regex_match=re.search(self._date_pattern,self._date_string) #TODO use Regex class
    
    @property
    @abstractmethod
    def _date_pattern(self):
        return ''

    def from_regex_group(self,group_name:str):
        if self._regex_match is None:
            print(f'date string "{self._date_string}" is not matching regex pattern"{self._date_pattern}"')
            return None
        else:
            if group_name not in self._regex_match.groupdict():
                print(f'cant find group {group_name} in string "{self._date_string}" through regex pattern "{self._date_pattern}"')
                return None
            else:
                return self._regex_match.group(group_name)

    @property
    @to_int_or_none
    def day(self):
        return self.from_regex_group('day')
    
    @property
    @lower
    def month_string(self):
        return self.from_regex_group('month')
    
    @property
    def month(self):
        if self.month_string is None:
            print('month string is None')
            return None
        if self.month_string[:3]:
            return self._months_dict[self.month_string[:3]]
        else:
            print(f'cant get month from {self.month_string}')
            return None
        
    @property
    @to_int_or_none
    def year(self):
        return self.from_regex_group('year')
    
    @property
    @lower
    def week_day_string(self):
        return self.from_regex_group('week_day')
    
    @property
    def week_day(self):
        if self.week_day_string is None:
            print('week day string is None')
            return None
        try:
            return self._weekday_list.index(self.week_day_string[:3])
        except ValueError:
            print(f'cant get month from {self.week_day_string}')
            return None

    @property
    @to_int_or_none
    def hour(self):
        return self.from_regex_group('hour')
    
    @property
    @to_int_or_none
    def minute(self):
        return self.from_regex_group('minute')
    
    @property
    def as_datetime(self):
        return datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute)
    
def format_season(date):
        def is_old_system(date_):
            """до июля 2023 года мы играли в система осень-весна, проверяем так ли это"""
            return date_<datetime(2023,7,1)
        if is_old_system(date):
            if date.month>=7:
                # текущий_год/следующий_год
                return f'{date.year}/{date.year+1}'
            else:
                #предыдущий_год/следущий_год
                return f'{date.year-1}/{date.year}'
        else:
            return f'{date.year}'