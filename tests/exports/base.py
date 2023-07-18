import json
import pathlib

from protocol_parsers import Exporter

files_folder='data'
here=pathlib.Path(__file__).parent
data_folder=here / files_folder

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
    if small != big | small:
        return False
    return big|small == big
