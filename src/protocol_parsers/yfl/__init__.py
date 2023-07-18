from typing import Callable
from functools import cached_property,cache
import datetime
import re

from ..decorators import trim, to_int, to_int_or_none
from ..regex import Regex, Regexes2
from ..tagminer import TagMiner

from protocol_parsers.date import PageDate
from .match import MatchPage
from .team_page import TeamPage
#from .player import MatchProtocolTabPlayer
#from .funcs import get_player_id
#from .events_list import Event, EventsList
from .player_page import PlayerPage
from .team import Team
    






    
