from ..decorators import trim
from .event import Event

class PlayerName:
    """a players name can consist of 3 parts
    fist name - optional
    middle name - optional
    last name - required"""
    def __init__(self, name_text:str):
        self._name_text=name_text
        self._strings=name_text.split(' ')
    @property
    def names_count(self):
        '''returns count of names Иванов Иван - 2, Иванов иван иванович -3'''
        return len(self._strings)
    @property
    def first_name(self):
        pass
    @property
    def middle_name(self):
        pass
    @property
    def last_name(self):
        pass

class ImgAltName(PlayerName):
    @property
    @trim
    def first_name(self):
        if self.names_count>=2:
            return self._strings[1]
        else:
            return None
    @property
    @trim
    def middle_name(self):
        if self.names_count>2:
            return self._strings[2]
        else:
            return None
    @property
    @trim
    def last_name(self):
        return self._strings[0]

class DivName(PlayerName):
    @property
    @trim
    def first_name(self):
        if self.names_count>1:
            return self._strings[1]
        else:
            return None
    @property
    @trim
    def middle_name(self):
        return None
    @property
    @trim
    def last_name(self):
        return self._strings[0]    


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
        return DivName(next(name_div.stripped_strings))

    @property
    def img_alt_name(self)->PlayerName:
        """taken from img alt"""
        return ImgAltName(self._img['alt'])

    @property
    def name(self)->PlayerName:
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
            if event.is_red_card or event.is_double_yellow:
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
