# anemometer
Setting up, and charting a wind speed checker

I wanted a system where I could buy all the bits off the internet without much knoweldge required. The HAT is purchased from BC robotics and very little soldering is required. The tutorial below is where i developed, counter.py.

## reference URL
https://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/

## Architecture
<dl>
  <dt>data</dt>
  <dt>test</dt>
  <dd>gpio_testing.py</dd>
  <dd>main_testing.py</dd>
  <dd>test_counter.py</dd>
  <dt>counter.py</dt>
  <dd>


# Installs
```
sudo apt-get update
sudo pip3 install --upgrade setuptools
pip3 install RPI.GPIO
pip3 install adafruit-blinka
```

Setting up crontab
This is the current layout of my crontab. It should run counter.py at one minute past the hour, every hour for about 57 minutes. Thus it will give you roughly an hour's worth of data in each hour. The output is done within the code, so any further output should just be piped to standard out.  
```
1 * * * * python3 /home/pi/bc-robotics/counter.py 2>&1
```

I have considered adding this element at the bottom of crontab. Upon reboot of the device, it should run this script again. I removed this as it might reboot mid-hour and that would mess up the data files.
```
@reboot python3 /home/pi/bc/robotics/counter.py
```

The output
1. test_data_from_counter.csv  
...in the format, "YY-MM-DD HH-SS, XX.X," where X is speed in kmh
