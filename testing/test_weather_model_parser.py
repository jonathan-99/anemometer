#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from src.weather_model_parser import parser, extract_csv_from_text

class TestParser(unittest.TestCase):

    def test_parser(self):
        # Mocking the schema.load method to return a fixed dictionary
        with patch('your_script_name.model.WeatherConfigurationSchema.load') as mock_load:
            mock_load.return_value = {'result': 'fake_result'}

            # Providing mock data similar to what's passed to the parser function
            data = {'weatherConfiguration': {'some_data': 'fake_data'}}

            # Expected output after parsing
            expected_output = {'result': 'fake_result'}

            # Testing the parser function
            self.assertEqual(parser(data), expected_output)

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


if __name__ == '__main__':
    unittest.main()
