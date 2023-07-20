from functools import cached_property,cache

from ..decorators import trim, to_int, to_int_or_none

from ..tagminer import TagMiner
from .funcs import get_player_id

from .events_list import Event, EventsList
import protocol_parsers.yfl as yfl


class MatchProtocolTabPlayer(TagMiner):
    def __init__(self, html):
        super().__init__(html)
        self.events: EventsList=None
        import protocol_parsers.yfl.team as team ##TODO how to put it to top of file?
        self.team:team.Team=None
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
        return not capitain_tag.is_empty
    
    @cached_property
    def is_substitute(self):
        """returns true if this player was a substitute, false if was a main player"""
        return self.find_in_parents(lambda tag: tag.has_class('match-protocol__substitutes')) is not None
    @property
    def is_main_player(self):
        return not self.is_substitute
    
    @property 
    def sub_in_event(self):
        """returns a event, when player subbed in
        None if played from start"""
        if self.is_main_player or not self.has_played:
            return None
        else:
            sub_event=self.events.find_sub_in(self.id)
            if sub_event is None:
                print('substitution event failure')
                return None
            return sub_event
        
    @property
    def sub_from_id(self):
        """returns id of player who was subbed by this player"""
        if self.sub_in_event is not None:
            return self.sub_in_event.assist_id
        else:
            return None
            
        
    @property
    def sub_out_event(self):
        """returns a player id, who substituted this player
        None if never substituted"""
        sub_event=self.events.find_sub_out(self.id)
        if sub_event is None:
            return None
        return sub_event

    @property
    def sub_to_id(self):
        """returns id of player who subbed this player"""
        if self.sub_out_event is not None:
            return self.sub_out_event.author_id
        else:
            return None   
    
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
        if self.played_till_end:
            return minute>=self.time_in #in case goal time was later than match ended or at last minute
        else:
            return minute>=self.time_in and minute<self.time_out
        
                
    @property
    def missed_goals(self):
        def goals_when_on_field(event:Event):
            return (event.is_goal or event.is_penalty) and self.was_on_the_field_on(event.minute) 
        def autogoals_when_on_field(event:Event):
            return event.is_autogoal and self.was_on_the_field_on(event.minute)
        
        if not self.is_goalkeeper:
            return 0
        
        game_goals_count=self.team.opposing_team.events.count(goals_when_on_field)
        autogoals_count=self.team.events.count(autogoals_when_on_field)
        
        return game_goals_count+autogoals_count
    
    @property
    def goals(self):
        return self.events.goals + self.events.penalties
        
    def __str__(self):
        return f'player: {self.number} {self.name} {self.relative_url}'
