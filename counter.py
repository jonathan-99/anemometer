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
    from class_file import config_data
    from functools import partial
except Exception as e:
    print("importing error: ", e)


def crontab_method(number: str) -> None:
    while True:
        time_now = datetime.datetime.now()
        t = time_now.strftime("%M")
        if str(t) == number:
            interval = 3420
            a_wind_object = WindMonitor(3420, 17)
            while True:
                execute(a_wind_object)
        else:
            pass


class WindMonitor:
    global count

    def __init__(self, interval_number: int, pin_number: int) -> None:
        self.PIN = pin_number
        self.interval = interval_number
        logging.debug(f'Initiating the weather monitor')
        global count
        count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.BOTH)
        GPIO.add_event_callback(self.PIN, self.add_count)
        logging.debug(f"Set up complete. PIN=" + str(self.PIN) + " ,interval=" + str(self.interval))

    def add_count(*args) -> None:
        """
        The callback function passes the PIN number to add_count.
        It won't work without doing this, but the add_count doesn't need the number at this time.
        """
        global count
        count += 1
        logging.debug(f'Adding a tick: ' + str(count))

    def show_count(self):
        global count
        return count

    def get_interval(self):
        return self.interval

    def reset(self):
        global count
        count = 0


def calculate_speed(input_info: int, spare: int) -> float:
    """
    Calculates speed in kph
    :param input_info: int
    :param spare:
    :return: speed: float
    """
    total_path = config.get_path() + config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())
    logging.debug(f"I am in calculating speed number: " + str(input_info))

    return (input_info*1.2) / spare


def execute(wind_object) -> None:
    """
    This function executes until either user interuption or until the interval in seconds completes.
    """
    config = functions.get_config()
    print("(Execute) Config capture path: ", config.get_path())
    print("(Execute) Config log location: ", config.get_logging_path(), config.get_log_filename())
    total_path = config.get_path() + config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())
    logging.debug(f'Ticks first count: ' + str(wind_object.show_count()))

    time.sleep(wind_object.get_interval())
    speed = calculate_speed(wind_object.show_count(), wind_object.get_interval())
    logging.debug(f"Ticks second count: " + str(wind_object.show_count()) + " speed " + str(speed))
    functions.file_handler(speed)
    logging.debug(f"For the last " + str(wind_object.interval/60) + "mins, the speed has been: " + str(speed))
    wind_object.reset()


if __name__ == '__main__':
    config = functions.get_config()
    print("Config capture path: ", config.get_path())
    total_path = config.get_path() + config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    # interval = 3420
    a_count = WindMonitor(3420, 17)
    while True:
        execute(a_count)