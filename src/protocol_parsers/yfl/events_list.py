from typing import Callable
from functools import cached_property

from ..decorators import trim, to_int, to_int_or_none
from ..regex import Regex

from ..tagminer import TagMiner
from .funcs import get_player_id

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
        """id of author of event, goal and substitutions
        
        for substitutions author id - player went on field"""
        relative_url=self._find_tag('a',class_='vertical-timeline__event-author')['href']
        return get_player_id(relative_url)
    @cached_property
    @to_int_or_none
    def assist_id(self):
        """id of author of event, goal and substitutions
        for substitutions assist id - player left field"""
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