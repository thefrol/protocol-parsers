
import unittest
from exports.base import load_dicts, is_subset



class BasicTest(unittest.TestCase):
    def test_3409563(self):
        data,file_data=load_dicts('yfl_match_3409563.txt')
        self.assertTrue(is_subset(data, file_data))

if __name__ == '__main__':
    unittest.main()