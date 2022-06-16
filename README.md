# anemometer
Setting up, and charting a wind speed checker

## reference URL
https://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/


# Installs

sudo apt-get update
sudo pip3 install --upgrade setuptools
pip3 install RPI.GPIO
pip3 install adafruit-blinka

# set up crontab
1 * * * * python3 /home/pi/bc-robotics/counter.py

@reboot python3 /home/pi/bc/robotics/counter.py

## output
something.csv
# in the format, "YY-MM-DD HH-SS, XX.X," where X is speed in kmh