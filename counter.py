#!/usr/bin/env python3

"""
Logs input from a GPIO-connected wind sensor to CSV-formatted output files.
Additional component plots graphs based on logged sensor values.

How long we want to wait between loops (seconds) - one hour.
3660 = 1 hour
3420 = 57 minutes. Do this due to starting on reboot and initiating through crontab on the hour.
"""

try:
    import datetime
    import os
    import sys
    import RPi.GPIO as GPIO
    import functions
    import time
    import logging
except Exception as e:
    print("importing error: ", e)

# formatter = logging.Formatter("%(asctime)s , %(levelname)s , %(message)s",
#                                  datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="logging/log.txt", level=logging.DEBUG, format="%(asctime)s , %(levelname)s , %(message)s")

class WindMonitor:
    global count


    def __init__(self, intervalNumber: int, pinNumber: int):
        self.PIN = pinNumber
        self.interval = intervalNumber
        logging.info('Initiating the weather monitor')
        self.count = 0
        global _coreDataFilePath
        _coreDataFilePath = "Use a configuration or variable"
        logging.info('interval: ', str(self.interval))

        # Set GPIO pins to use BCM pin numbers
        GPIO.setmode(GPIO.BCM)
        logging.info('setmode()')
        # Set digital pin 17 to an input and enable the pull-up
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logging.info('setup()')
        # Event to detect wind (4 ticks per revolution)
        GPIO.add_event_detect(self.PIN, GPIO.BOTH)
        logging.info('add_event_detect()')
        GPIO.add_event_callback(17, self.add_count())

    def add_count(self):
        logging.debug('add_count()')
        self.count += 1

    def show_count(self):
        return self.count

    def reset(self):
        self.count = 0


def calculate_speed(input_info: int, spare: int) -> float:
    """
    Calculates speed in kph
    :param input_info: int
    :param spare:
    :return: speed: float
    """
    return (input_info*1.2) / spare


def execute(windObject) -> None:
    logging.debug('Ticks count: ', str(windObject.show_count()))
    time.sleep(windObject.interval)
    speed = calculate_speed(windObject.show_count(), windObject.interval)
    logging.debug("Ticks count: ", str(windObject.show_count()), "speed ", str(speed))
    functions.file_handler(speed)
    windObject.reset()

    print("This is the speed: ", speed)


if __name__ == '__main__':
    # interval = 3420
    a_count = WindMonitor(10, 17)
    while True:
        execute(a_count)
