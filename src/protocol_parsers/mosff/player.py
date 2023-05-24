from ..decorators import trim
from .event import Event

class Player:
    """a class for parsing player data """
    def __init__(self, player_html, is_main):
        self._player_html=player_html

        self._img=player_html.img
        self._number_div=self._player_html.find('div',{'class':"structure__number"})
        self._position_div=self._player_html.find('div',{'class':"structure__position"})

        self.is_main=is_main

        self._events_htmls=self._player_html.find_all('li',{'class':"structure__event"}) or [] # so it wont be none
        self.events=[Event(html) for html in self._events_htmls]
    
    
    @property
    def text_name(self):
        "taken from div"
        name_div=self._player_html.find('div',{'class':"structure__name-text"})
        return next(name_div.stripped_strings)

    @property
    def img_alt_name(self):
        """taken from img alt"""
        return self._img['alt']

    @property
    def name(self):
        return self.img_alt_name or self.text_name
    
    @property
    def img_url(self):
        return self._img['src']
    
    @property
    @trim
    def number(self):
        return self._number_div.text
    
    @property
    def is_capitain(self):
        if self._position_div is None:
            return False
        return True if '(к)' in self._position_div.text else False
    
    @property
    def is_goalkeeper(self):
        if self._position_div is None:
            return False
        return True if '(вр)' in self._position_div.text else False
    
    @property
    def in_at(self):
        """a time player got in"""
        if self.is_main:
            return 0
        else:
            for event in self.events:
                if event.is_substitute_in:
                    return event.minute
        return None # not played
    
    @property
    def out_at(self):
        """a time player got out"""
        for event in self.events:
            if event.is_substitute_out:
                return event.minute
        return None # not came out or playted till end
    
    def time_played(self, match_time:int):
        """time on field"""
        if self.in_at is not None:
            if self.out_at:
                return self.out_at-self.in_at
            else: # played till end
                return match_time-self.in_at
        else: # not played
            return 0

    
    @property
    def yellow_cards(self):
        count=0
        for event in self.events:
            if event.is_double_yellow:
                return 2
            if event.is_yellow:
                count=1
        return count
    
    @property
    def goals(self):
        return sum([1 if event.is_goal else 0 for event in self.events])
    
    @property
    def autogoals(self):
        return sum([1 if event.is_autogoal else 0 for event in self.events])

    
    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'[{self.number}] {self.name}{" (к)" if self.is_capitain else ""}{" (в)" if self.is_goalkeeper else ""}{" "+"Ж"*self.yellow_cards if self.yellow_cards>0 else ""}{" "+"Г"*self.goals if self.goals>0 else ""}{" "+"А"*self.autogoals if self.autogoals>0 else ""} t={self.time_played(80)}'
