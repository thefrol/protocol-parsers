from protocol_parsers.decorators import store_,store_first_output
import time

class Cl:
    def __init__(self, val):
         self.val=val
    @property
    @store_first_output
    def from_store(self):
        print('evaluating')
        return self.val
    @property
    def no_store(self):
        return self.val
    
def run_1000_times(func):
    start=time.time()
    for i in range(1000):
        func()
    total=time.time()-start
    return total


    
c=Cl(1)
b=Cl(2)

print(c.from_store)
print(c.from_store)
print(b.from_store)
print(c.from_store)
print(b.from_store)
print(b.from_store)

print(f'from store 1000 times = {run_1000_times(lambda: c.from_store)}')
print(f'no store 1000 times = {run_1000_times(lambda: c.no_store)}')