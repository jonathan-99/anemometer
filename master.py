#!/usr/bin/env python3

try:
    import os
    import sys
    import argparse
    import counter
    from src import Capture, basic_plotting, functions
    import logging
    from src.class_file import config_data
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def setup_argparse() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture', help='run the capture')
    parser.add_argument('--plot', help='do a basic plot of data held')
    parser.add_argument('-t', '--tickcounter', help='run the counter') # interval='3420', pin='17',
    parser.add_argument("-i", "--interval", default="3420", help="run the counter")
    parser.add_argument("--crontab", default="00", help="run the counter on a schedule like crontab")

    return parser


def main_function() -> int:
    """
    This is the main controller to effectively control the anemometer.
    """
    logging.basicConfig(filename='logging/log.txt')
    logging.debug("main function from master.py")

    parser = setup_argparse()
    args = parser.parse_args() # sys.argv[1:])
    if args.capture:
        logging.debug("Argument for Capture used")
        a = Capture.Capture()
        a.WindEventHandler()
    elif args.plot:
        logging.debug("Argument for Plotting used")
        basic_plotting.basic_plot(args.plot)
    elif args.tickcounter:
        b_count = counter.WindMonitor(args.interval, args.pin)
        while True:
            counter.execute(b_count)
    elif args.crontab:
        counter.crontab_method(str(args.crontab))
    else:
        print("you need to select an option, try -h for help.")
    return 0


if __name__ == "__main__":
    main_function()
