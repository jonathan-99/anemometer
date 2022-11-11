#!/usr/bin/env python3

try:
    import time
    import RPi.GPIO as GPIO
    import sys
except ImportError as e:
    sys.exit("Importing error: " + str(e))

windTick = 0  # Used to count the number of times the wind speed input is triggered

def windtrig() -> None:
    global windTick
    windTick += 1


def main_function(interval: int) -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.BOTH)
    GPIO.add_event_callback(17, windtrig)

    while True:
        time.sleep(interval)
        windSpeed = (windTick * 1.2) / interval
        windTick = 0

        print("Wind Speed: ", windSpeed, " KPH")


if __name__ == "__main__":
    windTick = 0  # Used to count the number of times the wind speed input is triggered
    main_function(10)
