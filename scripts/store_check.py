from protocol_parsers.decorators import store_first_output, new_store_first_output, fast_store_first_output, replace_store_first_output,id_store_first_output
import time

class Cl:
    def __init__(self, val):
         self.val=val
         self._b=3
         self._c=3
         self._d=3
         self._u=3
         self._g=3
         self._g22=3
    @property
    @store_first_output
    def from_store(self):
        return self.val
    @property
    def no_store(self):
        return self.val
    @property
    @new_store_first_output
    def new_store(self):
        return self.val
    
    @property
    @fast_store_first_output
    def fast_store(self):
        return self.val
    @property
    @replace_store_first_output
    def replace_store(self):
        return self.val
    @property
    @id_store_first_output
    def id_store(self):
        return self.val
    
    
def run_1000_times(func):
    start=time.time()
    for i in range(1000000):
        func()
    total=time.time()-start
    return total


    
c=Cl(1)
b=Cl(2)
c.replace_store
c.fast_store
c.new_store
c.from_store
c.id_store


print(f'no store 1000 times = {run_1000_times(lambda: c.no_store)}')
print(f'new store 1000 times = {run_1000_times(lambda: c.new_store)}')
print(f'fast store 1000 times = {run_1000_times(lambda: c.fast_store)}')
print(f'from store 1000 times = {run_1000_times(lambda: c.from_store)}')
print(f'replace store 1000 times = {run_1000_times(lambda: c.replace_store)}')
print(f'id store 1000 times = {run_1000_times(lambda: c.id_store)}')

