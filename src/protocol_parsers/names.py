from .decorators import trim

class PlayerName:
    """a players name can consist of 3 parts
    fist name - optional
    middle name - optional
    last name - required"""
    def __init__(self, name_text:str):
        if name_text is None:
            raise ValueError(f'text of a name cant be None in {self.__class__}')
        self._name_text=name_text
        self._strings=name_text.split(' ')
    @property
    def names_count(self):
        '''returns count of names Иванов Иван - 2, Иванов иван иванович -3'''
        return len(self._strings)
    @property
    def first_name(self):
        pass #TODO ADD errors of implementation
    @property
    def middle_name(self):
        pass
    @property
    def last_name(self):
        pass
    @property
    def raw_name(self):
        return self._name_text
    
    @property
    def format_basic(self):
        """returns a basic tro part name
        Иван Иванов"""
        if self.first_name is not None:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.last_name

 #   def __str__(self):
 #       return ' '.join([self.first_name,self.last_name])

    def __repr__(self):
        return f'<{self.__class__.__name__}{" "+self.first_name if self.first_name else ""} {self.last_name}>'

class FioName(PlayerName):
    """A class for working with three part names
    Иванов Иван Иванович"""
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

class TwoPartName(PlayerName):
    """A class for working with two part names
    Иванов Иван"""
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