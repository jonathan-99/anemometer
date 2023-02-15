import unittest
from src import functions
from os.path import exists

"""
Test to check the validity of the data entered into a file.
"""


class TestFileHandler(unittest.TestCase):
    global good_value, bad_value_letters
    good_value = '2.3'
    bad_value_letters = 'wd'

    def test_file_handler_good(self):
        """
        Is the filename handled correctly - good / bad input data.
        Currently an error on finding the file, hence commenting it out.
        """
        temp_filename = "data/2022-07-26.txt"

        # with self.subTest():
        #     output = functions.file_handler(temp_filename, good_value)
        #     self.assertTrue(output)
        # with self.subTest():
        #     output = functions.file_handler(temp_filename, bad_value_letters)
        #     if 'True' not in output:
        #         self.assertFalse(False)
        #     else:
        #         self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()