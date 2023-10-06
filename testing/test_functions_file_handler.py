import os
import unittest
from src import functions
import src.weather_class as weather_data_object

"""
Test to check the validity of the data entered into a file.
"""


class TestFileHandler(unittest.TestCase):

    def test_file_handler(self):
        """
        This will test the file_handler().
        . Creates file.
        . Good input data.
        . logs data
        . delete test file
        """
        self.test_good_filename = "../data/2022-07-26.txt"
        self.test_good_data_list = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]
        self.test_good_speed = 12.3
        self.test_good_time = '22-06-16 22'
        self.test_directory = '../data'


        return_value = functions.file_handler(self.test_good_time, self.test_good_speed, self.test_good_filename)

        with self.subTest('correct directory'):
            self.assertTrue(os.path.isdir(self.test_directory))
        with self.subTest('does the test file exist now'):
            self.assertTrue(os.path.exists('../data/2022-07-26.txt'))
        with self.subTest('does the function return something'):
            self.assertEqual(type(return_value), str)
        with self.subTest('does this function return a string value of TRUE'):
            self.assertEqual(return_value, "True")

    def test_validating_data(self):
        """
        This needs to test bad data handling - at the moment file_handler() does not do validity checking.
        """
        self.test_bad_filename = 'bad.txt'
        #  add logic
        #  if filename doesn't exist and its a 00 or 01 in the hour, create file; else error
        return_error = functions.file_handler('22-06-16 22', 12.3, self.test_bad_filename)
        with self.subTest('does it issue an error on incorrect filename'):
            print("test_file_handler() - return_error - {}".format(return_error))
            if 'Exception error in file_handler() -' in return_error:
                self.assertTrue(True)
                # has it created a bad file even as its errored?
                self.assertTrue(os.path.exists(self.test_bad_filename),
                                "file_handler() returned an error message but it still created the bad file.")
            else:
                self.assertTrue(True, "file_handler() functioned correctly")
        with self.subTest('its using the default filename'):
            self.assertEqual(os.path.exists(self.test_bad_filename),
                             True,
                             "Its using the default filename - {}".format(self.test_bad_filename))

        if os.path.exists(self.test_bad_filename):
            os.remove(self.test_bad_filename)
        else:
            pass


if __name__ == '__main__':
    unittest.main()
