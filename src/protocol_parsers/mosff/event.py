import re

class Event:
    """class for working with event html data"""
    regex_pattern=r'(?P<note>.*)(, (?P<minute>\d{1,2}).){1}$'

    def __init__(self, event_html):
        self._event_html=event_html

        self._title=self._event_html['title']
        self._svg_icon_href=self._event_html.svg.use['xlink:href'] # used to check what kind of event it is

        result=re.search(pattern=self.regex_pattern, string=self._title)

        self._minute=result.group('minute')
        self.note=result.group('note')

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
    def minute(self):
        return int(self._minute)
