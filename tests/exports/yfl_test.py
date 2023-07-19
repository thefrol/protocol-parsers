import unittest
from exports.base import load_dicts, is_subset, find_files

class BasicTest(unittest.TestCase):
    def test_protocols(self):
        for file in find_files('yfl_match'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')
    def test_players(self):
        for file in find_files('yfl_player'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')
    def test_teams(self):
        for file in find_files('yfl_team'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')

if __name__ == '__main__':
    unittest.main()