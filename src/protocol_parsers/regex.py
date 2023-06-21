import re
from functools import cached_property

def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)

class Regex:
    def __init__(self,pattern, string):
        self._pattern=pattern
        self._string=string
        self._match=None
    @cached_property
    def match(self):
        if self._match is None:
            self._match=re.search(self._pattern,self._string)
            if self._match is None:
                print(f'matching "{self._string}" with "{self._pattern}" returns None' )
        return self._match
    def get_group(self,group:str, default=None):
        if self.match is None:
            return default
        groupdict=self.match.groupdict()
        if group not in self.match.groupdict():
            print(f'returning {default} for group {group}. not found in results')
            return default
        return self.match.group(group) or default
    @property
    def is_ok(self):
        return self.match is not None
    
    @classmethod
    def try_create(cls, pattern, string):
        """returns None if Regex not ok,
        useful for this type of actions
        regex=Regex.try(pattern1,string) or Regex.try(pattern2, string)"""
        new_obj=cls(pattern, string)
        if new_obj.is_ok:
            return new_obj
        else:
            print(f'pattern "{pattern}" failed for string {string}')
            return None

class Regexes:
    """A class for trying multiple regex patterns on one string,
    also can fallback to default values"""
    def __init__(self,string,*patterns):
        self._patterns=patterns
        self._string=string
    @cached_property
    def match(self):
        return first_true([re.search(pattern, self._string) for pattern in self._patterns],default=None)
    def get_group(self,group:str, default=None):
        if self.match is None:
            return default
        groupdict=self.match.groupdict()
        if group not in self.match.groupdict():
            print(f'returning {default} for group {group}. not found in results')
            return default
        return self.match.group(group) or default
    @property
    def is_ok(self):
        return self.match is not None
    
    @classmethod
    def try_create(cls, pattern, string):
        """returns None if Regex not ok,
        useful for this type of actions
        regex=Regex.try(pattern1,string) or Regex.try(pattern2, string)"""
        new_obj=cls(pattern, string)
        if new_obj.is_ok:
            return new_obj
        else:
            print(f'pattern "{pattern}" failed for string {string}')
            return None
        
class Regexes2:
    def __init__(self,string,*patterns):
        self._patterns=patterns
        self._string=string

        for group in self.match.groupdict():
            self.__dict__[group]=self.get_group(group)
    @cached_property
    def match(self):
        return first_true([re.search(pattern, self._string) for pattern in self._patterns],default=None)
    def get_group(self,group:str, default=None):
        if self.match is None:
            return default
        groupdict=self.match.groupdict()
        if group not in self.match.groupdict():
            print(f'returning {default} for group {group}. not found in results')
            return default
        return self.match.group(group) or default
    @property
    def is_ok(self):
        return self.match is not None
    
