#!/usr/bin/env python3
import os
import csv
import json
import logging
import sys

import src.weather_class as weather_class
import src.class_file as ConfigData


class FileHandlerClass:

    def __init__(self, name: str) -> None:
        try:
            self._filename = name
            self._directory = self._get_config_path()
            self._files_in_directory = []
            self._weatherDataList = []
            logging.debug("FileHandlerClass initiated")
        except Exception as e:
            logging.error(f"Initialization error: {e}")

    def get_filename(self) -> str:
        return self._filename

    def set_filename(self, name: str) -> None:
        self._filename = name

    def get_directory(self) -> str:
        return self._directory

    def set_directory(self, path: str) -> None:
        self._directory = path

    def get_files_in_directory(self) -> list:
        return self._files_in_directory

    def append_files_in_directory(self, file: str) -> None:
        self._files_in_directory.append(file)

    def set_files_in_directory(self, files: list) -> None:
        self._files_in_directory = files

    def get_weather_data_list(self) -> list:
        return self._weatherDataList

    def set_weather_data_list(self, data: list) -> None:
        self._weatherDataList = data

    def _get_config_path(self) -> str:
        try:
            self._change_directory_if_file_not_found('config.json')
            config_object = ConfigData.ConfigData('config.json')
            return str(config_object.get_path())
        except Exception as e:
            logging.error(f"Error getting config path: {e}")

    def _change_directory_if_file_not_found(self, filename: str) -> None:
        try:
            if sys.platform.startswith('linux'):
                if not os.path.exists(filename):
                    logging.warning(f"File not found: {filename}")
                    logging.warning("Changing directory to ~/opt/anemometer/")
                    os.chdir(os.path.expanduser("~/opt/anemometer/"))
                    logging.info(f"Current working directory changed to: {os.getcwd()}")
            else:
                raise NotImplementedError(f"{sys.platform} platform is not supported.")
        except NotImplementedError as e:
            logging.error(f"NotImplementedError: {e}")

    def _append_weather_data_singular_to_list(self, time, speed) -> None:
        try:
            self._weatherDataList.append((time, speed))
        except Exception as e:
            logging.error(f"Error appending weather data: {e}")

    def append_specific_file_with_singular_weather_data(self,
                                                        time_stamp, speed, filename='data/2022-07-26.txt') -> None:
        try:
            logging.debug(f"Opening file {filename} with absolute path {self._directory}.")
            self._change_directory_if_file_not_found(filename)
            with open(os.path.join(self._directory, filename), 'a+') as fileObject:
                fileObject.write(f"{time_stamp},{speed},\n")
                logging.debug('File added to in file_handler()')
        except Exception as e:
            logging.error(f"Error appending weather data to file: {e}")

    def read_specific_weather_file(self, filename="data/2022-07-26.txt") -> None:
        try:
            logging.debug("read_specific_weather_file()")
            self._change_directory_if_file_not_found(filename)
            with open(os.path.join(self._directory, filename), 'r') as fileObject:
                input_data = fileObject.read()
                logging.debug(f"read_specific_weather_file(): {input_data[0]}, len({len(input_data)})")
                for i in range(0, len(input_data), 2):
                    self._append_weather_data_singular_to_list(input_data[i], input_data[i + 1])
                logging.debug(f"read_specific_weather_file({filename})")
        except Exception as e:
            logging.error(f"Error reading specific weather file: {e}")

    def read_specific_csv_file(self, filename) -> None:
        try:
            self._filename = filename
            self._change_directory_if_file_not_found(filename)
            with open(os.path.join(self._directory, filename), 'r') as file_object:
                csv_reader = csv.reader(file_object, delimiter=',')
                logging.debug("read_specific_csv_file()")
                for i, row in enumerate(csv_reader):
                    if i % 2 == 0:
                        self._append_weather_data_singular_to_list(row[0], row[1])
        except Exception as e:
            logging.error(f"Error reading specific CSV file: {e}")

    def add_files_in_directory(self, directory='data/') -> list:
        if not self._files_in_directory:
            try:
                files = []
                for root, _, filenames in os.walk(directory):
                    for filename in filenames:
                        files.append(os.path.splitext(filename)[0])
                return files
            except Exception as e:
                logging.error(f"Error adding files in directory: {e}")
        else:
            pass

    def read_json_data_from_file(self, filename: str) -> json:
        try:
            self._change_directory_if_file_not_found(filename)
            data = [json.loads(line) for line in open(os.path.join(self._directory, filename), 'r')]
            print(f"Data contents: {data}")
            return data
        except Exception as e:
            logging.error(f"Error reading JSON data from file: {e}")
