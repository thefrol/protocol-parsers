def trim(f):
    def callee(*args,**kwargs):
        return f(*args,**kwargs).strip()
    return callee

def to_int(f):
    def callee(*args,**kwargs):
        try:
            return int(f(*args,**kwargs))
        except ValueError as e:
            print(f'cant convert to int — {f.__name__}')
            return None
    return callee

def to_int_or_none(f):
    def callee(*args,**kwargs):
        call_result=f(*args,**kwargs)
        if call_result is None:
            return None
        else:
            try:
                return int(call_result)
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


def store_first_output(f): #TODO add with_name
    """some sort of lazy initializer
    stores the first value or the called method,
    sloud me used for propetries only"""
    def callee(self, *args,**kwargs):
        if self.__dict__.get('__output_store__') is None:
            self.__dict__['__output_store__']={}
        if f.__name__ in self.__dict__['__output_store__']:
            return self.__dict__['__output_store__'][f.__name__]
        else:
            value_to_save=f(self,*args,**kwargs)
            self.__dict__['__output_store__'][f.__name__]=value_to_save
            return value_to_save
    return callee

# def store_(f):
#     _local_value=None
#     _is_stored=False # in case _local_value is None and we may check if we called the function already
#     def callee(*args, **kwargs):
#         nonlocal _local_value,_is_stored
#         if _is_stored is False:
#             _local_value=f(*args,**kwargs)
#             _is_stored=True
#         return _local_value
#     return callee



        
