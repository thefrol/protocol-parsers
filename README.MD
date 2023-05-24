# Парсеры для протоколов МФФ и ЮФЛ

# Установка

# Использование

    from protocol_parsers import MosffParser, YflParser

    protocol1 =  MosffParser().parse('http://mosff.ru/match/34992')
    protocol2 =  YflParser().parse('https://yflrussia.ru/match/3061996')

# Тесты

# Проблемы

Что делать со временем матча? Некоторые игры проходят 70 минут, тот же возраст потом может сыграть 60 минут. И как все это регулировать непонятно ибо в протоколе не написано