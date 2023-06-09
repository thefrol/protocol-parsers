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

def new_store_first_output(f): #TODO add with_name
    """some sort of lazy initializer
    stores the first value or the called method,
    sloud me used for propetries only"""
    def callee(self, *args,**kwargs):
        if f.__name__ in self.__dict__.get('__output_store__',{}):
            return self.__dict__['__output_store__'][f.__name__]
        else:
            if self.__dict__.get('__output_store__') is None: # create output store if needed
                self.__dict__['__output_store__']={}
            value_to_save=f(self,*args,**kwargs)
            self.__dict__['__output_store__'][f.__name__]=value_to_save
            return value_to_save
    return callee

#fastest
def fast_store_first_output(f): #TODO add with_name
    """some sort of lazy initializer
    stores the first value or the called method,
    sloud me used for propetries only"""
    def callee(self, *args,**kwargs):
        store_name='__lazy__'+f.__name__
        if store_name in self.__dict__:
            return self.__dict__[store_name]
        else:
            value_to_save=f(self,*args,**kwargs)
            self.__dict__[store_name]=value_to_save
            return value_to_save
    return callee

#winner!!!!
def id_store_first_output(f): #TODO add with_name
    """some sort of lazy initializer
    stores the first value or the called method,
    sloud me used for propetries only"""
    __store={}
    def callee(self, *args,**kwargs):
        nonlocal __store
        id_=id(self)
        if id_ in __store:
            return __store[id_]
        else:
            value_to_save=f(self,*args,**kwargs)
            __store[id_]=value_to_save
            return value_to_save
    return callee

#not working
def replace_store_first_output(f): #TODO add with_name
    """some sort of lazy initializer
    stores the first value or the called method,
    sloud me used for propetries only"""
    def callee(self, *args,**kwargs):
            value_to_save=f(self,*args,**kwargs)
            #print('stored')
            self.__dict__[f.__name__]=value_to_save
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



        
