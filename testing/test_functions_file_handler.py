import os
import unittest
import csv
import json
import logging
from unittest.mock import patch
from ..src import file_handler_class as filehandlerclass

try:
    import src.weather_class as weather_class
    import src.functions as functions
    import ast
except Exception as e:
    logging.error("Importing packages error: {}".format(e))


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.test_directory = 'data/'
        self.test_good_filename = "../data/2022-07-26.txt"
        self.test_bad_filename = 'bad.txt'
        self.test_csv_filename = 'test_csv_file.csv'
        self.test_json_filename = 'test_json_file.json'
        self.test_csv_data = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]
        self.test_json_data = [{"time": "22-06-16 22", "speed": 12.3},
                               {"time": "22-06-16 23", "speed": 10.3},
                               {"time": "22-06-17 00", "speed": 8.0}]
        self.test_good_time = "22-06-16 22"
        self.test_good_speed = 12.9


    def tearDown(self):
        for filename in [self.test_good_filename, self.test_bad_filename, self.test_csv_filename,
                         self.test_json_filename]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_file_handler(self):
        return_value = functions.file_handler(self.test_good_time, self.test_good_speed, self.test_good_filename)

        with self.subTest('correct directory'):
            self.assertTrue(os.path.isdir(self.test_directory))
        with self.subTest('does the test file exist now'):
            self.assertTrue(os.path.exists(self.test_good_filename))
        with self.subTest('does the function return something'):
            self.assertEqual(type(return_value), str)
        with self.subTest('does this function return a string value of TRUE'):
            self.assertEqual(return_value, "True")

    def test_validating_data(self):
        self.test_bad_filename = 'bad.txt'
        return_error = functions.file_handler('22-06-16 22', 12.3, self.test_bad_filename)

        with self.subTest('does it issue an error on incorrect filename'):
            self.assertTrue('Exception error in file_handler()' in return_error)
            self.assertTrue(os.path.exists(self.test_bad_filename),
                            "file_handler() returned an error message but it still created the bad file.")

        with self.subTest('its using the default filename'):
            self.assertTrue(os.path.exists(self.test_bad_filename),
                            f"It's using the default filename - {self.test_bad_filename}")

        if os.path.exists(self.test_bad_filename):
            os.remove(self.test_bad_filename)

    def test_append_specific_file_with_singular_weather_data(self):
        # Create an instance of the FileHandlerClass
        file_handler = filehandlerclass(self.test_good_filename)

        # Call the method to append weather data
        file_handler.append_specific_file_with_singular_weather_data('22-06-16 22', 12.3)

        # Check if the file was opened with the expected parameters
        with open(self.test_good_filename, 'a+') as file:
            # Read the contents of the file
            content = file.read()
            # Check if the data was appended correctly
            self.assertIn('22-06-16 22', content)
            self.assertIn('12.3', content)

    def test_read_specific_weather_file(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.read.return_value = ''.join(self.test_csv_data)
            filehandlerclass.read_specific_weather_file(self.test_good_filename)
            self.assertEqual(mock_open.call_args.args[0], self.test_good_filename)

    def test_read_specific_csv_file(self):
        with open(self.test_csv_filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.test_csv_data)
        filehandlerclass.read_specific_csv_file(self.test_csv_filename)
        self.assertEqual(len(filehandlerclass.weatherDataList), 3)

    def test_add_files_in_directory(self):
        os.makedirs(self.test_directory, exist_ok=True)
        os.makedirs(os.path.join(self.test_directory, 'subdir'), exist_ok=True)
        with open(os.path.join(self.test_directory, 'file1.txt'), 'w') as f:
            pass
        with open(os.path.join(self.test_directory, 'subdir', 'file2.txt'), 'w') as f:
            pass

        # Print out the contents of the directory
        print("Directory contents:", os.listdir(self.test_directory))

        files = filehandlerclass.add_files_in_directory(self.test_directory)
        print("Files found:", files)  # Add this line to print the files found
        self.assertEqual(len(files), 2)
        self.assertIn('file1', files)
        self.assertIn('file2', files)

    def test_get_files_in_directory(self):
        files = filehandlerclass.get_files_in_directory()
        self.assertEqual(files, [])

    def test_read_json_data_from_file(self):
        with open(self.test_json_filename, 'w') as json_file:
            json.dump(self.test_json_data, json_file)
        data = filehandlerclass.read_json_data_from_file(self.test_json_filename)
        self.assertEqual(data, self.test_json_data)


if __name__ == '__main__':
    unittest.main()
