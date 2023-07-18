from ..decorators import trim, to_int, to_int_or_none
from ..regex import Regex

@to_int_or_none
def get_player_id(player_relative_url:str):
    return Regex(pattern=r'/player/(?P<player_id>\d+)',
          string=player_relative_url).get_group('player_id')