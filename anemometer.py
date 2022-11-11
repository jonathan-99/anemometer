#!/usr/bin/env python3

try:
    import os
    import sys
    import argparse
    import Capture
    import basic_plotting
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def main_function() -> int:
    """
    This is the main function which holds all arguments to effectively control the anemometer.
    """
    logging.basicConfig(filename="/logging/log.txt")
    logging.info("main function fro anemometer.py")
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--capture", help="run the capture")
    parser.add_argument("-p", "--plot", type=str,
                        default="testing/test_data_from_counter.csv",
                        const="testing/test_data_from_counter.csv",
                        nargs='?',
                        dest="input_a",
                        help="do a basic plot of data held")
    args = parser.parse_args()

    if args.capture:
        a = Capture.Capture()
        a.WindEventHandler()
    elif args.plot:
        basic_plotting.basic_plot(args.plot)
    else:
        print("you need to select an option, try -h for help.")
    return 0


if __name__ == "__main__":
    main_function()
