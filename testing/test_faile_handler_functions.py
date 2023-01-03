import unittest
from src import functions
import datetime
from os.path import exists

"""
Issue with FileNotFoundError: [Errno 2] No such file 'data/YYYY-mm-dd.txt'
"""


class TestFileHandler(unittest.TestCase):
    def test_file_handler(self):
        test_value = '99.9'
        functions.file_handler(test_value)
        today = datetime.datetime.today()
        this_day = 'data/' + today.strftime('%Y-%m-%d') + '.txt'
        print("this day", this_day)
        with open(this_day, 'r') as fileObject:
            line = fileObject.read()
            if test_value in line: check = True
            else: check = False
        self.assertTrue(check)
        self.assertTrue(exists(this_day))
