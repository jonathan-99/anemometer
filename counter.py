import time, datetime
import board # not sure this is needed
import RPi.GPIO as GPIO

interval = 3660 #How long we want to wait between loops (seconds) - one hour.
windTick = 0 #Used to count the number of times the wind speed input is triggered

#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

#Set digital pin 17 to an input and enable the pullup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH)
def windtrig(self):
    global windTick
    windTick += 1

    GPIO.add_event_callback(17, windtrig)

while True:
    time.sleep(interval)
    # Calculate average windspeed over the last 15 seconds
    windSpeed = (windTick * 1.2) / interval
    windTick = 0

print("This is the speed: ",windSpeed)

if __name__ == '__main__':
    windtrig()