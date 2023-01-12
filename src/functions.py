#!/usr/bin/env python3

"""A collection of all functions for this program."""
try:
    import datetime
    import os
    import sys
    import csv
    import json
    import numpy as np
    import logging
    import re
    from src.class_file import config_data
    from collections import namedtuple
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def get_config() -> config_data:
    """
    Get the config from a json file and return an object class of that data.
    """
    location = "config.json"
    config_data_object = config_data()

    if location.lower().endswith('.json'):
        try:
            with open(location) as fileObject:
                data = json.load(fileObject)
            config_data_object.set_path(data["path"])
            config_data_object.set_logging_path(data["logging_path"])
            config_data_object.set_log_filename(data["log_filename"])
            config_data_object.set_data_location(data["data_path"])
            config_data_object.set_server_port(data["simple-server-port"])
            config_data_object.set_logging_level(["logging-level"])
        except FileExistsError or FileExistsError as err:
            logging.error("Getting config error: " + str(err))
    else:
        print("was expecting json as a config file")
        config_data_object.set_path()
        config_data_object.set_logging_path()
        config_data_object.set_log_filename()
        config_data_object.set_data_location()
        config_data_object.set_server_port()
        config_data_object.set_logging_level()
    logging.debug("We found these configs: " + str(config_data_object.show_all()))
    return config_data_object


def listing_directory(page_name: str) -> str:
    """This lists all files in a specified directory, then outputs it as a string of html tags, ready for rendering."""
    logging.debug("Listing directory accessed")

    alist, name_newest_file = list_file_directory()
    blist = row_major(alist, len(alist))
    clist = html_table(blist)
    c = ""
    for cl in clist:
        c += cl
    start, end = create_html_page_wrapper(page_name)
    return start + c + end


def create_html_page_wrapper(name: str) -> tuple:
    """
    Need the start and end of a html page.
    :return: str, str
    """
    config = get_config()
    total_path = config.get_path() + config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())
    logging.debug("create_html_page_wrapper with " + name)
    title = "<!DOCTYPE html><head><title>" + name
    title += "</title></head><body>"
    end_tags = "</body></html>"
    return title, end_tags


def row_major(alist: list, sublen: int) -> list:
    """
    Not quite sure of this yet
    :param alist: list
    :param sublen: int
    :return:
    """
    return [alist[i:i+sublen] for i in range(0, len(alist), sublen)]


def html_table(input_value) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    logging.debug("html_table")

    output = ['<table>']
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('</td><td>'.join(sublist))
        output.append('</td></tr>')
    output.append('</table>')
    return output


def get_newest_file(input_list: list) -> str:
    logging.debug("get_newest_file")

    for value in range(-1, 30, 1):
        check_day = datetime.datetime.now() - datetime.timedelta(value)
        test_day = str(check_day)[0:10]+".txt"
        if test_day in input_list:
            output_date = test_day
            logging.debug("Most current file: " + str(output_date))
            return output_date
        else:
            logging.debug("Need to go back further in get_newest_file() to find newest file")
    return "No file found"


def list_file_directory(directory="data/") -> tuple:
    """
    Search through 'data' folder for all names of files and return them in a string. This will enable
    the index.html file to list them safely for a browser
    :param directory: str
    :return: list
    """
    logging.debug("list_file_directory from directory: " + str(directory))

    list_of_files = []
    for path in os.listdir(directory):
        # check if current path is a file
        if os.path.isfile(os.path.join(directory, path)):
            list_of_files.append(path)
    output_file_name = get_newest_file(list_of_files)
    output_tuple = namedtuple("Directory", ["list_of_files", "output_file_name"])
    logging.debug("list of files: " + output_tuple["list_of_files"] + "and newest file: " + output_file_name)
    return output_tuple(list_of_files, output_file_name)


def get_yesterdays_date() -> str:
    """
    Simple function for getting yesterday's date.
    :return String:
    """
    config = get_config()
    total_path = config.get_path() + config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    logging.debug(("Yesterday is: " + str(yesterday)[0:10]))
    return str(yesterday)[0:10]


def file_handler(input_data) -> None:
    """
    Open a file in "data" folder and add a time (now) and wind speed.
    :param: input_data: float
    :return: None: # should this be a boolean for success / failure?
    """
    logging.debug("file_handler")

    try:
        today = datetime.datetime.today()
        temp_filename = str('data/') + today.strftime("%Y-%m-%d") + ".txt"
        logging.debug(f"Opening file, " + str(temp_filename))
        with open(temp_filename, 'a+') as fileObject:
            time_stamp = str(datetime.datetime.now().strftime("%Y %m %d %H:%M:%S"))
            fileObject.write(f"{time_stamp},{input_data},\n")
            logging.debug(f"File added to in file_handler()")
    except FileExistsError or FileNotFoundError as err:
        logging.error("Exception error in file_handler()" + str(err), exc_info=True)
    return


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


def handle_input_list_datetime(in_list: list, correct_date_regex: str) -> list:
    """
    Handle Input List accounts for an incorrect date plus hour format being passed in the list
    from the original text file.
    It converts it to the correct version if necessary and returns to the original list.
    : param: input_list (list) : description
    : param: correct_date_regex (str) : description
    : param: incorrect_date_regex (str) : description
    : return: input_list (list) : description
    """

    p = re.compile(correct_date_regex)
    for count, value in enumerate(in_list):
        m = p.match(value)
        if m:
            pass
        else:
            result = value.split('.')[0].split(':')[0]
            in_list[count] = result
    return in_list


def reformat_data(input_list: list):  # how to declare two list returns?
    """
    This will take data in str format "YY-MM-DD HH" and return into (datetime, str). If the datetime is
    not correct format such as "YY-MM-DD H:m:s.xxx" then it will convert it to the correct.

    This will create duplicates of HOURS and need to be resolved.

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

    correct_date_regex = '([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])'
    incorrect_date_regex = '([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)'
    local_x = handle_input_list_datetime(local_x, correct_date_regex)
    return local_x, local_y
