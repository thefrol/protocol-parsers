import unittest

class TestModule(unittest.TestCase):
    def test_import(self):
        """
        test importing main classes
        """
        from protocol_parsers import MosffParser, YflParser
        self.assertIsNotNone(MosffParser)
        self.assertIsNotNone(YflParser)

if __name__ == '__main__':
    unittest.main()