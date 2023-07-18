"""Contains object for exporting data from single link,
a unified parser"""

from . import (
    MosffParser, MosffPlayerParser,MosffTeamParser,
    YflParser, YflPlayerParser, YflTeamParser)

parsers={
    'https://mosff.ru/match/':MosffParser,
    'https://mosff.ru/player/':MosffPlayerParser,
    'https://mosff.ru/player/':MosffTeamParser,
    'https://yflrussia.ru/match/': YflParser,
    'https://yflrussia.ru/player/': YflPlayerParser,
    'https://yflrussia.ru/team/': YflTeamParser,
}

class Exporter:
    def __init__(self, url,*args,html_data=None,**kwargs):
        """
        args, kwargs - parser specific args
        like match_time for MosffParser"""
        parser=self.get_parser(url)
        self.page=parser(url,*args,html_text=html_data,**kwargs)
        self.parser=parser
    @staticmethod
    def get_parser(url):
        for pattern in parsers:
            if pattern in url:
                parser=parsers[pattern]
                return parser
        raise AttributeError(f'no parser for url line {url}')
    def to_rbdata(self):
        return self.page.to_rbdata()


