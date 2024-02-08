# REVIEW: putting exception handling around imports suggests that initialisation issues are not resolved
try:
    import os
    import sys
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    from src import functions
    import logging
    from src.class_file import config_data
    import src.file_handler_class as file_handler_class
    from collections import namedtuple
except ImportError as e:
    sys.exit("Importing error: " + str(e))

default_file_name = "../testing/test_data_from_counter.csv"
# can I remove this global variable?


def basic_plot(input_list: list, save=False) -> None:
    """
    This functions takes dates (and hours) and plots them on a basic x-y chart.
    """
    logging.debug("basic_plot" + str(input_list) + "saving? " + str(save))

    # even to x, odd to y
    dates, y_values = functions.split_list(input_list)
    dates = functions.handle_input_list_datetime(dates)
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
    logging.debug("Within create plot for png creation.")

    file_handler_object = file_handler_class.FileHandlerClass('data/2202-11-04.txt')
    file_handler_object.read_specific_csv_file('data/2202-11-04.txt')
    value = file_handler_object.get_weather_data_list()
    basic_plot(value, True)


if __name__ == '__main__':
    import src.class_file as config_data
    config = config_data.ConfigData('config.json')
    name = config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=name)

    alist = functions.get_weather_data()
    basic_plot(alist)
