"""a script for makink export files for testing
in file there is a web page and expected output"""
import requests
import json

from protocol_parsers import Exporter


url='https://mosff.ru/match/34549'
#url='https://mosff.ru/match/38876' #CUP
#url='https://mosff.ru/match/38860' #CUP 2009
#url='https://mosff.ru/match/34540' #no minute for autogoals, add to tests
file_name='mosff_match_34549.txt'
args=[]
kwargs={}

def make_dict(url,*args, **kwargs):
    exporter=Exporter(url,*args, **kwargs)

    res={}
    
    res['url']=url
    res['exporter_args']=args
    res['exporter_kwargs']=kwargs
    res['html_data']=requests.get(url).text
    res['rbdata']=exporter.to_rbdata()
    return res

def save(file,data):
    with open(file,'w') as f:
        json.dump(data,f)

save(file_name, make_dict(url, *args,*kwargs))