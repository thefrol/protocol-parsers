import unittest
from exports.base import load_dicts, is_subset, find_files, unequal_params

#TODO test for errors on creation

class BasicTest(unittest.TestCase):
    def test_protocols(self):
        for file in find_files('mosff_match'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name} \n unequal params {unequal_params(data, file_data)}')
    def test_players(self):
        for file in find_files('mosff_player'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name} \n unequal params {unequal_params(data, file_data)}')
    def test_teams(self):
        for file in find_files('mosff_team'):
            data,file_data=load_dicts(file.name)
            self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name} \n unequal params {unequal_params(data, file_data)}')


if __name__ == '__main__':
    unittest.main()