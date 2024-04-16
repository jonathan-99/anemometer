import logging
import sys
import os
import requests
from marshmallow import ValidationError
import json
from src.class_weather_model import WeatherModelSchema as Model
import socket
from datetime import datetime


def extract_date_filename(file_path):
    try:
        # Extract the filename from the file path
        used_filename = os.path.basename(file_path)
        logging.debug(f'extract_date_filename() filename - {filename}')
        return used_filename
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None


def convert_extracted_file_to_model(input_data: dict, input_filename: str) -> dict:
    """
    This function takes the text file csv data of weather (datetime and speed) which has been converted into
    a json format. Uses Marshmallow to create the standard model and embed the weather data into it.

    :param input_data: JSON formatted weather data
    :type input_data: dict
    :param input_filename: Name of the input file
    :type input_filename: str
    :return: Weather model embedded with the data
    :rtype: dict
    """
    logging.debug(f'convert extracted file to model - data - {input_filename}')
    output_filename = extract_date_filename(input_filename)
    hostname = socket.gethostname()
    internal_ip_address = socket.gethostbyname(hostname)
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename_without_extension = input_filename.split('.')[0]

    temp_data = []
    try:
        # Parse JSON string to dictionary if data is a string
        if isinstance(input_data, str):
            temp_data = json.loads(input_data)
        elif isinstance(input_data, dict):
            temp_data = input_data
        else:
            logging.error("Invalid input_data format")

        # Convert the input data to a list of dictionaries
        data_list = []
        for line in temp_data.get('data', []):  # Access 'data' key safely
            timestamp, speed = line.get('timestamp', ''), line.get('speed',
                                                                   '')  # Access 'timestamp' and 'speed' keys safely
            data_list.append({"timestamp": timestamp, "speed": speed})

        # Create the model data dictionary
        model_data = {
            "weatherData": {
                "metadata": {
                    "version": 1.0,
                    "date_recorded": output_filename,
                    "date_transmitted": current_date,
                    "filename": filename_without_extension,
                    "src_ip": internal_ip_address,
                    "hostname": hostname
                },
                "data": data_list  # Include the converted data list
            },
            "relationship": {},  # Initialize 'relationship'
            "validation": {  # Initialize 'validation' with its rules
                "version_validation": "[0-9]*.[0-9][0-9]",
                "date_recorded_validation": "^\\d{4}\\s\\d{2}\\s\\d{2}\\s\\d{2}$",
                "date_transmitted_validation": "^\\d{4}\\s\\d{2}\\s\\d{2}\\s\\d{2}$",
                "filename_validation": "[2-9][0-9][0-9][0-9]-[0-1][0-2].txt",
                "src_ip": "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b",
                "hostname_validation": "[0-9a-z]+",
                "speed_validation": "[0-9]*.[0-9]*"
            }
        }

        # Return the model data
        logging.debug(f'model_data - {model_data}')
        return model_data
    except ValidationError as err:
        error_info = {
            'messages': err.messages,
            'data': err.data,
            'field_name': err.field_name,
            'valid_data': err.valid_data
        }
        logging.error(f'ValidationError - {error_info}')
        logging.error(json.dumps(error_info))
    return {'need': 'something better'}  # this whole function needs refactoring.


def extract_csv_from_text(file_path) -> json:
    logging.debug(f'extract_csv_from_text() - {file_path}')
    csv_data = {'data': []}  # Initialize as a dictionary
    try:
        # Normalize the file path
        normalized_file_path = os.path.normpath(file_path)

        # Get the absolute path to the file
        abs_file_path = os.path.abspath(normalized_file_path)

        with open(abs_file_path, 'r') as file:
            for line in file:
                # Split each line by comma to get key-value pairs
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    timestamp, speed = parts[:2]  # Take only the first two elements
                    # Append a dictionary representing each entry to the 'data' list
                    csv_data['data'].append(
                        {'timestamp': timestamp.strip(), 'speed': float(speed.strip())})
                else:
                    logging.error(f"Ignored line: {line.strip()}")  # Log lines with more or fewer than 2 elements
    except FileNotFoundError as e:
        logging.error(f"File '{file_path}' not found: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

    # Convert the dictionary to a JSON string
    json_data = json.dumps(csv_data, indent=4)
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
        logging.debug(f'data_dir - {data_dir}')
        data_dir = data_dir.replace('\\src', '')
        local_filename = os.path.join(data_dir, local_filename)
        logging.debug(f'local_filename - {local_filename}')
    return local_filename


def print_pretty_json(input_data):
    try:
        # Convert the parsed data to JSON with indentation for better readability
        pretty_json = json.dumps(input_data, indent=2)
        print(f'Parsed Data - {pretty_json}')
    except Exception as e:
        logging.error(f"An error occurred while printing JSON data: {str(e)}")


def run_parser(this_ip_address: str, this_port: int, internal_filename='2024-03-07.txt'):
    """
    This is a simple function to execute the code, aimed at the super-argparse file of anemometer.
    """
    # Remove single quotes from the filename if present
    internal_filename = internal_filename.strip("'")

    # Get the absolute file path
    internal_filename = get_absolute_path(internal_filename)

    if not os.path.isfile(internal_filename):
        logging.debug(f"File '{internal_filename}' not found. Exiting.")
        logging.error(f"File '{internal_filename}' not found. Exiting.")
        sys.exit(1)

    this_url = f"http://{this_ip_address}:{this_port}/api/data"

    logging.info(f"Attempting to parse data from file: {internal_filename}")
    this_data = extract_csv_from_text(internal_filename)
    this_parsed_data = convert_extracted_file_to_model(this_data, internal_filename)
    print_pretty_json(this_parsed_data)
    post_json_data(this_parsed_data, this_url)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        logging.debug("Usage: python3 script.py <IP_address> <port> [<filename>]")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = sys.argv[2]
    filename = sys.argv[3] if len(sys.argv) == 4 else '2024-03-07.txt'

    # Remove single quotes from the filename if present
    filename = filename.strip("'")

    # Get the absolute file path
    filename = get_absolute_path(filename)

    if not os.path.isfile(filename):
        logging.error(f"File '{filename}' not found. Exiting.")
        sys.exit(1)

    url = f"http://{ip_address}:{port}/api/data"

    print(f"Attempting to parse data from file: {filename}")
    data = extract_csv_from_text(filename)
    parsed_data = convert_extracted_file_to_model(data, filename)
    print_pretty_json(parsed_data)
    post_json_data(parsed_data, url)
