"""
need to know
names like a, div, li, ul represents a html tag and its info within python code

self.divs_with_names implies a collection of div tags, that stored names
"""


import re
from datetime import datetime
from functools import cached_property, cache

from protocol_parsers.mosff.promo import Promo


from .team import Team
from .player_block import PlayerBlock,PlayerBlockList
from ..date import PageDate
from ..decorators import trim, to_int
from ..exceptions import TeamNotFound
from ..regex import Regex, Regexes
from ..tagminer import TagMiner

@trim
def format_cup_round(stage_name):
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

@to_int
def format_tournament_year(tournament_name):
        """tryes to extract year of tournament from name and fallbacks to current year"""
        main_pattern=r'\(.*(?P<tournament_year>\d{4})\)'
        fallback_pattern=r'[с|С]езон (?P<tournament_year>\d{4})'
        lastchance_pattern=r'(?P<tournament_year>\d{4}) год.{1,5}'

        m=Regexes(tournament_name,
                   main_pattern,
                   fallback_pattern,
                   lastchance_pattern)
        
        return m.get_group('tournament_year',default=datetime.now().year)
        
class MatchPageDate(PageDate):
    @property
    def _date_pattern(self):
        return r'(?P<day>\d+) (?P<month>\w+) / (?P<week_day>\w+) / (?P<hour>\d+):(?P<minute>\d+)'
    

class Match(TagMiner): #TODO extract a promo block
    """
    A class for interacting with html data
    its like a data object, gets a raw hml
    has properties and functions to return
    players, match data, score and others
    """

    round_pattern=r'(?P<round_number>\d)+ тур'
    team_year_pattern=r'(?P<team_year>\d+) +г.р.'

    #_team_id_pattern=r'/team/(?P<team_id>\d+)\Z'
    _tournament_id_pattern=r'/tournament/(?P<tournament_id>\d+)\Z'


    def __init__(self, html_text, parser='html.parser'):
        super().__init__(html_text)
        _soup=self._html

        self.a_with_round=_soup.find("a", {"class":"match__round"})
        self.a_with_tournament=_soup.find("a", {"class":"match__tournament"})


    @cached_property
    def promo(self):
        return Promo(self._find_tag('section',class_='match'))
    
    @cached_property
    def player_blocks(self):
        block_tags=self._find_all_tags(class_='structure__unit')
        return PlayerBlockList([PlayerBlock(block) for block in block_tags])

 
    @cached_property
    def home_team(self):
        return Team(self.player_blocks.home_players)
    
    @cached_property
    def guest_team(self):
        return Team(self.player_blocks.guest_players)
    
    @property
    def teams(self):
        'returns a list of Team objects: home+guest team'
        return [self.home_team, self.guest_team]
    
    @cache
    def get_opposing_team(self, for_team:Team):
        'returns opposing team of for_team'
        for team in self.teams:
            if team is not for_team:
                return team
        print('cant find opposing team')
        return None

    @property
    def date(self):
        date_text=self._find_tag(class_='match__date').text
        return MatchPageDate(date_text)
    
    @property
    def round(self):
        """Return round number from the tournament
        6 тур - returns 6
        
        1/8 кубка - 1/8"""

        stage_text=self.a_with_round.text
        if self.tournament_is_cup:
            return format_cup_round(stage_name=stage_text)
        else:
            m=re.search(self.round_pattern, self.a_with_round.text)
            if m:
                return m.group('round_number')
            else:
                return None
        
    @property
    @trim
    def tournament(self):
        return self.a_with_tournament.text
    
    @property
    def tournament_relative_url(self):
        return self.a_with_tournament['href']
    
    @property
    def tournament_url(self):
        return 'https://mosff.ru'+self.tournament_relative_url
    
    @property
    def tournament_id(self):
        m=re.fullmatch(self._tournament_id_pattern,self.tournament_relative_url)
        if m:
            return int(m.group('tournament_id'))
        else:
            print('cant parse tournament id')
            return None
        
    @property
    def tournament_is_cup(self):
        '''returns True if match played in cup'''
        return 'кубок' in self.tournament.lower()
        
    @property
    def tournament_year(self) -> int:
        """year when tournament hosted ex. 2023, 2024"""
        return format_tournament_year(self.tournament)

    @cached_property
    @to_int
    def team_year(self) ->int:
        """year of born players ex. 2013, 2014"""
        m=re.search(self.team_year_pattern,self.tournament)
        if m is None:
            print(f'cant find team year in tournament title "{self.tournament}", falling back to year of teams. ')
            new_try=self.promo.home_team.year or self.promo.guest_team.year
            if new_try is None:
                print('year in teams cant be found')
            return new_try
            
        else:
            try:
                return int(m.group('team_year'))
            except Exception as e:
                print(f'cant convert team year to int:{e}')
                return None
        
    def find_by_name(self, first_name, last_name):
        '''finds first player by name
        searches home team first'''
        return self.home_team.find_player_by_name(first_name,last_name) or self.guest_team.find_player_by_name(first_name,last_name)


