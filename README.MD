# Парсеры для протоколов МФФ и ЮФЛ

# Установка

    pip install git+https://github.com/thefrol/protocol-parsers

# Использование

## МФФ
    from protocol_parsers import MosffParser

    protocol_data =  MosffParser('http://mosff.ru/match/34992')
    print(protocol_data.to_rbdata()) # вывод формате питона
    print(protocol_data.to_json()) # вывод в формате json строки

# Формат вывода

    {

        'tournament_name': 'MФФ ЛПМ U10(2013)', # название лиги
        'tournament_round': '6', # раунд
        
        'score': '7:2', #счет в матче
        'home_team_score': 7,
        'guest_team_score': 2,

        'time_played': 50, # время на поле

        'guest_team_name': 'Сокол 2013',
        'home_team_name': 'ФШМ 2013',

        'home_team_id': 2044,
        'guest_team_id': 2051

        'guest_team_players':  #состав команды хозяев
            [
                {
                    'autogoals': 0, # количество автоголов
                    'goals': 0, # количество забитых
                    'goals_missed': 5, # количество пропущенных, если вратарь, если полевой - то ноль
                    'image': 'https://hb.bizmrg.com/st.mosmff.ru/player/27649/photo/639340d953def_200x200.jpg', # фотка с сайта мфф
                    'is_capitain': False, # игрок капитан
                    'is_goalkeeper': True, # игрок голкипер
                    'name': 'Иван Ничутин', # как зовут в формате имя-фамилия
                    'id': 27649, # id в системе мосфф
                    'yellow_cards': 0 # количество желтых
                    'red_cards': 0, # количество красных

                    'time_played': 50, # время на поле
                    'relative_time_played': 0 # относительное время если >0, то не зависит от времени матча,
                                              # если меньше нуля, то       time_played= match_time+relative_time_played
                    'time_in':0, # минута появления на поле, или none если на поле не выходил
                    'time_out':50 # минута ухода с поля или none если не играл
                },
                {...},
            ] ,
        'home_team_players': [...], #состав команды гостей
    }

# Тесты

# Проблемы

Что делать со временем матча? Некоторые игры проходят 70 минут, тот же возраст потом может сыграть 60 минут. И как все это регулировать непонятно ибо в протоколе не написано