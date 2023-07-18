
import unittest
from exports.base import load_dicts, is_subset, data_folder
from protocol_parsers.regex import Regex

#TODO test for errors on creation

def find_files(prefix):
    '''returns pathlib.Path objects for files with specified prefix in data folder'''
    for file in data_folder.iterdir():
        if file.name.startswith(prefix):
              yield file

class BasicTest(unittest.TestCase):
    def test_protocols(self):
        for file in find_files('mosff_match'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')
    def test_players(self):
        for file in find_files('mosff_player'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')


if __name__ == '__main__':
    unittest.main()