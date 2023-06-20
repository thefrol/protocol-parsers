import re

from ..decorators import to_int
from ..regex import Regex, Regexes

class Event:
    """class for working with event html data"""
    regex_pattern=r'(?P<note>.*)(, (?P<minute>\d{1,2}).)$'
    fallback_pattern=r'(?P<note>.*)(, (?P<minute>\d{1,2}).)?$'

    def __init__(self, event_html):
        self._event_html=event_html

        self._title=self._event_html['title']
        self._svg_icon_href=self._event_html.svg.use['xlink:href'] # used to check what kind of event it is

        _regex:Regexes=Regexes(self._title, self.regex_pattern, self.fallback_pattern)
        self.note=_regex.get_group('note','')
        self._minute=_regex.get_group('minute',0)
    
    @property
    @to_int
    def minute(self):
        return self._minute

    @property
    def is_yellow(self):
        return "#yellow-card" in self._svg_icon_href 
    
    @property
    def is_double_yellow(self):
        """ in mosff second yellow is marked as double card"""
        return "#double-card" in self._svg_icon_href 
    
    @property
    def is_red_card(self):
        return "#red-card" in self._svg_icon_href 
    
    @property
    def is_goal(self):
        return "#goal" in self._svg_icon_href 
    
    @property
    def is_autogoal(self):
        return "#own-goal" in self._svg_icon_href 
    
    @property
    def is_substitute_in(self):
        return "#sub-in" in self._svg_icon_href 
    
    @property
    def is_substitute_out(self):
        return "#sub-out" in self._svg_icon_href 
    

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

