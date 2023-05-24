"""A test scipt for working with regex in event html blocks"""


text="Симуляция, 17'"

regex_pattern='(?P<note>.*)(, (?P<minute>\d{1,2}).){1}$'

import re

res=re.search(regex_pattern,text)
print(res.group('note'))
print(res.group('minute'))
