import logging
import sys
import os
import requests
from marshmallow import ValidationError
import json
import class_weather_model as model


def parser(input_data) -> json:
    logging.debug(f'parser()')
    try:
        # Parse JSON string to dictionary if data is a string
        if isinstance(input_data, str):
            temp_data = json.loads(input_data)

        # Initialize an empty list to store the parsed CSV data
        temp_parsed_data = []

        # Iterate over each entry in the 'weatherConfiguration' section of the data
        for entry in temp_data['weatherConfiguration']:
            # Create a dictionary with the required fields for each entry
            entry_dict = {
                'timestamp': entry['timestamp'],
                'speed': entry['speed']
            }
            # Append the dictionary to the parsed data list
            temp_parsed_data.append(entry_dict)

        # Return the parsed data
        return temp_parsed_data
    except ValidationError as err:
        error_info = {
            'messages': err.messages,
            'data': err.data,
            'field_name': err.field_name,
            'valid_data': err.valid_data
        }
        logging.error(f'ValidationError - {error_info}')
        return json.dumps(error_info)


def extract_csv_from_text(file_path) -> json:
    logging.debug(f'extract_csv_from_text() - {file_path}')
    csv_data = {'weatherConfiguration': []}  # Initialize as a dictionary
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by comma to get key-value pairs
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    timestamp, speed = parts[:2]  # Take only the first two elements
                    # Append a dictionary representing each entry to the 'weatherConfiguration' list
                    csv_data['weatherConfiguration'].append(
                        {'timestamp': timestamp.strip(), 'speed': float(speed.strip())})
                else:
                    logging.error(f"Ignored line: {line.strip()}")  # Log lines with more or fewer than 2 elements
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        logging.error(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")

    # Convert the dictionary to a JSON string
    json_data = json.dumps(csv_data)
    logging.info(f'extract data from csv to json() - {json_data}')
    return json_data


def post_json_data(json_data, input_url):
    logging.debug(f'post_json_data() - {input_url} - {json_data}')
    try:
        response = requests.post(input_url, json=json_data)
        print(f' here - {response.raise_for_status()}')
        print("JSON data posted successfully.")
        logging.debug(f'JSON POSTed them - {response.raise_for_status()}')
    except requests.exceptions.ConnectionError as err:
        logging.error(f'Connection error - {err}')
        print(f'Connection error - {err}')
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        logging.error(f'HTTP Error - {err}')
    except requests.exceptions.RequestException as err:
        logging.error(f'RequestException - {err}')
        print(f"Request Exception: {err}")


def get_absolute_path(local_filename):
    # If the filename is provided without a path, assume it is in the 'data' directory
    if not os.path.isabs(local_filename):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        data_dir = data_dir.replace('\\src', '')
        local_filename = os.path.join(data_dir, local_filename)
    return local_filename


def print_pretty_json(input_data):
    try:
        # Convert the parsed data to JSON with indentation for better readability
        pretty_json = json.dumps(input_data, indent=2)
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
        logging.error(f"File '{filename}' not found. Exiting.")
        sys.exit(1)

    url = f"http://{ip_address}:{port}/api/data"

    print(f"Attempting to parse data from file: {filename}")
    data = extract_csv_from_text(filename)
    parsed_data = parser(data)
    post_json_data(parsed_data, url)
