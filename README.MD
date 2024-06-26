# Парсеры для протоколов МФФ и ЮФЛ

# Установка

    pip install git+https://github.com/thefrol/protocol-parsers

Готово, пользуйтесь!

## Важные моменты

У матчей очень важны дата. По ней может определяться сезон соревнования, и если дата будет пустой, то матч может просто не испортироватьс в РБДата

### Установка для разработчика

Скачивание репозитория
```
 git clone https://github.com/thefrol/protocol-parsers
 cd protocol-parsers
```

Установка локального окружения

```
python -m venv .local_env
source ./.local_env/bin/activate
pip install -r requirements.txt
```

Установка пакета в режиме разработки, после чего в системе можно будет делать `import protocol-parsers`

```bash
pip install -e .
```

Теперь можно работать!

# Использование

## Универсальный способ

```python
from protocol_parsers import Exporter

data=Exproter('https://yflrussia.ru/match/3409563').to_rbdata()
print(data)
```
~~да, да импорт экспортер лол~~

## МФФ

```python
    from protocol_parsers import MosffParser

    protocol_data =  MosffParser('http://mosff.ru/match/34992')
    print(protocol_data.to_rbdata()) # вывод формате питона
    print(protocol_data.to_json()) # вывод в формате json строки
```

Парсинг игроков

```python
    from protocol_parsers import MosffPlayerParser

    player=MosffPlayerParser('https://mosff.ru/player/2060')
    print(protocol_data.to_rbdata()) # вывод формате питона
```

# Формат вывода

## Протокол

```javascript
    {

        "tournament_name": "MФФ ЛПМ U10(2013)", // название лиги

        "tournament_id": 484, // id турнира на сайте мосфф
        "tournament_round": "6", // раунд string
        "tournament_round_id": 12314 // id раунда
        "tournament_round_url" : "/tournament/1024231/calendar?round_id=1042374" // ссылка на раунд
        "tournament_name": "MФФ ЛПМ U10(2013)", // название лиги
        
        "score": "7:2", //счет в матче
        "home_team_score": 7,
        "guest_team_score": 2,

        "duration": 50, // время на поле
        "time_player":50 // то же самое, сделано для обратной совместимости

        "guest_team_name": "Сокол 2013",
        "home_team_name": "ФШМ 2013",

        "home_team_id": 2044,
        "guest_team_id": 2051

        "home_team_image_url": "https://hb.bizmrg.com/st.mosmff.ru/team/78/logo/63dbb7c7646ea_200x200.png", // логотипы комманд
        "guest_team_image_url": "https://hb.bizmrg.com/st.mosmff.ru/team/54/logo/600ea55de3146_200x200.jpg",
        
        "date": { // дата матча
            "iso_string": "2023-05-21 11:30:00", // дата в формате utc
            "day": 21,
            "hour": 11, // тут уже московское время
            "minute": 30,
            "month": 5,
            "year": 2023 // берется из даты турнира, иначе текущий год
            },

        "guest_team_players":  //состав команды хозяев
            [
                {
                    "name": "Иван Ничутин", // как зовут в формате имя-фамилия
                    "number":"71", // номер на поле
                    "autogoals": 0, // количество автоголов
                    "goals": 0, // количество забитых
                    "goals_missed": 5, // количество пропущенных, если вратарь, если полевой - то ноль
                    "image": "https://hb.bizmrg.com/st.mosmff.ru/player/27649/photo/639340d953def_200x200.jpg", // фотка с сайта мфф
                    "is_capitain": False, // игрок капитан
                    "is_goalkeeper": True, // игрок голкипер
                    
                    "id": 27649, // id в системе мосфф
                    "yellow_cards": 0 // количество желтых
                    "red_cards": 0, // количество красных

                    "time_played": 50, // время на поле
                    "relative_time_played": 0 // относительное время если >0, то не зависит от времени матча,
                                              // если меньше нуля, то time_played= match_time+relative_time_played
                                              //
                                              // none - игрок не играл, то сыграл вообще ноль
                                              // 0 - играл весь матч
                                              // -14 играл весь матч без 14 минут
                                              // 14 сыграл 14 минут
                    "relative_time_out": 0 // время ухода с поля по тем же правилам
                                           // 0 - играл до конца
                                           // 14 ушел на 14 минуте
                                           // отрицательные значения не выдает
                                           // кажется глупым, но нам просто важно знать, что игрок играл до конца матча

                                           // комментарий относительно relative_time_in
                                           // чтобы не путаться, относительно время выхода на поле не указано, 
                                           // иначе можно перепутать 0 - это конец матча, или начало
                                           // а указывать none как начало матча это слишком усложняет дело
                    "time_in":0, // минута появления на поле, или none если на поле не выходил
                    "time_out":50 // минута ухода с поля или none если не играл

                    "sub_from": { // Информация о том, кого заменил игрок. None в случае если никого
                        "id": 3098674, // id игрока
                        "minute": 62, //минута замены
                        "number": "72"}, //номер замененного игрока
                    "sub_to": None, // информация о игроке, который заменил этого

                    "events":[
                        {
                            "time":20,  // время события
                            "type":"yellow-card" // тип события
                                                 // sub-in, sub-out - замены
                                                 // yellow-card, red-card - карточки
                                                 // goal, autogoal - голы и автоголы
                        },
                        {...}
                    ]
                },
                {...},
            ] ,
        "home_team_players": [...], //состав команды гостей
    }
```

## Игрок МФФ

```javascript
    {
        'birth_date': '2006-06-30 00:00:00', // дата рождения в ISO формате
        'birth_date_dict':  // дата рождения в формате словаря
                {
                    'day': 30,
                    'month': 6,
                    'year': 2006}, 
        'birth_date_raw': '30 июня 2006', // дата рождения как было написано на сайтесайте№

        'name': 'Иван Ульянов', // имя в формате rbdata
        'name_raw': 'Ульянов Иван Евгеньевич', // имя в формате rbdata
        'image_url': 'https://st.joinsport.io/player/5865769/photo/640c111e2f812_thumb.png', // фото игрока

        'role_raw': 'Вратарь', // амплуа как на сайте

        'team_name': 'Савеловская 2006', // имя команды в формате rbdata
        'team_name_raw': 'Савеловская 2006 г.р.', // имя команды как на сайте

        'team_id': 374, // айди команды
        'team_url': 'https://mosff.ru/team/374', // ссылка на команду
        'team_url_raw': '/team/374', // ссылка на команду как было на сайте

        'team_year': '2006' // год рождения игроков команды
    }
```

## команда МФФ

```javascript
    {
        'id': 2044, // id команды
        'name': 'ФШМ 2013', // имя в стиле rbdata
        'raw_name': 'ФШМ 2013 г.р.', // имя команды как на сайте
        'team_year': '2013'} // год рождения игроков команды
```
# Тесты

```bash
    python -m unittest discover -s ./tests -p '*_test.py'    
```

# Обновления

## 20.07.23 Обновление 0.4
в вывод добавлены поля `tournament_round`, `tournament_round_id`, `tournament_round_url`
Добавлена поддержка номера тура в протоколах ЮФЛ
дофигища зарефакторено, теперь более четкая логика
Добавлены поля `home_team_image_url` `guest_team_image_url` с логотипами комманд в выводе протоколов
Добавлены `image_url` - фото игрока со страницы его профиля(парсинг игрока)

## 19.07.23 Обновление 0.3
Добавлен `Exporter` - класс позволяющий майнить данные по любой поддерживаемой ссылке
Протоколы ЮФЛ и МФЛ покрыты тестами на экспорт

## 18.07.23
При парсинге протокола выдается информация кого или кем был заменен игрок `sub_from` `sub_to`

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

    [ ] пусть какой-то скрипт вычищает лишнюю инфу из созраненных страниц для тестирования. Там текст скриптов и прочее. Можно столько места освободить
    [ ] https://mosff.ru/player/27840 игрок имеет две команды
    [ ] https://mosff.ru/player/2061 нет команды и фото
    [ ] https://yflrussia.ru/player/6431134 криво указана команда
    [ ] https://yflrussia.ru/match/3409643 нет номера у капитана
    [ ] время выдает на три часа позже в хабе. Видимо надо выдавать utc standart time
    [ ] teams without year
    [x] tournament id
    [ ] Кубок МФФ - вовсе не кубок, например
    [ ] mosff substitute info(sub_from, sub_to)
    [ ] players list in team page parser
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

### 0.2.5
[x] фикс айдишников команд в юфл

### 0.2.6
[x] починка багов
https://yflrussia.ru/player/5865769 - нет даты

### 0.2.7
тесты для yfl
исправлен баг с количеством голов, если гол был забит на последней минуте или в дополнительное время

### 0.2.8
разбиение yfl/__init__.py на подфайлы

## 0.3
больше информации о заменах. Кого на кого поменяли. Только протоколы юфл

## 0.4
Универсальный парсер `Exporter`

### 0.4.1
Больше тестов на экспорт

### 0.4.x
Переезд парсеров МФФ на WebParser


## 0.4
Поддержка фото в парсинге игроков
списки игроков при парсинге команд, и другие данные что можно вытянуть

## 0.5 Рефакторинг
Парсинг мосфф исползует класс `TagMiner`

## 0.6 Exceptions
проработка странных сценариев, когда на старнице нет каких=то полей или что-то указано неверно