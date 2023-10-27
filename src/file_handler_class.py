try:
    import os
    import sys
    import csv
    import json
    import logging
    import src.weather_class as weather_class
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class FileHandlerClass:

    def __init__(self, name: str) -> None:
        self.filename = name
        self.directory = None
        self.files_in_directory = []
        self.weatherDataList = []

    def _append_weather_data_singular_to_list(self, time, speed) -> None:
        self.weatherDataList.append((time, speed))

    def get_weather_data_list(self) -> list:
        return self.weatherDataList
    def append_specific_file_with_singular_weather_data(self, time_stamp, speed, filename='data/2022-07-26.txt') -> None:
        """
            Open a file in "data" folder and add a time (now) and wind speed only.
            This function does not check validity of data.
            This function does not accept lists of multiple weatherData.
            :param: time_stamp(2022-07-26 21): str
            :param: speed(12.2): float
            :param: filename(data/2022-07-26): str
            :return: string("True" or Error message as str): str
        """
        logging.debug(f"Opening file, " + str(filename))
        try:
            print("file_handler({}) - type {} - speed {}".format(filename, type(speed), speed))
            with open(filename, 'a+') as fileObject:
                fileObject.write(f"{time_stamp},{speed},\n")
                logging.debug(f'File added to in file_handler()')
        except FileExistsError or FileNotFoundError as err:
            logging.error('Exception error in file_handler() - {}'.format(str(err)), exc_info=True)


    def read_specific_weather_file(self, filename="data/2022-07-26.txt") -> None:
        try:
            with open(filename, 'r') as fileObject:
                input_data = fileObject.read()
                logging.debug("read_specific_weather_file(): 0{}, len({})".format(input_data[0], len(input_data)))
                for i in range(0, len(input_data), 2):
                    self._append_weather_data_singular_to_list(input_data[i], input_data[i + 1])
                logging.debug("read_specific_weather_file({})".format(filename))
        except FileExistsError or FileNotFoundError as err:
            logging.error('Exception error in file_handler() - {}'.format(str(err)), exc_info=True)

    def read_specific_csv_file(self, filename) -> None:
        self.filename = filename
        temp_list = []
        try:
            file_object = open(self.filename, 'r')
            temp_list = list(csv.reader(file_object, delimiter=','))
            r = range(0, len(temp_list), 2)
            logging.debug("read_specific_csv_file(): 0, len()")
            for i in r:
                self._append_weather_data_singular_to_list(temp_list[i], temp_list[i + 1])
            file_object.close()
        except Exception as err:
            logging.error("Reading in csv data error: " + str(err))
        return

    def add_files_in_directory(self, directory='data/') -> list:
        for a_file in os.listdir(directory):
            extension = os.path.splitext(a_file)
            self.files_in_directory.append(extension[0])
        return self.files_in_directory

    def get_files_in_directory(self) -> list:
        return self.files_in_directory
