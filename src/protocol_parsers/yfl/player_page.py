import re
from functools import cached_property

from . import TagMiner
from ..names import FioName
from ..date import PageDate
from ..decorators import trim

class YflPlayerDate(PageDate):
    _date_pattern=r'(?P<date_string>(?P<day>\d+) (?P<month>\w+) (?P<year>\d+))'

    @property
    def is_healthy(self):
        return self.day is not None and self.month is not None and self.year is not None

class PlayerPage(TagMiner):
    @cached_property
    @trim
    def name_raw(self):
        return self._find_tag('p',class_='player-promo__name').text
    @cached_property
    def name(self):
        return FioName(self.name_raw)
    @cached_property
    def date_raw(self):
        wrapper_tag=TagMiner(self._find_tag('p','player-promo__item--birth'))
        value_tag=wrapper_tag._find_tag('span','player-promo__value')
        return value_tag.text
    @cached_property
    def birth_date(self):
        return YflPlayerDate(self.date_raw)
    