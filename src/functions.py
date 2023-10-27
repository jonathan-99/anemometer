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
    import src.file_handler_class as file_handler_class
    import src.date_checking_class as date_checking_class
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


def file_handler(time, speed, filename):
    file_handler_object = file_handler_class.FileHandlerClass(filename)
    file_handler_object.append_specific_file_with_singular_weather_data(time, speed, filename)


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


def iterate_through_list_for_good_datetime(in_list: list) -> list:
    """
    Take a list of datetimes and correct against a regex, before returning the corrected list
    :in_list: list: input list
    """
    date_checking_object = date_checking_class.DateCheckingClass
    output_list = date_checking_object.correct_datetime_against_regex(in_list)
    return output_list


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
