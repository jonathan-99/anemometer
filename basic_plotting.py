# REVIEW: putting exception handling around imports suggests that initialisation issues are not resolved
try:
    import os
    import sys
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    import functions
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))

default_file_name = "testing/test_data_from_counter.csv"
# can I remove this global variable?


def basic_plot(input_list, save=False) -> None:
    """
    This functions takes dates (and hours) and plots them on a basic x-y chart.
    """
    logging.basicConfig(filename="/logging/log.txt")
    logging.debug("basic_plot" + str(input_list) + "saving? " + str(save))
    # even to x, odd to y
    dates, y_values = functions.reformat_data(input_list)

    x = np.array(dates)
    y = np.array(y_values)

    fig, main_ax = plt.subplots()
    main_ax.plot(x, y, 'o')
    main_ax.set_ylim(y_values[0], y_values[len(y_values) - 1])

    # plt.title("Basic Plot in ", matplotlib.__version__)
    plt.show()
    if save:
        plt.savefig('default_plot.png')
        logging.debug('Saved default_plot.png')
    else:
        pass
    return


def create_plot() -> None:
    logging.basicConfig(filename="/logging/log.txt")
    logging.debug("Within create plot for png creation.")
    disregard_list_of_files_in_directory, file_name = functions.list_file_directory()
    local_list = functions.read_in_data(file_name)
    basic_plot(local_list, True)


if __name__ == '__main__':
    logging.basicConfig(filename="/logging/log.txt")
    alist = functions.read_in_data(default_file_name)
    basic_plot(alist)
