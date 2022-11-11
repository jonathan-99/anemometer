#!/usr/bin/env python3

"""A collection of all functions for this program."""
try:
    import datetime
    import os
    import sys
    import csv
    import matplotlib.pyplot as plt
    import numpy as np
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))

def create_html_page_wrapper(name: str) -> str:
    """
    Need the start and end of a html page.
    :return 2 x str:
    """
    logging.basicConfig(filename="/logging/log.txt")
    logging.info("create_html_page_wrapper")
    title = "<!DOCTYPE html><head><title>" + name
    title += "</title></head><body>"
    end_tags = "</body></html>"
    return title, end_tags

def row_major(alist, sublen) -> list:
    """
    NOt quite sure of this yet!
    :param alist:
    :param sublen:
    :return:
    """
    return [alist[i:i+sublen] for i in range(0, len(alist), sublen)]

def html_table(input_value) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    output = []
    output.append('<table>')
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('</td><td>'.join(sublist))
        output.append('</td></tr>')
    output.append('</table>')
    return output


def list_file_directory(directory="data/") -> list:
    """
    Search through 'data' folder for all names of files and return them in a string. This will enable
    the index.html file to list them safely for a browser.
    :param directory: str
    :return: list
    """

    logging.basicConfig(filename="/logging/log.txt")
    logging.info("list_file_directory")
    list_of_files = []
    for path in os.listdir(directory):
        # check if current path is a file
        if os.path.isfile(os.path.join(directory, path)):
            list_of_files.append(path)
    return list_of_files


def get_yesterdays_date() -> str:
    """
    Simple function for getting yesterday's date.
    :return String:
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    print("Yesterday is: ", str(yesterday)[0:10])
    return str(yesterday)[0:10]


def file_handler(input_data) -> None:
    """
    Open a file in "data" folder and add a time (now) and wind speed.
    :param input_data:
    :return None: # should this be a boolean for success / failure?
    """

    logging.basicConfig(filename="/logging/log.txt")
    logging.debug("file_handler")
    try:
        # file_object = open("/data/" + str(datetime.datetime.today())[0:10] + ".txt", 'a')
        # time_stamp = str(datetime.datetime.now())
        # file_object.write(time_stamp[0:16] + "," + str(input_data) + ",\n")
        # file_object.close()
        temp_filename = "data/" + str(datetime.datetime.today())[0:10] + ".txt"
        logging.debug("Opening file, " + str(temp_filename))
        with open(temp_filename, 'a+') as fileObject:
            time_stamp = str(datetime.datetime.now())
            fileObject.write(f"{time_stamp},{input_data},\n")
            logging.debug("File added to in file_handler()")
    except Exception as err:
        logging.error("Exception error in file_handler()", exc_info=True)
    return


def open_file(filename):
    """
    Find and open a file to read data from it.
    :param filename:
    :return Error as string:
    """

    logging.basicConfig(filename="/logging/log.txt")
    logging.debug("opening file with read-only")
    output = ""
    try:
        output = open(filename, "r")
    except Exception as err:
        logging.error("Exception error in open_file()", exc_info=True)
    if output is not None:
        pass
    else:
        output = "Error"  # need a better handle than this
    return output


def sort_dates(input_list) -> list:
    """
    Sort the dates of a list from string to YY MM DD HH.
    Need to check format of the data as it returns integers?
    :param input_list:
    :return list:
    """
    print("input list: ", input_list)
    date_output_list = []
    for i in input_list:
        date_output_list.append(datetime.datetime(int(i[0] + i[1]),
                                                  int(i[3] + i[4]),
                                                  int(i[6] + i[7]),
                                                  int(i[9] + i[10])))
    date_output_list.sort()  # this should go in ascending order
    return date_output_list


def read_in_data(filename: str) -> list:
    """
    Read in data from csv file.
    """
    output = []
    file = open_file(filename)
    reader = csv.reader(file)
    for each_row in reader:
        output.append(each_row)
    file.close()
    return output


def reformat_data(input_list: list):  # how to declare two list returns?
    """
    This will take data in str format "YY-MM-DD HH" and return into (datetime, str)
    :return: list -> WeatherData(datetime, str)
    """

    logging.basicConfig(filename="/logging/log.txt")
    logging.info("reformat_data for plotting")
    local_x = []
    local_y = []
    output = []

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
        # output = sort_dates(local_x) # this takes a string yymmdd and returns a datetime format.
    return local_x, local_y
