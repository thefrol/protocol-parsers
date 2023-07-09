from typing import Callable
from functools import cached_property,cache
import datetime


from protocol_parsers.date import PageDate
from ..decorators import trim, to_int, to_int_or_none
import re
from ..regex import Regex, Regexes2

from ..tagminer import TagMiner
from .player_page import PlayerPage
from .team_page import TeamPage

@to_int_or_none
def get_player_id(player_relative_url:str):
    return Regex(pattern=r'/player/(?P<player_id>\d+)',
          string=player_relative_url).get_group('player_id')
    





class MatchProtocolTabPlayer(TagMiner):
    def __init__(self, html):
        super().__init__(html)
        self.events: EventsList=None
        self.team:Team=None
    @cached_property
    @trim
    def number(self):
        return self._find_tag('span',class_='match-protocol__member-number').text
    @cached_property
    @trim
    def raw_amplua(self):
        amplua_tag=self._find_tag('span',class_='match-protocol__member-amplua')
        return amplua_tag.text if amplua_tag is not None else ''
    @cached_property
    @trim
    def name(self):
        return self._find_tag('a',class_='match-protocol__member-name').text
    @cached_property
    def relative_url(self):
        return self._find_tag('a',class_='match-protocol__member-name')['href']
    
    @cached_property
    @to_int
    def id(self):
        return get_player_id(self.relative_url)
    
    @property
    def is_capitain(self):
        capitain_tag=self._find_tag('span',class_='match-protocol__member-captain')
        return capitain_tag is not None
    
    @cached_property
    def is_substitute(self):
        """returns true if this player was a substitute, false if was a main player"""
        return self.find_in_parents(lambda tag: 'match-protocol__substitutes' in tag['class'])
    @property
    def is_main_player(self):
        return not self.is_substitute
    
    @property 
    def is_goalkeeper(self):
        return 'вр' in self.raw_amplua.lower()
    
    @property
    def time_in(self):
        """A minute player entered field,
        None if never played"""
        if self.is_main_player:
            return 0
        else:
            subsitute_event=self.events.find_sub_in(self.id)
            if subsitute_event is None:
                return None # never substituted
            else:
                return subsitute_event.minute
            
    @property
    def played_till_end(self):
        subsitute_event=self.events.find_sub_out(self.id)
        return subsitute_event is None and not self.was_sent_off
            
    @property
    def time_out(self):
        """A minute player left field"""
        match_duration=self.team._parent_match.time_played
        subsitute_event=self.events.find_sub_out(self.id)
        if subsitute_event is None and not self.was_sent_off:
            return self.team._parent_match.time_played if self.has_played else None# never substituted
        else:
            if self.was_sent_off:
                yellow_cards_cout=0
                time_sent_off=None
                for event in self.events:
                    if event.is_yellow_card:
                        yellow_cards_cout=yellow_cards_cout+1
                        if yellow_cards_cout>1:
                            time_sent_off=event.minute
                            return time_sent_off
                    if event.is_red_card:
                        time_sent_off=event.minute
                        return time_sent_off
                print(f'error with sent off time: sent off event not found {self}')
                return time_sent_off
            else:
                return subsitute_event.minute
        
    @property
    def time_on_field(self):
        match_duration=self.team._parent_match.time_played
        if self.time_in is None:
            return 0
        else:
            if self.has_played:
                return self.time_out-self.time_in
            else:
                print('time_on_field business error')
                return match_duration # if time out=None will substract 0
        
    @property
    def has_played(self):
        return self.time_in is not None
    
    @property
    def was_sent_off(self):
        """returns true is player was banned from field^ red card or two yellow cards"""
        return self.events.red_cards>0 or self.events.yellow_cards >1
    
   
    def was_on_the_field_on(self, minute):
        """returns true if played was on the field in this minute"""
        if not self.has_played:
            return False
        return minute>=self.time_in and minute<self.time_out
        
                
    @property
    def missed_goals(self):
        if not self.is_goalkeeper:
            return 0
        game_goals_count=self.team.opposing_team.events._count(lambda event: (event.is_goal or event.is_penalty) and self.was_on_the_field_on(event.minute) )
        autogoals_count=self.team.events._count(lambda event: event.is_autogoal and self.was_on_the_field_on(event.minute) )
        return game_goals_count+autogoals_count
    
    @property
    def goals(self):
        return self.events.goals + self.events.penalties
        
    def __str__(self):
        return f'player: {self.number} {self.name} {self.relative_url}'

class Team:
    """A class for working with protocol tab player names and others
    location may be left or right
    left team is the home team, rigth is guest team"""
    def __init__(self, html, location:str,parent_match:'MatchPage'):
        self._html=html
        self._location=location
        self._parent_match=parent_match
    @cached_property
    def name(self):
        """returns left or right team name"""
        return self._html.find('a',{'class':f'match-protocol__team-name--{self._location}'})['title'] #TODO failures#
    @cached_property
    def players(self)-> list[MatchProtocolTabPlayer]:
        result=[]
        tags=self._html.find_all('li',{'class':f'match-protocol__member--{self._location}'}) #TODO failures#
        for tag in tags:
            new_player=MatchProtocolTabPlayer(tag)
            new_player.events=self._parent_match.events.get_by_player_id(new_player.id)
            new_player.team=self
            result.append(new_player)
        return result
    
    @property
    def opposing_team(self):
        if self is self._parent_match.home_team:
            return self._parent_match.guest_team
        else:
            return self._parent_match.home_team
        
    @cached_property
    def events(self)->'EventsList':
        array=sum([player.events for player in self.players],start=EventsList())
        unique=set(array)
        return EventsList(unique)

    
class Event(TagMiner):
    _minute_pattern=r'(?P<minute>\d+)\''
    @cached_property
    @to_int
    def minute(self):
        raw_text=self._find_tag('div',class_='vertical-timeline__event-minute').text
        return Regex(pattern=self._minute_pattern, string=raw_text).get_group('minute',0)
    @cached_property
    @to_int_or_none
    def author_id(self):
        """id of author of event, goal and substitutions"""
        relative_url=self._find_tag('a',class_='vertical-timeline__event-author')['href']
        return get_player_id(relative_url)
    @cached_property
    @to_int_or_none
    def assist_id(self):
        """id of author of event, goal and substitutions"""
        tag=self._find_tag('a',class_='vertical-timeline__event-assist')
        if tag is None:
            return None
        relative_url=tag['href']
        return get_player_id(relative_url)
    @cached_property
    @trim
    def raw_text(self):
        tag=self._find_tag('div',class_='event-item')
        if tag is None:
            return None
        else:
            return tag.get('title')
        
    def __str__(self):
        return f"event {self.author_id} {self.assist_id} {self.raw_text}"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def is_yellow_card(self):
        return self.raw_text.lower()=='жёлтая карточка'
    
    @property
    def is_red_card(self):
        return self.raw_text.lower()=='красная карточка'
    
    @property
    def is_goal(self):
        return self.raw_text.lower()=='гол'

    @property
    def is_penalty(self):
        return self.raw_text.lower()=='пенальти'
    
    @property
    def is_failed_penalty(self):
        return self.raw_text.lower()=='незабитый пенальти'

    @property
    def is_autogoal(self):
        return self.raw_text.lower()=='автогол'
    
    @property
    def is_substitute(self):
        return self.raw_text.lower()=='замена'




class EventsList(list[Event]):
    @classmethod
    def from_tags(cls,tags):
        return cls([Event(tag) for tag in tags])

    def get_by_player_id(self, player_id:int):
        return self.__class__([event for event in self if event.author_id==player_id or event.assist_id==player_id])
    
    def _count(self, comparer:Callable[[Event],bool]):
        """counts how many times is true camparer for each event"""
        return sum(comparer(event) for event in self)
    
    @property
    def yellow_cards(self):
        return self._count(lambda e: e.is_yellow_card)
    
    @property
    def red_cards(self):
        return self._count(lambda e: e.is_red_card)
                
    @property
    def goals(self):
        return self._count(lambda e: e.is_goal)
    
    @property
    def autogoals(self):
        return self._count(lambda e: e.is_autogoal)
    
    @property
    def penalties(self):
        return self._count(lambda e: e.is_penalty)
    
    @property
    def failed_penalties(self):
        return self._count(lambda e: e.is_missed_penalty)
    
    def find_sub_out(self, player_id:int):
        """returns event when current player left field"""
        for event in self:
            if event.is_substitute:
                if event.assist_id==player_id:
                    return event
        return None
    
    def find_sub_in(self, player_id:int):
        """returns event when current player entered field"""
        for event in self:
            if event.is_substitute:
                if event.author_id==player_id:
                    return event
        return None
    
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