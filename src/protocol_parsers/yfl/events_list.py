from typing import Callable
from functools import cached_property

from ..decorators import trim, to_int, to_int_or_none
from ..regex import Regex

from ..tagminer import TagMiner, TagMinerList
from .funcs import get_player_id

class Event(TagMiner):
    _minute_pattern=r'(?P<minute>\d+)(\+(?P<add>\d+))?\''
    @cached_property
    @to_int
    def minute(self):
        raw_text=self._find_tag('div',class_='timeline__minute').text
        match= Regex(pattern=self._minute_pattern, string=raw_text)
        main_time=int(match.get_group('minute',0))
        add_time=int(match.get_group('add',0))
        return main_time+add_time
    @cached_property
    @to_int_or_none
    def author_id(self):
        """id of author of event, goal and substitutions
        
        for substitutions author id - player went on field"""
        tag=self._find_tag('a',class_='timeline__name')
        relative_url=tag['href']
        return get_player_id(relative_url)
    @cached_property
    @to_int_or_none
    def assist_id(self):
        """id of author of event, goal and substitutions
        for substitutions assist id - player left field"""
        tag=self._find_tag('a',class_='timeline__text')

        # for red cards and so a tags dont have a href
        if tag.is_empty or tag.href is None:
            return None

        relative_url=tag['href']
        return get_player_id(relative_url)
    @cached_property
    @trim
    def raw_text(self):
        return self._find_tag('div',class_='timeline__icon').get_param('title')
        
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




class EventsList(TagMinerList):
    @classmethod
    def from_tags(cls,tags):
        return cls([Event(tag) for tag in tags])

    def get_by_player_id(self, player_id:int):
        return self.__class__([event for event in self if event.author_id==player_id or event.assist_id==player_id])
    
    @property
    def yellow_cards(self):
        return self.count(lambda e: e.is_yellow_card)
    
    @property
    def red_cards(self):
        return self.count(lambda e: e.is_red_card)
                
    @property
    def goals(self):
        return self.count(lambda e: e.is_goal)
    
    @property
    def autogoals(self):
        return self.count(lambda e: e.is_autogoal)
    
    @property
    def penalties(self):
        return self.count(lambda e: e.is_penalty)
    
    @property
    def failed_penalties(self):
        return self.count(lambda e: e.is_missed_penalty)
    
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