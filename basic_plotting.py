try:
    import datetime
    import os
    import csv
    import sys
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
except ImportError as e:
    sys.exit("Importing error: " + str(e))

default_file_name = "testing/test_data_from_counter.csv"
global_dict = []


def sort_dates(input_list):
    print("input list: ", input_list)
    date_output_list = []
    for i in input_list:
        date_output_list.append(datetime.datetime(int(i[0] + i[1]),
                                                  int(i[3] + i[4]),
                                                  int(i[6] + i[7]),
                                                  int(i[9] + i[10])))
    date_output_list.sort()  # this should go in ascending order
    return date_output_list


# find and open data file
def open_file(input_value):
    output = ""
    try:
        output = open(input_value, "r")
    except Exception as err:
        print("error opening file: ", err)
    if output is not None:
        pass
    else:
        output = "Error"  # need a better handle than this
    return output


# read in data from csv file
def read_in_data():
    file = open_file(default_file_name)
    reader = csv.reader(file)
    for each_row in reader:
        global_dict.append(each_row)
    file.close()

def reformat_data():
    """
    This will take data in str format "YY-MM-DD HH" and return into (datetime, str)
    :return: list -> WeatherData(datetime, str)
    """
    local_x = []
    local_y = []
    output = []

    for gl in global_dict:
        for counter, g in enumerate(gl):
            if counter % 2 == 0:
                temp = g.replace('"', '')
                t = str(temp.lstrip())
                tmp = str(t[0:2]) + str(t[3:5]) + str(t[6:8])
                local_x.append(tmp)
                # print("stuff: {}, {}, {}, hour {}".format(t[0:2], t[3:5], t[6:8], t[9:11]))
            else:
                local_y.append(str(g))
        #output = sort_dates(local_x) # this takes a string yymmdd and returns a datetime format.
    return local_x, local_y


"""
This functions takes dates (and hours) and plots them on a basic x-y chart.
"""
def basic_plot():

    # even to x, odd to y
    dates, y_values = reformat_data()

    x = np.array(dates)
    y = np.array(y_values)

    fig, main_ax = plt.subplots()
    main_ax.plot(x, y, 'o')
    main_ax.set_ylim(y_values[0], y_values[len(y_values) - 1])

    # plt.title("Basic Plot in ", matplotlib.__version__)
    plt.show()


if __name__ == '__main__':
    read_in_data()
    basic_plot()
