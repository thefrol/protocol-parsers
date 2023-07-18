from typing import Callable
from functools import cached_property,cache
import datetime


from protocol_parsers.date import PageDate
from ..decorators import trim, to_int, to_int_or_none
import re
from ..regex import Regex, Regexes2

from ..tagminer import TagMiner
from .funcs import get_player_id
from .events_list import Event, EventsList
from .player import MatchProtocolTabPlayer
from .team import Team

    
   
class Tournament(TagMiner):
    @cached_property
    @trim
    def name_raw(self)->str:
        return self._find_tag('a',class_='match-promo__tournament').text
    @property
    def name(self):
        return self.name_raw.split(' ')[0]
    @cached_property
    def relative_url(self):
        return self._find_tag('a',class_='match-promo__tournament')['href']
    @cached_property
    @to_int
    def id(self):
        res=Regexes2(self.relative_url,r'/tournament/(?P<tournament_id>\d+)').tournament_id
        return res
    
class PromoTeam(TagMiner):
    _team_pattern=r'/tournament/(?P<tournament_id>\d+)/teams/application\?team_id=(?P<team_id>\d+)'
    @property
    @trim
    def name(self):
        return self.get_param('title')
    @property
    @trim
    def relative_url(self):
        return self.get_param('href')
    @property
    def _team_regex(self):
        return Regex(pattern=self._team_pattern,string=self.relative_url)
    @property
    @to_int
    def id(self):
        return self._team_regex.get_group('team_id')
    @property
    @to_int
    def tournament_id(self):
        return self._team_regex.get_group('tournament_id')
    

class PromoDate(PageDate):
    @property
    def year(self):
        """returning current year"""
        return datetime.datetime.now().year
    @property
    def _date_pattern(self):
        return r'(?P<day>\d+) (?P<month>\w+) / (?P<week_day>\w+) / (?P<hour>\d+):(?P<minute>\d+)'   

class Promo(TagMiner):
    @cached_property
    @trim
    def score_raw_text(self)->str:
        return self._find_tag('div',class_='match-promo__score-main').text.replace(' ','')
    @cached_property
    def scores(self)-> list[str]:
        return self.score_raw_text.split(':')
    @property
    @to_int
    def home_score(self)->int:
        return self.scores[0]
    
    @property
    @to_int
    def guest_score(self)->int:
        return self.scores[1]
    
    @cached_property
    def home_team(self):
        wrapper=self._find_tag('div', class_='match-promo__team-text--right') ## the left-text means align left so right team aligns to left. need to change to something more logical
        team_tag=wrapper.a
        return PromoTeam(team_tag)

    @cached_property
    def guest_team(self):
        wrapper=self._find_tag('div', class_='match-promo__team-text--left') ## the left-text means align left so right team aligns to left. need to change to something more logical
        team_tag=wrapper.a
        return PromoTeam(team_tag)

    @cached_property
    def tournament(self):
        return Tournament(self._find_tag('div',class_='match-promo__tournament-wrapper'))
    
    @property
    def date(self)->PromoDate:
        date_tag=self._find_tag('div',class_='match-promo__date-time')
        if date_tag is not None:
            return PromoDate(date_tag.text)
        else:
            return None

class MatchPage(TagMiner):
    def _get_team(self, team_from) -> Team:
        
        """retuns a dataclass with match protocols tags
        htmls with substitutions, names from page tab protocol
        
        team_from=home|guest"""
        positive_values=['guest','home']
        if team_from in positive_values:
            tag=self._html.find('div',{'class':'match-protocol'})
            return Team(tag,'left' if team_from == 'home' else 'right',parent_match=self)
        else:
            raise ValueError(f'team_from must be one of {positive_values}')
        
    @property
    def time_played(self):
        """returns match duration based on a tournament name"""
        if 'ЮФЛ-3' in self.promo.tournament.name:
            return 80
        return 90
    
    @cached_property
    def home_team(self)-> Team:
        return self._get_team('home')
    
    @cached_property
    def guest_team(self) -> Team:
        return self._get_team('guest')
    
    @cached_property
    def promo(self):
        return Promo(self._find_tag('section',class_='match-promo'))
    
    @property
    def score(self):
        return self.promo.score
    
    @cached_property
    def events(self) -> EventsList:
        tags=self._find_all_tags('li',class_='vertical-timeline__event-item')
        return EventsList.from_tags(tags)
    
    def find_player_by_id(self, id_)->MatchProtocolTabPlayer:
        for player in self.guest_team.players + self.home_team.players:
            if player.id== id_:
                return  player
        return None
    
    def find_player_by_name(self, name)->MatchProtocolTabPlayer:
        for player in self.guest_team.players + self.home_team.players:
            if player.name== name:
                return  player
        return None
