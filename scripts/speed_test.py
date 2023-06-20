from protocol_parsers import MosffParser
from pprint import pprint

import time

def count_mean(times:int):
    def decorator(f):
        def callee(*args,**kwargs):
            return sum([f(*args,**kwargs) for i in range(times)])/times
        return callee
    return decorator

#@count_mean(10)
def test_speed(func):
    start=time.time()
    func()
    return time.time()-start


#URL='https://mosff.ru/match/34549'
#URL='https://mosff.ru/match/38876' CUP
#URL='https://mosff.ru/match/38860' #CUP 2009
URL='https://mosff.ru/match/34540' #no minute for autogoals, add to tests

func=MosffParser(URL).to_rbdata

print(f'elapsed {test_speed(func)}')
print(f'elapsed {test_speed(func)}')
print(f'elapsed {test_speed(func)}')

# 3 times before cached
# elapsed 0.09293127059936523
# elapsed 0.009006500244140625
# elapsed 0.007993698120117188

# same time after caching teams
# slight boost after cahing opposing team

