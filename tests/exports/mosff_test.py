
import unittest
from exports.base import load_dicts, is_subset, data_folder
from protocol_parsers.regex import Regex

#TODO test for errors on creation

class BasicTest(unittest.TestCase):
    def test_protocols(self):
        for file in data_folder.iterdir():
            prefix='mosff_match'
            if file.name.startswith(prefix):
                data,file_data=load_dicts(file.name)
                self.assertTrue(is_subset(data, file_data), f'error parsing saved file {file.name}')

if __name__ == '__main__':
    unittest.main()