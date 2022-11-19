# REVIEW: putting exception handling around imports suggests that initialisation issues are not resolved
try:
    import os
    import sys
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    import functions
    import logging
    from class_file import config_data
    from collections import namedtuple
except ImportError as e:
    sys.exit("Importing error: " + str(e))

default_file_name = "testing/test_data_from_counter.csv"
# can I remove this global variable?


def basic_plot(input_list, save=False) -> None:
    """
    This functions takes dates (and hours) and plots them on a basic x-y chart.
    """
    config_class = functions.get_config()
    logging.basicConfig(filename=config_class.get_logging_location())
    logging.debug("basic_plot" + str(input_list) + "saving? " + str(save))

    # even to x, odd to y
    dates, y_values = functions.reformat_data(input_list)
    print("dates: ", dates, " : y_values: ", y_values)

    x = np.array(dates)
    y = np.array(y_values)
    print("x:", x)
    print("y: ", y)

    fig, main_ax = plt.subplots()
    main_ax.plot(x, y, 'o')
    main_ax.set_ylim(y_values[0], y_values[len(y_values) - 1])

    # plt.title("Basic Plot in ", matplotlib.__version__)
    if save:
        plt.title("This is the image")
        fig1 = plt.gcf()
        fig1.savefig('default_plot.jpg', dpi=100)
        logging.debug('Saved default_plot.jpg')
        plt.close(fig1)
    else:
        pass
    plt.show()
    plt.close('all')
    return


def create_plot() -> None:
    config_class = functions.get_config()
    logging.basicConfig(filename=config_class.get_logging_location())
    logging.debug("Within create plot for png creation.")

    # list_file_directory returns a tuple.
    value = functions.list_file_directory()
    local_list = functions.read_in_data(value[1])
    basic_plot(local_list, True)


if __name__ == '__main__':
    config = functions.get_config()
    logging.basicConfig(filename=config.get_logging_location())

    alist = functions.read_in_data(default_file_name)
    basic_plot(alist)
