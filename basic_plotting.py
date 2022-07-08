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

default_file_name = "test_data_from_counter.csv"
global_dict = []

def sort_dates(input_list):
    date_output_list = []
    for i in input_list:
        date_output_list.append(datetime.datetime(int(i[0]+i[1]),
                                                  int(i[3]+i[4]),
                                                  int(i[6]+i[7]),
                                                  int(i[9]+i[10])))
    date_output_list.sort() # this should go in accending order
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
        output = "Error"
 #   print("Output in opening file ", output)
    return output


# read in data from csv file
def read_in_data():
    file = open_file(default_file_name)
    reader = csv.reader(file)
    for each_row in reader:
        global_dict.append(each_row)
#    print("global dict: ", global_dict)
    file.close()


# create basic plot
def basic_plot():
    x_values = []
    y_values = []

    # even to x, odd to y
    for gl in global_dict:
        for counter, g in enumerate(gl):
            if (counter % 2 == 0):
                temp = g.replace('"', '')
                x_values.append(temp.lstrip())
            else:
                y_values.append(g)
    dates = sort_dates(x_values)
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