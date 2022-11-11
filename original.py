#!/usr/bin/env python3

try:
    import time
    import RPi.GPIO as GPIO
    import sys
except ImportError as e:
    sys.exit("Importing error: " + str(e))


global windTick
global interval
interval = 10
windTick = 0  # Used to count the number of times the wind speed input is triggered

def system_check():
    print("GPIO info", GPIO.RPI_INFO)

def windtrig() -> None:
    global windTick
    windTick += 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.BOTH)
try:
    GPIO.add_event_callback(17, windtrig)
except TypeError as e:
    windtrig()

while True:
    time.sleep(interval)
    windSpeed = (windTick * 1.2) / interval
    windTick = 0

    print("Wind Speed: ", windSpeed, " KPH")

"""
if __name__ == "__main__":
    pass
"""