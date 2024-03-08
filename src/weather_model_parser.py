#!/usr/bin/env python3

from marshmallow import ValidationError
import re
import json
import class_weather_model as model

def parser(data):
    try:
        schema = model.WeatherConfigurationSchema()
        result = schema.load(data['weatherConfiguration'])
        return result
    except ValidationError as err:
        error_info = {
            'messages': err.messages,
            'data': err.data,
            'field_name': err.field_name,
            'valid_data': err.valid_data
        }
        return json.dumps(error_info)

def extract_csv_from_text(file_path):
    csv_text = ""
    try:
        with open(file_path, 'r') as file:
            # Read the entire content of the file
            file_content = file.read()

            # Use regular expression to find CSV text
            csv_matches = re.findall(r'(?<=\bCSV:)(.*?)(?=\bENDCSV|$)', file_content, re.DOTALL)

            # Concatenate all CSV matches
            csv_text = '\n'.join(csv_matches)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return csv_text

if __name__ == "__main__":
    test_data = extract_csv_from_text('2024-03-07.txt')
    parser(test_data)