import json
import pathlib

from protocol_parsers import Exporter

files_folder='data'
here=pathlib.Path(__file__).parent
data_folder=here / files_folder

def find_files(prefix):
    '''returns pathlib.Path objects for files with specified prefix in data folder'''
    for file in data_folder.iterdir():
        if file.name.startswith(prefix):
              yield file

def load_dicts(file_name):
    path = data_folder / file_name
    with open(path,'r') as f:
        res=json.load(f)
    
    file_data=res['rbdata']
    data=Exporter(url=res['url'],html_data=res['html_data']).to_rbdata()

    return data, file_data

def is_subset(big, small):
    """compares two dictinaries
    True: small is subset of big AND all small values equall to big"""
    if big != big | small:
        return False
    return big|small == big

def unequal_params(a,b, indent=0):
    error_strings=[]
    if isinstance(a,dict) and isinstance(b,dict):
        unequal=[k for k in b if k in a if b[k]!=a[k]]        
        if unequal:
            for k in unequal:
                if isinstance(a[k],dict|list) and isinstance(b[k],dict|list):
                    error_strings.append(f'in field "{k}"')
                    error_strings.append(unequal_params(a[k],b[k],indent=indent+1))
                else:
                    error_strings.append(f"not equal:b['{k}']={b[k]} and a['{k}']={a[k]}")
    elif isinstance(a,list) and isinstance(b,list):
        if len(a) != len(b):
            error_strings.append('arrays have different len')
        else:
            list_err=[]
            for item in zip(a,b):
                m,n=item
                unequal=unequal_params(m,n, indent+1)
                if unequal:
                    list_err.append(unequal)
            if list_err:
                error_strings.append('in_array:')
                error_strings.extend(list_err)
    else:
        if a!=b:
            error_strings.append(f'{a}!={b}')
        else:
            return ''
    return f'\n{"    "*indent}'.join(error_strings)
