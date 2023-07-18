import json
import pathlib
import unittest

from protocol_parsers import Exporter

here=pathlib.Path(__file__).parent
files_folder='data'

def load_dicts(file_name):
    path = here / files_folder / file_name
    with open(path,'r') as f:
        res=json.load(f)
    
    file_data=res['rbdata']
    data=Exporter(url=res['url'],html_data=res['html_data']).to_rbdata()

    return data, file_data

def is_subset(big, small):
    return small == big | small


class BasicTest(unittest.TestCase):
    def test_3409563(self):
        data,file_data=load_dicts('yfl_match_3409563.txt')
        self.assertTrue(is_subset(data, file_data))

if __name__ == '__main__':
    unittest.main()