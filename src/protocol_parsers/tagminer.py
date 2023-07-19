from typing import Callable

class TagMiner:
    """a basic class for working with tags, a wrapper for bs4 parser"""
    def __init__(self, html):
        self._html=html
    def _find_tag(self, tag=None, class_=None):
        ##TODO should return some metaclass, or we should have an error wrapper for this when getting text
        #TODO _find_tag(self, class_,tag=None) for search as class
        return self._html.find(tag,{'class':class_})
    def _find_all_tags(self, tag=None, class_=None):
        return self._html.find_all(tag,{'class':class_})
    def tag_text(self):
        return self._html.text
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
    def get_param(self, attribute_name, default=None):
        """safely returns html tag attribute value and fallbacks to default if param not found
        self.get('href', 'no link')
        #/player/12342"""
        if attribute_name in self._html.attrs:
            return self._html.attrs[attribute_name]
        else:
            return default