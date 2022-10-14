# REVIEW: putting exception handling around imports suggests that initialisation issues are not resolved
try:
    import os
    import sys
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    import functions
except ImportError as e:
    sys.exit("Importing error: " + str(e))

default_file_name = "testing/test_data_from_counter.csv"
# can I remove this global variable?


def basic_plot(input_list):
    """
    This functions takes dates (and hours) and plots them on a basic x-y chart.
    """

    # even to x, odd to y
    dates, y_values = functions.reformat_data(input_list)

    x = np.array(dates)
    y = np.array(y_values)

    fig, main_ax = plt.subplots()
    main_ax.plot(x, y, 'o')
    main_ax.set_ylim(y_values[0], y_values[len(y_values) - 1])

    # plt.title("Basic Plot in ", matplotlib.__version__)
    plt.show()


if __name__ == '__main__':
    alist = functions.read_in_data(default_file_name)
    basic_plot(alist)
