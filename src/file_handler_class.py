import os
import csv
import json
import logging

try:
    import src.weather_class as weather_class
    import ast
except Exception as e:
    logging.error("Importing packages error: {}".format(e))


class FileHandlerClass:

    def __init__(self, name: str) -> None:
        self.filename = name
        self.directory = None
        self.files_in_directory = []
        self.weatherDataList = []
        logging.debug("FileHandlerClass initiated")

    def _append_weather_data_singular_to_list(self, time, speed) -> None:
        self.weatherDataList.append((time, speed))

    def get_weather_data_list(self) -> list:
        return self.weatherDataList

    @staticmethod
    def append_specific_file_with_singular_weather_data(time_stamp, speed, filename='data/2022-07-26.txt') -> None:
        logging.debug(f"Opening file, {filename}")
        try:
            with open(filename, 'a+') as fileObject:
                fileObject.write(f"{time_stamp},{speed},\n")
                logging.debug('File added to in file_handler()')
        except (FileExistsError, FileNotFoundError) as err_1:
            logging.error(f'Exception error in file_handler() - {str(err_1)}', exc_info=True)
        except Exception as err_2:
            logging.error(f'Unknown exception error in file_handler() - {str(err_2)}', exc_info=True)

    def read_specific_weather_file(self, filename="data/2022-07-26.txt") -> None:
        logging.debug("read_specific_weather_file()")
        try:
            with open(filename, 'r') as fileObject:
                input_data = fileObject.read()
                logging.debug(f"read_specific_weather_file(): {input_data[0]}, len({len(input_data)})")
                for i in range(0, len(input_data), 2):
                    self._append_weather_data_singular_to_list(input_data[i], input_data[i + 1])
                logging.debug(f"read_specific_weather_file({filename})")
        except (FileExistsError) as err_1:
            error = str(os.listdir('.'))
            logging.error(f'FileExistsError in file_handler() - {str(err_1)} - {error}', exc_info=True)
        except (FileNotFoundError) as err_2:
            error = str(os.listdir('.'))
            logging.error(f'FileNotFoundError in file_handler() - {str(err_2)} - {error}', exc_info=True)
        except Exception as err:
            error = str(os.listdir('.'))
            logging.error(f'Randon exception error in file_handler() - {str(err)} - {error}', exc_info=True)

    def read_specific_csv_file(self, filename) -> None:
        self.filename = filename
        try:
            with open(self.filename, 'r') as file_object:
                csv_reader = csv.reader(file_object, delimiter=',')
                logging.debug("read_specific_csv_file()")
                for i, row in enumerate(csv_reader):
                    if i % 2 == 0:
                        self._append_weather_data_singular_to_list(row[0], row[1])
        except (FileExistsError) as err_1:
            error = str(os.listdir('.'))
            logging.error(f'FileExistsError in file_handler() - {str(err_1)} - {error}', exc_info=True)
        except (FileNotFoundError) as err_2:
            error = str(os.listdir('.'))
            logging.error(f'FileNotFoundError in file_handler() - {str(err_2)} - {error}', exc_info=True)
        except Exception as err:
            error = str(os.listdir('.'))
            logging.error(f'Randon exception error in file_handler() - {str(err)} - {error}', exc_info=True)

    def add_files_in_directory(self, directory='data/') -> list:
        for a_file in os.listdir(directory):
            extension = os.path.splitext(a_file)
            self.files_in_directory.append(extension[0])
        return self.files_in_directory

    def get_files_in_directory(self) -> list:
        return self.files_in_directory

    @staticmethod
    def read_json_data_from_file(filename: str) -> json:
        try:
            data = [json.loads(line) for line in open(filename, 'r')]
            print(f"Data contents: {data}")
            return data
        except (FileExistsError, FileNotFoundError) as err:
            logging.error(f"Getting config error: {str(err)}")
            return {"Error:": str(err)}
        except json.decoder.JSONDecodeError as err_1:
            logging.error(f"Error. JSONDecodeError. Possibly you have a special character - {err_1}")
            return {"Error 1:": str(err_1)}
