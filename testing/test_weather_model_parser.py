#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import datetime
import json
from src.weather_model_parser import extract_csv_from_text, convert_extracted_file_to_model, get_absolute_path

class TestWeatherModelParser(unittest.TestCase):

    def test_extract_csv_from_text(self):
        # Testing with a sample file content
        file_content = "2024 03 07 00,0.09724137931034482,\n"\
                       "2024 03 07 01,0.018620689655172412,\n"\
                       "2024 03 07 02,0.0010344827586206895,\n"\
                       "2024 03 07 03,0.006206896551724138,\n"\
                       "2024 03 07 04,0.001379310344827586,\n"\
                       "2024 03 07 05,0.000689655172413793,\n"\
                       "2024 03 07 06,0.13448275862068965,\n"\
                       "2024 03 07 07,0.31344827586206897,\n"\
                       "2024 03 07 08,0.08413793103448276,\n"\
                       "2024 03 07 09,0.10620689655172413,\n"\
                       "2024 03 07 10,0.24206896551724139,\n"\
                       "2024 03 07 11,0.3096551724137931,\n"\
                       "2024 03 07 12,0.7510344827586206,\n"\
                       "2024 03 07 13,0.6362068965517241,\n"\
                       "2024 03 07 14,0.5575862068965517,\n"\
                       "2024 03 07 15,0.6406896551724137,\n"\
                       "2024 03 07 16,0.5637931034482758,\n"\
                       "2024 03 07 17,0.48413793103448277,\n"\
                       "2024 03 07 18,0.18999999999999997,\n"\
                       "2024 03 07 19,0.3393103448275862,\n"\
                       "2024 03 07 20,0.1772413793103448,\n"\
                       "2024 03 07 21,0.39034482758620687,\n"\
                       "2024 03 07 22,0.6075862068965517,\n"\
                       "2024 03 07 23,0.5158620689655172,"

        # Creating a temporary file with the sample content
        with patch('builtins.open', unittest.mock.mock_open(read_data=file_content)):
            # Testing the extract_csv_from_text function
            self.assertEqual(extract_csv_from_text('fake_file_path'), file_content)


    def test_convert_extracted_file_to_model(self):
        """
        This should postivitely test the convert_extracted_file_to_model(input_data, input_filename): only.
        """
        filename = 'data/2024-03-07.txt'
        csv_data = extract_csv_from_text(filename)

        filename_expected = get_absolute_path('extracted_and_converted_example.json')
        print(f'This is the filaname - {filename_expected}')
        with open(filename_expected, 'r') as file_object:
            print(f'file object - {file_object}')
            expected_json = json.load(file_object.name)

        with self.subTest():
            return_json = convert_extracted_file_to_model(csv_data, filename)
            self.assertEqual(return_json, expected_json)


if __name__ == '__main__':
    unittest.main()
