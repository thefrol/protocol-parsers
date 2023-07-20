import re
from datetime import datetime
from ..decorators import trim, to_int, to_int_or_none
from ..exceptions import TeamNotFound
from ..regex import Regex, Regexes
from ..tagminer import TagMiner

@trim
def format_cup_round(stage_name): #TODO - to separate class
    #1 try find known patterns
    cup_text_variations={
        '1/256':'1/256',
        '1/128':'1/128',
        '1/64':'1/64',
        '1/32':'1/32',
        '1/16':'1/16',
        '1/8':'1/8',
        '1/4':'1/4',
        '1/2':'1/2',
        'Четвертьфинал':'1/4',
        'Полуфинал':'1/2',
        'Финал':'финал',
    }
    for key in cup_text_variations:
        if key in stage_name:
            return cup_text_variations[key]
        
    #2 fallback to regexp
    _pattern='\.(?P<stage_name>[^.]+)\Z'
    match=Regex(_pattern,stage_name)
    if match.is_ok:
        return match.get_group('stage_name')
    
    #3 return full name
    return stage_name

class Tournament(TagMiner):
    @property
    @trim
    def raw_name(self):
        return self._find_tag(class_='match__tournament').text
    
    @property
    def relative_url(self):
        return self._find_tag(class_='match__tournament').href
    
    @property
    def url(self):
        return 'https://mosff.ru'+self.relative_url
    
    @property
    @to_int_or_none
    def id(self):
        return Regex(
            pattern=r'/tournament/(?P<tournament_id>\d+)\Z',
            string=self.relative_url
        ).get_group('tournament_id')

        
    @property
    def is_cup(self):
        '''returns True if match played in cup'''
        return 'кубок' in self.raw_name.lower()
        
    @property
    @to_int_or_none
    def year(self) -> int:
        """year when tournament hosted ex. 2023, 2024
        tries to extract year of tournament from name and fallbacks to current year"""
        main_pattern=r'\(.*(?P<tournament_year>\d{4})\)'
        fallback_pattern=r'[с|С]езон (?P<tournament_year>\d{4})'
        lastchance_pattern=r'(?P<tournament_year>\d{4}) год.{1,5}'

        m=Regexes(self.raw_name,
                   main_pattern,
                   fallback_pattern,
                   lastchance_pattern)
        
        return m.get_group('tournament_year',default=datetime.now().year)
    
    @property
    @to_int_or_none
    def team_year(self):
        '''returns team year from tournament title if possible,
        otherwise return None'''
        return Regex(
            pattern=r'(?P<team_year>\d+) +г.р.',
            string=self.name
            ).get_group('team_year')

           
    @property
    def round(self):
        """Return round number from the tournament
        6 тур - returns 6
        
        1/8 кубка - 1/8"""

        stage_text=self._find_tag(class_='match__round').text
        if self.is_cup:
            return format_cup_round(stage_name=stage_text)
        else:
            return Regex(
                pattern=r'(?P<round_number>\d)+ тур',
                string=stage_text
            ).get_group('round_number')