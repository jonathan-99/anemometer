#!/usr/bin/env python3

"""A collection of all functions for this program."""
try:
    import datetime
    import os
    import sys
    import csv
    import json
    import logging
    import re
    from src.class_file import ConfigData
    from collections import namedtuple
    import src.weather_class as weather_data_object
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def get_config() -> ConfigData:
    """
    Get the config from a json file and return an object class of that data.
    """

    ConfigData.error_trapping()
    config_object = ConfigData()

    logging.debug('We found these configs: ' + str(config_object.show_all()))
    print("All config data: ", config_object.show_all())
    return config_object


def get_yesterdays_date() -> str:
    """
    Simple function for getting yesterday's date.
    :return String:
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    logging.debug(("Yesterday is: " + str(yesterday)[0:10]))
    return str(yesterday)[0:10]


def get_todays_date() -> datetime:
    """
    Get date for a filename.
    """
    output = datetime.datetime.now()
    return 'data/' + output.strftime("%Y-%m-%d") + '.txt'


def create_weather_list(in_str: str) -> weather_data_object:
    """
    This creates a list of weather objects if there are multiple instances. Returns list.
    """

    output_list = weather_data_object.WeatherData()
    temp_list = in_str.replace("'", "").split(',')
    for i in range(0, len(temp_list), 2):
        print("create_list() - index number {}".format(i))
        output_list.eventTime = temp_list[i]
        output_list.windSpeed = temp_list[i + 1]
    return output_list


def file_handler(time_stamp: str, speed: float, filename='data/file.txt') -> str:
    """
    Open a file in "data" folder and add a time (now) and wind speed only.
    This function does not check vailidty of data.
    This function does not accept lists of multiple weatherData.
    :param: time_stamp(2022-07-26 21): str
    :param: speed(12.2): float
    :param: filename(data/2022-07-26): str
    :return: string("True" or Error message as str): str
    """
    logging.debug("file_handler()")

    try:
        logging.debug(f"Opening file, " + str(filename))
        print("file opening - {}".format(filename))
        with open(filename, 'a+') as fileObject:
            print("file_handler() - type {} - speed {}".format(type(speed), speed))
            fileObject.write(f"{time_stamp},{speed},\n")
            logging.debug(f'File added to in file_handler()')
    except FileExistsError or FileNotFoundError as err:
        return_string = 'Exception error in file_handler() - {}'.format(str(err))
        logging.error(return_string, exc_info=True)
        return return_string
    return "True"


def read_in_data(filename: str) -> list:
    """
    Read in data from csv file.
    """
    logging.debug("Read_in_data from " + filename)

    output = []
    try:
        file = open(filename)
        reader = csv.reader(file)
        for each_row in reader:
            output.append(each_row)
        file.close()
    except Exception as err:
        logging.error("Reading in csv data error: " + str(err))
    return output


def handle_input_list_datetime(in_list: list,
                               input_regex='([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])') -> list:
    """
    If the datetime is not correct format such as "YY-MM-DD H:m:s.xxx" then it will convert it to the correct.

    This will create duplicates of HOURS and need to be resolved.
    This needs to extract the date regex out to config.

    :param: input_list (list) : description
    :param: correct_date_regex (str) : description
    :param: incorrect_date_regex (str) : description
    :return: input_list (list) : description
    """
    correct_date_regex = '([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])'
    incorrect_date_regex = '([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)'

    p = re.compile(correct_date_regex)
    for count, value in enumerate(in_list):
        m = p.match(value)
        if m:
            pass
        else:
            result = value.split('.')[0].split(':')[0]
            in_list[count] = result
    return in_list


def split_list(input_list: list):  # how to declare two list returns?
    """
    This will take data in str format "YY-MM-DD HH speed.value" and return into (datetime, str).

    :return: list -> WeatherData(datetime, str)
    """
    logging.debug("reformat_data for plotting")

    local_x = []
    local_y = []

    logging.debug("input list " + str(input_list))
    for counter, g in enumerate(input_list):
        if counter % 2 == 0:
            gl = g[0:13]
            local_x.append(gl)
        else:
            local_y.append(str(g))
    logging.debug("X axis values: " + str(local_x))
    logging.debug("Y axis values: " + str(local_y))

    return local_x, local_y
