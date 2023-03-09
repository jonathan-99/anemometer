import unittest
from src import functions
from os.path import exists


class TestReadInData(unittest.TestCase):
    def test_read_in_data(self):
        """
        When a filename is passed, it creates the file.
        """
        output = functions.read_in_data("testing/test_data_from_counter.csv")
        file_exists = exists("testing/test_data_from_counter.csv")
        self.assertEqual(type(output), list)
        self.assertTrue(file_exists)


if __name__ == '__main__':
    unittest.main()
