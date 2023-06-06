def trim(f):
    def callee(*args,**kwargs):
        return f(*args,**kwargs).strip()
    return callee

def to_int(f):
    def callee(*args,**kwargs):
        try:
            return int(f(*args,**kwargs))
        except Exception as e:
            print(f'cant convert to int — {f.__name__}')
            return None
    return callee