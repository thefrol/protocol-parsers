"""represents a player block: a div with class='structure__unit'"""
from functools import cached_property

from ..tagminer import TagMiner
from .player import Player

class PlayerBlock(TagMiner):
    @cached_property
    def is_away_team(self):
        return self.has_class('structure__unit--right')
    @property
    def is_home_team(self):
        return not self.is_away_team
    
    @cached_property
    def _structure_title(self)->str:
        """returns title of block
        ex. Основной состав, Запасной состав, Официальные лица"""
        structure_tag=self.find_in_parents(lambda tag: tag.has_class('structure'))
        return structure_tag._find_tag(class_='subtitle').text

    @property
    def is_main(self):
        """returns True if this block has main team players"""
        return 'основной' in self._structure_title.lower()
    
    @property
    def is_bench(self):
        """returns True if this block has bench team players"""
        return 'запасной' in self._structure_title.lower()
    
    @property
    def is_coaches(self):
        """returns True if this block has coaches"""
        return 'официальные' in self._structure_title.lower()
    
    @property
    def is_players(self):
        """returns True if this block has players, and no coaches"""
        return self.is_main or self.is_bench
    
    @property
    def players(self):
        if not self.is_players:
            return []
        player_tags=self._find_all_tags(class_='structure__item')
        return [Player(tag,is_main=self.is_main) for tag in player_tags]
    
    def health_check(self):
        if sum([1 if val else 0 for val in [self.is_bench, self.is_coaches, self.is_main]])!=1:
            #only one of this params must be True
            print(f'player block is corrupted: more one value in bench, main, trainers')

def home_players(block:PlayerBlock):
    return block.is_players and block.is_home_team

def guest_players(block:PlayerBlock):
    return block.is_players and block.is_away_team


class PlayerBlockList(list[PlayerBlock]):
    def where(self, compare_func)-> PlayerBlock:
        return PlayerBlockList(block for block in self if compare_func(block))
    
    @cached_property
    def players(self):
        return sum([block.players for block in self],[])
    
    @cached_property
    def home_players(self):
        return self.where(home_players).players
    
    @cached_property
    def guest_players(self):
        return self.where(guest_players).players
    
