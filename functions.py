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
    from class_file import config_data
    from collections import namedtuple
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def get_config(self, location="config.json", type_of_file="json") -> config_data:
    """
    Get the config from a json file and return an object class of that data.
    """
    config_data_object = config_data()
    print("Path debug default ", location)
    if type_of_file == "json":
        try:
            f = open("opt/anemometer/" + location)
            data = json.load(f)
            f.close()
            config_data_object.set_path(data["path"])
            config_data_object.set_logging_location(data["logging"])
            config_data_object.set_data_location(data["data"])
            config_data_object.set_server_port(data["simple-server-port"])
            config_data_object.set_logging_level(["logging-level"])
        except FileExistsError or FileExistsError as err:
            logging.error("Getting config error: " + str(err))
    else:
        print("was expecting json as a config file")
        config_data_object.set_path()
        config_data_object.set_logging_location()
        config_data_object.set_data_location()
        config_data_object.set_server_port()
        config_data_object.set_logging_level()
    logging.debug("We found these configs: " + str(config_data_object.show_all()))
    return config_data_object


def listing_directory(page_name: str) -> str:
    """This lists all files in a specified directory, then outputs it as a string of html tags, ready for rendering."""
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + str(config.get_logging_location()), level=config.get_logging_level())
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
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
    logging.debug("create_html_page_wrapper with " + name)
    title = "<!DOCTYPE html><head><title>" + name
    title += "</title></head><body>"
    end_tags = "</body></html>"
    return title, end_tags


def row_major(alist, SubLen) -> list:
    """
    Not quite sure of this yet
    :param alist: list
    :param SubLen: int
    :return:
    """
    return [alist[i:i+SubLen] for i in range(0, len(alist), SubLen)]


def html_table(input_value) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())

    output = ['<table>']
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('</td><td>'.join(sublist))
        output.append('</td></tr>')
    output.append('</table>')
    return output


def get_newest_file(input_list: list) -> str:
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())

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
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
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
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())

    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    logging.debug(("Yesterday is: " + str(yesterday)[0:10]))
    return str(yesterday)[0:10]


def file_handler(input_data) -> None:
    """
    Open a file in "data" folder and add a time (now) and wind speed.
    :param input_data:
    :return None: # should this be a boolean for success / failure?
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
    logging.debug("file_handler")

    try:
        temp_filename = str(config.get_path()) + str(datetime.datetime.today())[0:10] + ".txt"
        logging.debug("Opening file, " + str(temp_filename))
        with open(temp_filename, 'a+') as fileObject:
            time_stamp = str(datetime.datetime.now())
            fileObject.write(f"{time_stamp},{input_data},\n")
            logging.debug("File added to in file_handler()")
    except FileExistsError or FileNotFoundError as err:
        logging.error("Exception error in file_handler()" + str(err), exc_info=True)
    return


def open_file(filename: str, default_path="data/"):
    """
    Find and open a file to read data from it.
    :param filename:
    :return Error as string:
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
    logging.debug("opening file with read-only")

    output = ""
    try:
        output = open(default_path + filename, "r")
    except Exception as err:
        logging.error("Exception error in open_file()" + str(err), exc_info=True)
    if output is not None:
        pass
    else:
        output = "Error"  # need a better handle than this
    return output


def sort_dates(input_list) -> list:
    """
    Sort the dates of a list from string to YY MM DD HH.
    Need to check format of the data as it returns integers
    :param input_list:
    :return list:
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())

    print("input list: ", input_list)
    date_output_list = []
    for i in input_list:
        date_output_list.append(datetime.datetime(int(i[0] + i[1]),
                                                  int(i[3] + i[4]),
                                                  int(i[6] + i[7]),
                                                  int(i[9] + i[10])))
    date_output_list.sort()  # this should go in ascending order
    logging.debug("Sorted this list: " + str(date_output_list))
    return date_output_list


def read_in_data(filename: str) -> list:
    """
    Read in data from csv file.
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
    logging.debug("Read_in_data from " + filename)

    output = []
    try:
        file = open_file(str(config.get_path()) + filename)
        reader = csv.reader(file)
        for each_row in reader:
            output.append(each_row)
        file.close()
    except Exception as err:
        logging.error("Reading in csv data error: " + str(err))
    return output


def reformat_data(input_list: list):  # how to declare two list returns?
    """
    This will take data in str format "YY-MM-DD HH" and return into (datetime, str)
    :return: list -> WeatherData(datetime, str)
    """
    config = get_config()
    logging.basicConfig(filename=str(config.get_path()) + config.get_logging_location(), level=config.get_logging_level())
    logging.debug("reformat_data for plotting")

    local_x = []
    local_y = []

    logging.debug("input list " + str(input_list))
    for gl in input_list:
        for counter, g in enumerate(gl):
            if counter % 2 == 0:
                temp = g.replace('"', '')
                t = str(temp.lstrip())
                tmp = str(t[0:2]) + str(t[3:5]) + str(t[6:8])
                local_x.append(tmp)
                # print("stuff: {}, {}, {}, hour {}".format(t[0:2], t[3:5], t[6:8], t[9:11]))
            else:
                local_y.append(str(g))
        # output = sort_dates(local_x) # this takes a string YYMMDD and returns a datetime format.
    logging.debug("X axis values: " + str(local_x))
    logging.debug("Y axis values: " + str(local_y))
    return local_x, local_y
