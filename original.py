#!/usr/bin/env python3

try:
    import time
    import RPi.GPIO as GPIO
    import sys
except ImportError as e:
    sys.exit("Importing error: " + str(e))


interval = 15  # How long we want to wait between loops (seconds)
windTick = 0  # Used to count the number of times the wind speed input is triggered

# Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

# Set digital pin 17 to an input and enable the pull-up
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH)


def windtrig() -> None:
    global windTick
    windTick += 1


GPIO.add_event_callback(17, windtrig)

while True:

    time.sleep(interval)

    # Calculate average wind speed over the last 15 seconds
    windSpeed = (windTick * 1.2) / interval
    windTick = 0

    print("Wind Speed: ", windSpeed, " KPH")
