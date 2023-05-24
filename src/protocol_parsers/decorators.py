def trim(f):
    def callee(*args,**kwargs):
        return f(*args,**kwargs).strip()
    return callee