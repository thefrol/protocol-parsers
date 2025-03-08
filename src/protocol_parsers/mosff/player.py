from functools import cached_property

from ..tagminer import TagMiner
from ..names import PlayerName, TwoPartName, FioName
from ..decorators import to_int_or_none, trim, trim_or_none, to_int
from .event import Event
from ..regex import Regex


class Player(TagMiner):
    """a class for parsing player data """
    _mosff_prefix='https://mosff.ru'

    def __init__(self, html, is_main):
        super().__init__(html)
        self.is_main=is_main

    @cached_property
    def events(self) -> list[Event]:
        events_htmls=self._find_all_tags(class_='structure__event') or []
        return [Event(html) for html in events_htmls]
    
    @cached_property
    def _img(self):
        """returns a img tag, need for mining name data and photo"""
        return self._find_tag('img')
    
    @cached_property
    def text_name(self):
        "taken from div"
        name_div=self._find_tag('div',class_="structure__name-text")
        return TwoPartName(next(name_div.stripped_strings))

    @property
    def img_alt_name(self)->PlayerName:
        """taken from img alt"""
        return FioName(self._img.get_param('alt'))

    @property
    def name(self)->PlayerName:
        return self.img_alt_name or self.text_name
    
    @property
    def img_url(self):
        return self._img['src']
    
    @property
    def relative_url(self):
        '''a relative link to mosff website with player info'''
        return self._find_tag(class_="structure-name").href
    
    @property
    def full_url(self):
        """a relative link to mosff website with player info"""
        return self._mosff_prefix+self.relative_url
    
    @property
    @to_int_or_none
    def id(self):
        mosff_id_pattern=r'/player/(?P<player_id>\d+)\Z' #TODO to settings file
        return Regex(
            pattern=mosff_id_pattern,
            string=self.relative_url
            ).get_group('player_id')

    
    @property
    @trim
    def number(self):
        return self._find_tag(class_="structure__number").no_verbose.text
    
    @property
    @trim_or_none
    def position(self):
        return self._find_tag(class_="structure__position").no_verbose.text
    
    @property
    def is_capitain(self):
        if self.position is None:
            return False
        return True if '(к)' in self.position else False
    
    @property
    def is_goalkeeper(self):
        if self.position is None:
            return False
        return True if '(вр)' in self.position else False
    
    @property
    def in_at(self):
        """a time player got in
        
        0 - from the start
        None - never played"""
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
            if event.is_red_card or event.is_double_yellow:
                return event.minute
        return None # not came out or playted till end
    
    def time_played(self, match_time:int):
        """time on field
        
        None - played till end or never played"""
        if self.in_at is not None:
            if self.out_at:
                return self.out_at-self.in_at
            else: # played till end
                return match_time-self.in_at
        else: # not played
            return 0
        
    def played_interval(self, match_time:int): #not used
        """returns interval when player was on the field [from, to] or None if player not played"""
        start=None
        end=None
        if self.in_at is not None:
            start=self.out_at
            if self.out_at:
                end=self.in_at
            else: # played till end
                end=match_time
            return [start,end]
        else: # not played
            return None 
        
    def was_on_field(self, minute):
        if self.in_at is None:
            return False # player hasnt played
        else:
            if minute>= self.in_at:
                if self.out_at is None:
                    return True # plyed till end
                if minute < self.out_at:
                    return True # was changed
                else:
                    return False
            else:
                return False

    
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
    def red_cards(self):
        for event in self.events:
            if event.is_red_card:
                return 1
        return 0
    
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
