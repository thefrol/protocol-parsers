from typing import Callable
import copy

class TagMiner:
    """a basic class for working with tags, a wrapper for bs4 parser"""
    def __init__(self, html):
        if isinstance(html,TagMiner):
            self._html=html._html
        else:
            self._html=html

        self.verbose=True
    @property
    def is_empty(self):
        return self._html is None
    def _find_tag(self, tag=None, class_=None):
        """finds first specified tag
        if class= None searches for tags with any classes, 
        unlike in Beatiful soup where when class=None
        searches for tag with no specified classes and 
        if class specified find() doesnt return it"""
        ##TODO should return some metaclass, or we should have an error wrapper for this when getting text
        #TODO _find_tag(self, class_,tag=None) for search as class
        if self.is_empty:
            print(f'searching an empty tag {self} for tag={tag} class={class_}')
            found_tag=None
        else:
            if class_ is None:
                found_tag=self._html.find(tag)
            else:
                found_tag=self._html.find(tag, class_=class_)

            
        return TagMiner(found_tag)
    def _find_all_tags(self, tag=None, class_=None):
        """finds all specified tags
        if class= None searches for tags with any classes, 
        unlike in Beatiful soup where when class=None
        searches for tag with no specified classes and 
        if class specified find() doesnt return it"""

        if self.is_empty:
            print(f'searching an empty tag {self} for tag={tag} class={class_}')
            found_tags=[]
        else:
            if class_ is None:
                found_tags=self._html.find_all(tag)
            else:
                found_tags=self._html.find_all(tag, class_=class_)
        return [TagMiner(tag) for tag in found_tags]
    def tag_text(self):
        if self.is_empty:
            if self.verbose:
                print(f'getting text from empty Tagminer "{self}"')
            return None
        return self._html.text
    @property
    def text(self):
        return self.tag_text()
    @property
    def href(self):
        if self.is_empty:
            if self.verbose:
                print(f'getting href from empty Tagminer {self}')
        return self.get_param('href')
    def find_in_parents(self, comparator:Callable, search_depth=10): 
        """Function for searching in parent tags
        ex. if one of parent tags has a class 'bar'
        find_in_parent_tags(lambda tag: 'bar' in tag['class'])"""
        current_tag=self._html.parent
        for i in range(search_depth):
            if comparator(current_tag):
                return True
            current_tag=current_tag.parent
        return False
    def get_param(self, attribute_name, default=None, verbose=False):
        """safely returns html tag attribute value and fallbacks to default if param not found
        self.get('href', 'no link')
        #/player/12342
        verbose: if True -> show warning on fallback to default"""
        if attribute_name in self._html.attrs:
            return self._html.attrs[attribute_name]
        else:
            if verbose:
                print(f'falling back to default {default} when getting param "{attribute_name}" on Tagminer {self} (no attribute in this tag)')
            return default
    def __getitem__(self, item):
        if item not in self._html.attrs:
            raise ValueError(f'cant get param "{item}" from Tagminer {self.__class__}')

        return self._html[item]
    
    @property
    def a(self):
        return self._html.a
    
    @property
    def no_verbose(self):
        """used when we want to use this object but without it verbosing for this action
        like if sometimes obj.text shoots a warning and sometimes not, it could worn a 20-30 times a match
        but thi warning is ok, so we use
        obj.no_verbose.text instead of obj.text
        
        creates a copy of object so could take more time and memory"""
        new_obj=copy.copy(self)
        new_obj.verbose=False
        return new_obj



##
# все могло быть проще, можно было просто расширть класс Beautiful soup
# если бы я знал, что там тожно можно делать поиск по классу class_=...
