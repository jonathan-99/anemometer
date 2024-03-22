#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import datetime
import json
from src.weather_model_parser import extract_csv_from_text, convert_extracted_file_to_model, get_absolute_path



class TestWeatherModelParser(unittest.TestCase):
    def replace_json(self, json_obj, key: str, test_name: str):
        # Check if the 'weatherData' key exists in the JSON object
        if 'weatherData' in json_obj:
            # Check if the 'metadata' key exists within the 'weatherData' section
            if 'metadata' in json_obj['weatherData']:
                # Replace the value of the 'hostname' key with the value of 'test_hostname'
                json_obj['weatherData']['metadata'][key] = test_name
        return json_obj

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

        #extract csv data into json
        filename = ('2024-03-07.txt')
        full_filename = get_absolute_path(filename)
        extracted_csv_data =  extract_csv_from_text(full_filename)
        extracted_csv_data = json.loads(extracted_csv_data)
        # print(f'csv data  - {type(extracted_csv_data)} - {extracted_csv_data}')

        #parse csv to json format
        full_filename = str(full_filename).replace('\\\\','\\')
        return_json = convert_extracted_file_to_model(extracted_csv_data, full_filename)
        print(f'return json to be tested - {return_json}')

        #extract expected json data
        filename_expected = get_absolute_path('extracted_and_converted_example.json')
        # print(f'This is the filename - {filename_expected}')
        with open(filename_expected, 'r') as file:
            expected_json = json.load(file)


        #amend the expect json with some testing host specific variables.
        import socket
        from datetime import datetime
        local_hostname = socket.gethostname()
        local_ip_address = socket.gethostbyname(local_hostname)
        current_date = datetime.now().strftime('%Y-%m-%d')
        expected_json = self.replace_json(expected_json, "hostname", local_hostname)
        expected_json = self.replace_json(expected_json, 'src_ip', local_ip_address)
        expected_json = self.replace_json(expected_json, 'date_transmitted', current_date)

        print(f' extracted_and_converted_example.json - {expected_json}')

        with self.subTest():
            self.assertDictEqual(return_json, expected_json)


if __name__ == '__main__':
    unittest.main()
