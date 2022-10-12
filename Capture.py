from argparse import ArgumentError
from datetime import datetime, timedelta
from os.path import exists
from plistlib import InvalidFileException
from typing import Iterable, List
import json, json.encoder
import csv
import RPi.GPIO as GPIO
from threading import Timer

class Capture():
    """Used to wrap all the actual capture requirement into a type"""

    ## class attributes
    # Interval for timer to recalc wind speed
    Interval = 3420

    # Log file location. Let logrotate deal with the rotations (should be pulled from a config really)
    LogFile = f"/data/{datetime.now().strftime('%Y-%M-%d')}.csv"

    ## ctor
    def __init__(self) -> None:
        self.windTimer = Timer(
            Capture.Interval,
            self.WriteEvent
        )

        # Used to count the number of times the wind speed input is triggered
        self.wind_tick = 0

        # Set GPIO pins to use BCM pin numbers
        GPIO.setmode(GPIO.BCM)
        
        # Set digital pin 17 to an input and enable the pull-up
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Event to detect wind (4 ticks per revolution)
        GPIO.add_event_detect(17, GPIO.BOTH)

        # Assign the callback to trigger a particular event
        GPIO.add_event_callback(17, self.WindEventHandler())

        # start the timer
        self.windTimer.start()

    ## dtor
    def __del__(self):
        self.windTimer.cancel()

    ## methods
    def WindEventHandler(self) -> None:
        """Used to handle events from GPIO(17). Increment the positional tick counter representing the wind sensor"""
        self.wind_tick += 1

    def WriteEvent(self) -> bool:
        """Write wind event data to the log file"""
        measuredSpeed = (self.wind_tick * 1.2) * Capture.interval
        with open(Capture.LogFile, "a") as output:
            output.write(f"{str(datetime.now())},{measuredSpeed}\n")

        return True

        