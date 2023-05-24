import requests

from protocol_parsers.mosff.match import Match

#URL='https://mosff.ru/match/34549' # a good match with cards, goals, changes
URL='https://mosff.ru/match/34858' # a match with autogoals


page=requests.get(URL)

if page.status_code != 200:
    raise ConnectionError()




m=Match(page.text)
print(m.team_names)
print(m.scores)
print(m.round)
print(m.tournament)
print(m.tournament_year)
print(m.team_year)

print(m.home_team.players)
print(m.guest_team.players)

