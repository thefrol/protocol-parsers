from functools import cached_property

from ..tagminer import TagMiner
from ..decorators import to_int
from ..regex import Regexes

class Event(TagMiner):
    """class for working with event html data"""
    @property
    def title(self):
        return self._find_tag(class_="structure__event-desc").text.strip()
    
    @cached_property
    def _regex(self):
        '''a private field for shared use of this regex'''
        regex_pattern=r'(?P<note>.*)(, (?P<minute>\d{1,2}).)$'
        fallback_pattern=r'(?P<note>.*)(, (?P<minute>\d{1,2}).)?$'
        return Regexes(self.title, regex_pattern, fallback_pattern)

    @property
    @to_int
    def minute(self):
        return self._regex.get_group('minute',0)
    
    @property
    def note(self):
        return self._regex.get_group('note','')
    
    @cached_property
    def _icon_href(self):
        return self._find_tag('use').get_param('xlink:href')


    @property
    def is_yellow(self):
        return "#yellow-card" in self._icon_href 
    
    @property
    def is_double_yellow(self):
        """ in mosff second yellow is marked as double card"""
        return "#double-card" in self._icon_href 
    
    @property
    def is_red_card(self):
        return "#red-card" in self._icon_href 
    
    @property
    def is_goal(self):
        return "#goal" in self._icon_href 
    
    @property
    def is_autogoal(self):
        return "#own-goal" in self._icon_href 
    
    @property
    def is_substitute_in(self):
        return "#sub-in" in self._icon_href 
    
    @property
    def is_substitute_out(self):
        return "#sub-out" in self._icon_href 
    

    @property
    def type_(self)->str:
        'returns event type one of the following, goal, autogoal, yellow-card, red-card, sub-in, sub-out, unknown'
        event_type='unknown'
        if self.is_autogoal:
            event_type='autogoal'
        elif self.is_goal:
            event_type='goal'
        elif self.is_yellow:
            event_type='yellow-card'
        elif self.is_double_yellow:
            event_type='yellow-card'
        elif self.is_red_card:
            event_type='red-card'
        elif self.is_substitute_in:
            event_type='sub-in'
        elif self.is_substitute_out:
            event_type='sub-out'
        return event_type

