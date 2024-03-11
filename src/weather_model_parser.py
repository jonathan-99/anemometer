import sys
import requests
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

def post_json_data(json_data, url):
    try:
        response = requests.post(url, json=json_data)
        response.raise_for_status()
        print("JSON data posted successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python3 script.py <IP_address> <port> [<filename>]")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = sys.argv[2]
    filename = sys.argv[3] if len(sys.argv) == 4 else '2024-03-07.txt'
    url = f"http://{ip_address}:{port}/api/data"

    test_data = extract_csv_from_text(filename)
    parsed_data = parser(test_data)
    post_json_data(parsed_data, url)
