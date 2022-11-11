#!/usr/bin/env python3

"""
Logs input from a GPIO-connected wind sensor to CSV-formatted output files.
Additional component plots graphs based on logged sensor values.

How long we want to wait between loops (seconds) - one hour.
3660 = 1 hour
3420 = 57 minutes. Do this due to initiating through crontab on the hour which might be out.
"""

try:
    import datetime
    import os
    import sys
    import RPi.GPIO as GPIO
    import functions
    import time
    import logging
    from functools import partial
except Exception as e:
    print("importing error: ", e)

# formatter = logging.Formatter("%(asctime)s , %(levelname)s , %(message)s",
#                                  datefmt='%Y-%m-%d , %H:%M:%S')
logging.basicConfig(filename="logging/log.txt", level=logging.DEBUG, format="%(asctime)s , %(levelname)s , %(message)s")


class WindMonitor:
    coreDataFilePath = "Use a configuration or variable"


    def __init__(self, intervalNumber: int, pinNumber: int) -> None:
        self.PIN = pinNumber
        self.interval = intervalNumber
        logging.debug('Initiating the weather monitor')
        self.count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.BOTH)
        trying_something = partial(self.add_count)
        try:
            GPIO.add_event_callback(self.PIN, trying_something)
        except TypeError as e:
            self.add_count()
        logging.debug("Set up complete. PIN=" + str(self.PIN) + " ,interval=" + str(self.interval))

    def add_count(self):
        self.count += 1
        logging.debug('Adding a tick: ' + str(self.show_count()))


    def show_count(self):
        return self.count


    def get_interval(self):
        return self.interval


    def reset(self):
        self.count = 0


def calculate_speed(input_info: int, spare: int) -> float:
    """
    Calculates speed in kph
    :param input_info: int
    :param spare:
    :return: speed: float
    """
    logging.debug("I am in calculating speed number: " + str(input_info))
    return (input_info*1.2) / spare


def execute(windObject) -> None:
    logging.debug('Ticks first count: ' + str(windObject.show_count()))
    time.sleep(windObject.get_interval())
    speed = calculate_speed(windObject.show_count(), windObject.get_interval())
    logging.debug("Ticks second count: " + str(windObject.show_count()) + " speed " + str(speed))
    functions.file_handler(speed)
    print("This is the speed: ", speed)


if __name__ == '__main__':
    # interval = 3420
    a_count = WindMonitor(10, 17)
    while True:
        execute(a_count)
    a_count.reset()