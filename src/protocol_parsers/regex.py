import re
class Regex:
    def __init__(self,pattern, string):
        self._pattern=pattern
        self._string=string
        self._match=None
    @property
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
