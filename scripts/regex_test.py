import re    
from protocol_parsers.regex import Regexes
from protocol_parsers.mosff.match import format_tournament_year

tournament_name='Кубок Москвы среди команд спортивных школ 2009, 2010 гг.р. сызон 2022 года'
main_pattern=r'\(.*(?P<tournament_year>\d{4})\)'
fallback_pattern=r'сезон (?P<tournament_year>\d{4})'
lastchance_pattern=r'(?P<tournament_year>\d{4}) год.{1,5}'

m=Regexes(tournament_name,
    #main_pattern,
                #fallback_pattern,
                   lastchance_pattern)
#print(re.search(fallback_pattern,tournament_name))

print(m.get_group('tournament_year'))
#print(format_tournament_year(tournament_name=tournament_name))