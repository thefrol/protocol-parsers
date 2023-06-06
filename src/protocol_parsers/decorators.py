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

def lower(f):
    def callee(*args,**kwargs):
        try:
            res:str=f(*args,**kwargs)
            if res is None:
                return None
            
            else:
                if isinstance(res,str):
                    return res.lower()
                else:
                    print(f'{f.__name__} is not a string, cant lower that')
                    return None
        except Exception as e:
            print(f'cant lower string — {f.__name__}')
            return None
    return callee