#!/usr/bin/env python3

import time
import datetime
import RPi.GPIO as GPIO

"""
How long we want to wait between loops (seconds) - one hour.
3660 = 1 hour
3420 = 57 minutes. Do this due to starting on reboot and initiating through crontab on the hour.
"""


def file_handler(input_data):
    try:
        file_object = open("/data/" + str(datetime.datetime.today())[0:10] + ".txt", 'a')
        time_stamp = str(datetime.datetime.now())
        file_object.write(time_stamp[0:16] + "," + str(input_data) + ",")
        file_object.close()
    except Exception as err:
        print("Problem: ", err)
    return


interval = 3420
wind_tick = 0  # Used to count the number of times the wind speed input is triggered

# Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

# Set digital pin 17 to an input and enable the pull-up
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH)


def calculate_speed(input_info, spare):
    return (input_info*1.2) / spare


def wind_trig():
    global wind_tick
    wind_tick += 1


GPIO.add_event_callback(17, wind_trig())


while True:
    time.sleep(interval)
# Calculate average wind speed over the last 15 seconds
    wind_speed = (wind_tick * 1.2) / interval
    file_handler(wind_speed)
    wind_tick = 0

#   print("This is the speed: ", wind_speed)


if __name__ == '__main__':
    windtrig()
