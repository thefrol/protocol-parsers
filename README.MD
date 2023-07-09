# Парсеры для протоколов МФФ и ЮФЛ

# Установка

    pip install git+https://github.com/thefrol/protocol-parsers

# Использование

## МФФ
    from protocol_parsers import MosffParser

    protocol_data =  MosffParser('http://mosff.ru/match/34992')
    print(protocol_data.to_rbdata()) # вывод формате питона
    print(protocol_data.to_json()) # вывод в формате json строки

Парсинг игроков
    from protocol_parsers import MosffPlayerParser

    player=MosffPlayerParser('https://mosff.ru/player/2060')
    print(protocol_data.to_rbdata()) # вывод формате питона

# Формат вывода

## Протокол МФФ
    {

        'tournament_name': 'MФФ ЛПМ U10(2013)', # название лиги
        'tournament_round': '6', # раунд
        'tournament_id': 484, # id турнира на сайте мосфф
        
        'score': '7:2', #счет в матче
        'home_team_score': 7,
        'guest_team_score': 2,

        'time_played': 50, # время на поле

        'guest_team_name': 'Сокол 2013',
        'home_team_name': 'ФШМ 2013',

        'home_team_id': 2044,
        'guest_team_id': 2051
        
        'date': { # дата матча
            'iso_string': '2023-05-21 11:30:00', # дата в формате utc
            'day': 21,
            'hour': 11,
            'minute': 30,
            'month': 5,
            'year': 2023 # берется из даты турнира, иначе текущий год
            },

        'guest_team_players':  #состав команды хозяев
            [
                {
                    'name': 'Иван Ничутин', # как зовут в формате имя-фамилия
                    'number':'71', # номер на поле
                    'autogoals': 0, # количество автоголов
                    'goals': 0, # количество забитых
                    'goals_missed': 5, # количество пропущенных, если вратарь, если полевой - то ноль
                    'image': 'https://hb.bizmrg.com/st.mosmff.ru/player/27649/photo/639340d953def_200x200.jpg', # фотка с сайта мфф
                    'is_capitain': False, # игрок капитан
                    'is_goalkeeper': True, # игрок голкипер
                    
                    'id': 27649, # id в системе мосфф
                    'yellow_cards': 0 # количество желтых
                    'red_cards': 0, # количество красных

                    'time_played': 50, # время на поле
                    'relative_time_played': 0 # относительное время если >0, то не зависит от времени матча,
                                              # если меньше нуля, то time_played= match_time+relative_time_played
                                              #
                                              # none - игрок не играл, то сыграл вообще ноль
                                              # 0 - играл весь матч
                                              # -14 играл весь матч без 14 минут
                                              # 14 сыграл 14 минут
                    'relative_time_out': 0 # время ухода с поля по тем же правилам
                                           # 0 - играл до конца
                                           # 14 ушел на 14 минуте
                                           # отрицательные значения не выдает
                                           # кажется глупым, но нам просто важно знать, что игрок играл до конца матча

                                           # комментарий относительно relative_time_in
                                           # чтобы не путаться, относительно время выхода на поле не указано, 
                                           # иначе можно перепутать 0 - это конец матча, или начало
                                           # а указывать none как начало матча это слишком усложняет дело
                    'time_in':0, # минута появления на поле, или none если на поле не выходил
                    'time_out':50 # минута ухода с поля или none если не играл

                    'events':[
                        {
                            'time':20,  # время события
                            'type':'yellow-card' # тип события
                                                 # sub-in, sub-out - замены
                                                 # yellow-card, red-card - карточки
                                                 # goal, autogoal - голы и автоголы
                        },
                        {...}
                    ]
                },
                {...},
            ] ,
        'home_team_players': [...], #состав команды гостей
    }
## Игрок МФФ
    {
        'birth_date': '2006-06-30 00:00:00', # дата рождения в ISO формате
        'birth_date_dict':  # дата рождения в формате словаря
                {
                    'day': 30,
                    'month': 6,
                    'year': 2006}, 
        'birth_date_raw': '30 июня 2006', # дата рождения как было написано на сайте

        'name': 'Иван Ульянов', # имя в формате rbdata
        'name_raw': 'Ульянов Иван Евгеньевич', # имя в формате rbdata

        'role_raw': 'Вратарь', # амплуа как на сайте

        'team_name': 'Савеловская 2006', # имя команды в формате rbdata
        'team_name_raw': 'Савеловская 2006 г.р.', # имя команды как на сайте

        'team_id': 374, # айди команды
        'team_url': 'https://mosff.ru/team/374', # ссылка на команду
        'team_url_raw': '/team/374', # ссылка на команду как было на сайте

        'team_year': '2006' # год рождения игроков команды
    }

## команда МФФ
    {
        'id': 2044, # id команды
        'name': 'ФШМ 2013', # имя в стиле rbdata
        'raw_name': 'ФШМ 2013 г.р.', # имя команды как на сайте
        'team_year': '2013'} # год рождения игроков команды

# Тесты

    python -m unittest discover -s ./tests -p '*_test.py'    

# Обновления

### 27.06.23 
добавлен парсинг игроков и команд ЮФЛ `YFLPlayerParser` и `YflTeamParser`

### 20.06.23
добавлен парсинг протоколв ЮФЛ `YflProtocolParser`

### 07.06.2023
Добавлен номер игрока `number`

### 06.06.2023
Добавлена дата матча `date`, исправлен баг если в дате появлялся месяц `мая`

### 05.06.2023
Теперь с протоколом возвращается поле `tournament_id`

# Проблемы

    [x] tournament id
    [ ] players list
    [ ] add failed penalties to mosff
    [ ] penalties to output (to_rbdata)
    [x] yfl season naming
    [ ] image support on ufl and mff(teams, players)
    [ ] yfl.TeamPromo.home_team and guest team, use more logical containers than just align text left and right. too complicated

### две желтые в протоколах ЮФЛ
В ЮФЛ после второй желтой игроку прописывается автоматичеки красная картчка. Как возвращшать
yellow=2
red=1 |0  на данный момент red=0 по аналогии с мофф

### Cезоны в ЮФЛ возращают только текущий год, пока не известно где брать год матча

# Дорожная карта

## ~~0.2.4~~
~~ Сезоны ЮФЛ правильно рассчитываются ~~

## 0.2.5
[x] фикс айдишников команд в юфл

## 0.2.6
[x] починка багов
https://yflrussia.ru/player/5865769 - нет даты

## 0.2.?
тесты для yfl

## 0.2.?
разбиение yfl/__init__.py на подфайлы

## 0.3
Поддержка фото в парсинге игроков
списки игроков при парсинге команд, и другие данные что можно вытянуть

## 0.4 Рефакторинг
Парсинг мосфф исползует класс `TagMiner`

## 0.5 Exceptions
проработка странных сценариев, когда на старнице нет каких=то полей или что-то указано неверно