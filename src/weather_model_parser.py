import sys
import os
import requests
from marshmallow import ValidationError
import re
import json
import class_weather_model as model


def parser(data):
    try:
        # Initialize an empty list to store the parsed CSV data
        parsed_data = []

        # Iterate over each entry in the 'weatherConfiguration' section of the data
        for entry in data['weatherConfiguration']:
            # Create a dictionary with the required fields for each entry
            entry_dict = {
                'timestamp': entry['timestamp'],
                'value': entry['value']
            }
            # Append the dictionary to the parsed data list
            parsed_data.append(entry_dict)

        # Return the parsed data
        return parsed_data
    except ValidationError as err:
        error_info = {
            'messages': err.messages,
            'data': err.data,
            'field_name': err.field_name,
            'valid_data': err.valid_data
        }
        return json.dumps(error_info)



def extract_csv_from_text(file_path):
    csv_data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by comma to get key-value pairs
                parts = line.strip().split(',')
                print(f'extract_csv_from_text() - parts - {parts}')
                if len(parts) == 2:
                    key, value = parts
                    csv_data[key.strip()] = float(value.strip())
                    print(f'extract_csv_from_text() - csv_data - {csv_data}')
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return csv_data




def post_json_data(json_data, url):
    print(f'post_json_data() - {url} - {json_data}')
    try:
        response = requests.post(url, json=json_data)
        response.raise_for_status()
        print("JSON data posted successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")


def get_absolute_path(filename):
    # If the filename is provided without a path, assume it is in the 'data' directory
    if not os.path.isabs(filename):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        data_dir = data_dir.replace('\\src', '')
        filename = os.path.join(data_dir, filename)
    return filename

def print_pretty_json(parsed_data):
    try:
        # Convert the parsed data to JSON with indentation for better readability
        pretty_json = json.dumps(parsed_data, indent=2)
        print("Parsed Data:")
        print(pretty_json)
    except Exception as e:
        print(f"An error occurred while printing JSON data: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python3 script.py <IP_address> <port> [<filename>]")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = sys.argv[2]
    filename = sys.argv[3] if len(sys.argv) == 4 else '2024-03-07.txt'

    # Remove single quotes from the filename if present
    filename = filename.strip("'")

    # Get the absolute file path
    filename = get_absolute_path(filename)

    if not os.path.isfile(filename):
        print(f"File '{filename}' not found. Exiting.")
        sys.exit(1)

    url = f"http://{ip_address}:{port}/api/data"

    print(f"Attempting to parse data from file: {filename}")
    csv_data = extract_csv_from_text(filename)
    print("Data extraction successful.")

    # Wrap the CSV data in a dictionary
    data = {'weatherConfiguration': csv_data}
    print(f'data - {data}')

    print("Attempting to parse data...")
    parsed_data = parser(data)
    print("Data parsing successful.")

    # Print the parsed data in a beautiful JSON format
    print_pretty_json(parsed_data)

    print("Attempting to post JSON data...")
    post_json_data(parsed_data, url)
