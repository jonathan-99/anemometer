#!/usr/bin/env python3

import re
import unittest
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
        """
        This will input a csv data and output a json format.
        """
        # Testing with a sample file content
        filename = "2024-03-07.txt"
        fname = get_absolute_path(filename)
        full_filename = re.sub(r'\\\\', r'\\', filename)
        return_json = extract_csv_from_text(fname)
        expected_json = { "data": [
            {
            "timestamp": "2024 03 07 00",
            "speed": 0.09724137931034482
          },
          {
            "timestamp": "2024 03 07 01",
            "speed": 0.018620689655172412
          },
          {
            "timestamp": "2024 03 07 02",
            "speed": 0.0010344827586206895
          },
          {
            "timestamp": "2024 03 07 03",
            "speed": 0.006206896551724138
          },
          {
            "timestamp": "2024 03 07 04",
            "speed": 0.001379310344827586
          },
          {
            "timestamp": "2024 03 07 05",
            "speed": 0.000689655172413793
          },
          {
            "timestamp": "2024 03 07 06",
            "speed": 0.13448275862068965
          },
          {
            "timestamp": "2024 03 07 07",
            "speed": 0.31344827586206897
          },
          {
            "timestamp": "2024 03 07 08",
            "speed": 0.08413793103448276
          },
          {
            "timestamp": "2024 03 07 09",
            "speed": 0.10620689655172413
          },
          {
            "timestamp": "2024 03 07 10",
            "speed": 0.24206896551724139
          },
          {
            "timestamp": "2024 03 07 11",
            "speed": 0.3096551724137931
          },
          {
            "timestamp": "2024 03 07 12",
            "speed": 0.7510344827586206
          },
          {
            "timestamp": "2024 03 07 13",
            "speed": 0.6362068965517241
          },
          {
            "timestamp": "2024 03 07 14",
            "speed": 0.5575862068965517
          },
          {
            "timestamp": "2024 03 07 15",
            "speed": 0.6406896551724137
          },
          {
            "timestamp": "2024 03 07 16",
            "speed": 0.5637931034482758
          },
          {
            "timestamp": "2024 03 07 17",
            "speed": 0.48413793103448277
          },
          {
            "timestamp": "2024 03 07 18",
            "speed": 0.18999999999999997
          },
          {
            "timestamp": "2024 03 07 19",
            "speed": 0.3393103448275862
          },
          {
            "timestamp": "2024 03 07 20",
            "speed": 0.1772413793103448
          },
          {
            "timestamp": "2024 03 07 21",
            "speed": 0.39034482758620687
          },
          {
            "timestamp": "2024 03 07 22",
            "speed": 0.6075862068965517
          },
          {
            "timestamp": "2024 03 07 23",
            "speed": 0.5158620689655172
          }
        ]
      }

        with self.subTest():
            print(f'return_json - {repr(json.loads(return_json))}')
            print(f'expected_json - {repr(expected_json)}')
            self.assertDictEqual(json.loads(return_json), expected_json)


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
