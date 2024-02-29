#!/usr/bin/env python3

"""A collection of all functions for this program."""

import datetime
import os
import re
import logging
from ..src import file_handler_class as file_handler_class


def error_trapping():
    """Check file locations for errors."""
    file_locations = [
        "~../src/config.json",
        "~../config.json",
        "~src/config.json",
        "~config.json",
        "config.json",
        "~anemometer/src/config.json",
        "~/anemometer/src/config.json",
        "~opt/anemometer/src/config.json",
        "~/opt/anemometer/src/config.json",
        "~../opt/anemometer/src/config.json",
        "~../../opt/anemometer/src/config.json",
        "~../../../opt/anemometer/src/config.json",
        "~../../../~/opt/anemometer/src/config.json",
    ]
    for file_location in file_locations:
        logging.debug(f"Check json file file_location - {os.path.exists(file_location)} - {file_location}")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logging.debug(f"You are here -- {dir_path}")


def file_handler(time, speed, filename):
    """Handle file operations."""
    file_handler_object = file_handler_class.FileHandlerClass(filename)
    file_handler_object.append_specific_file_with_singular_weather_data(time, speed, filename)


def get_yesterdays_date() -> str:
    """Get yesterday's date."""
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    logging.debug(f"Yesterday is: {str(yesterday)[0:10]}")
    return str(yesterday)[0:10]


def get_weather_data(filename='data/2022-11-03.txt') -> list:
    """Get weather data."""
    file_object = file_handler_class.FileHandlerClass(filename)
    file_object.read_specific_csv_file(filename)
    return file_object.get_weather_data_list()


def get_todays_date() -> str:
    """Get today's date."""
    output = datetime.datetime.now()
    return f"data/{output.strftime('%Y-%m-%d')}.txt"


# def create_weather_list(in_str: str) -> weather_data_object:
#    """Create a list of weather objects."""
#    output_list = weather_data_object.WeatherData()
#    temp_list = in_str.replace("'", "").split(',')
#    for i in range(0, len(temp_list), 2):
#        logging.debug(f"Create list() - index number {i}")
#        output_list.eventTime = temp_list[i]
#        output_list.windSpeed = temp_list[i + 1]
#    return output_list


def check_date_format(date_list: list) -> list:
    """
    Iterate through a list of dates and check if they are in the specified format.

    Args:
        date_list (list): List of dates to be checked.

    Returns:
        list: List of dates that match the specified format.
    """
    valid_dates = []
    date_pattern = r"\d{4}-\d{2}-\d{2} \d{2}(:\d{2}){1,2},\d+\.\d+"

    for date in date_list:
        # Check if the date includes time with microseconds
        if re.match(date_pattern, date):
            # Extract only the hour part
            hour_only = date.split()[1].split(":")[0]
            # Reconstruct the date with only the hour part
            corrected_date = date.split()[0] + " " + hour_only + ","
            valid_dates.append(corrected_date)
        else:
            valid_dates.append(date)

    return valid_dates


def iterate_through_list_for_good_datetime(in_list: list) -> list:
    """Correct datetime against a regex."""
    return check_date_format(in_list)


def split_list(input_list: list) -> tuple:
    """Split data into datetime and speed."""
    local_x = []
    local_y = []
    for counter, g in enumerate(input_list):
        if counter % 2 == 0:
            gl = g[0:13]
            local_x.append(gl)
        else:
            local_y.append(str(g))
    logging.debug(f"X axis values: {local_x}")
    logging.debug(f"Y axis values: {local_y}")
    return local_x, local_y


def handle_input_list_datetime(actual_date: list) -> list:
    """Handle input list datetime."""
    return [date[:13] for date in actual_date]


def create_html_page_wrapper(title: str) -> tuple:
    """Create HTML page wrapper."""
    return f"<html><head><title>{title}</title></head><body>", "</body></html>"
