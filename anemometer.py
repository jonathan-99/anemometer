#!/usr/bin/env python3
import counter

try:
    import os
    import sys
    import argparse
    import Capture
    import basic_plotting
    import logging
    import functions
    from class_file import config_data
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def main_function() -> int:
    """
    This is the main function which holds all arguments to effectively control the anemometer.
    """
    config_class = functions.get_config()
    logging.basicConfig(filename=config_class.get_logging_location())
    logging.debug("main function fro anemometer.py")

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--capture", help="run the capture")
    parser.add_argument("-p", "--plot", type=str,
                        default="testing/test_data_from_counter.csv",
                        const="testing/test_data_from_counter.csv",
                        nargs='?',
                        dest="input_a",
                        help="do a basic plot of data held")
    parser.add_argument("-C", "--Counter", interval="3420", pin="17", help="run the counter")
    parser.add_argument("-P", "--pin", default="17", help="run the counter")
    parser.add_argument("-i", "--interval", default="3420", help="run the counter")
    args = parser.parse_args()

    if args.capture:
        logging.debug("Argument for Capture used")
        a = Capture.Capture()
        a.WindEventHandler()
    elif args.plot:
        logging.debug("Argument for Plotting used")
        basic_plotting.basic_plot(args.plot)
    elif args.counter:
        b_count = counter.WindMonitor(args.interval, args.pin)
        while True:
            counter.execute(b_count)
    else:
        print("you need to select an option, try -h for help.")
    return 0


if __name__ == "__main__":
    main_function()
