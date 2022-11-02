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
except ImportError as e:
    sys.exit("Importing error: " + str(e))

class wind_tick():
    global count

    def __init__(self):
        self.count = 0

    def add_count(self):
        self.count = self.count + 1

    def show_count(self):
        return self.count

def calculate_speed(input_info: int, spare: int) -> float:
    """
    Calculates speed in kph
    :param input_info: int
    :param spare:
    :return: speed: float
    """
    return (input_info*1.2) / spare


def wind_trig(self) -> None:
    wind_tick.add_count()


def setup() -> None:
    """
    Initiate all PINs etc.
    :return -> None:
    """
    global coreDataFilePath
    coreDataFilePath = "Use a configuration or variable"
    global interval
    interval = 3420

    # Set GPIO pins to use BCM pin numbers
    GPIO.setmode(GPIO.BCM)

    # Set digital pin 17 to an input and enable the pull-up
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Event to detect wind (4 ticks per revolution)
    GPIO.add_event_detect(17, GPIO.BOTH)
    GPIO.add_event_callback(17, wind_trig)


def execute() -> None:
    time.sleep(interval)
    speed = calculate_speed(wind_tick.show_count(), interval)
    functions.file_handler(speed)
    a_count = wind_tick()

    print("This is the speed: ", speed)


if __name__ == '__main__':
    a_count = wind_tick()
    setup()
    while True:
        execute()
