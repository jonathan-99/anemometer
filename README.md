# anemometer
Setting up, and charting a wind speed checker

I wanted a system where I could buy all the bits off the internet without much knowledge required. The HAT is purchased from BC robotics and very little soldering is required. The tutorial below is where I developed, counter.py.

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
  <dt>basic_plotting.py</dt>
  <dt>weather_class.py</dt>
  <dt>install.sh</dt>
</dl>


# Installs
I have now created a bash script which should install all the below on linux but require sudo priv.
```
sudo apt-get update && sudo apt-get upgrade
sudo pip3 install --upgrade setuptools
pip3 install numpy
pip3 install RPI.GPIO 
pip3 install adafruit-blinka
python3 -m pip install python3-matplotlib
```

# Setting up crontab
This is the current layout of my crontab. It should run counter.py at one minute past the hour, every hour for about 57 minutes. Thus it will give you roughly an hour's worth of data in each hour. The output is done within the code, so any further output should just be piped to standard out.  
```
sudo crontab -e"
```
with 
```
MAILTO=""
```
at the top of the file and 
```
1 * * * * python3 /opt/weather/counter.py 2>&1
```
at the bottom.

### Notes
=======
This is the current layout of my crontab. It should run counter.py at one minute past the hour, every hour for about 57 minutes. Thus, it will give you roughly an hour's worth of data in each hour. The output is done within the code, so any further output should just be piped to standard out.
I have considered adding this element at the bottom of crontab. Upon reboot of the device, it should run this script again. I removed this as it might reboot mid-hour and that would mess up the data files.
```
@reboot python3 /opt/weather/counter.py
```

Also check on OS:
- ```export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0```

# The output
1. test_data_from_counter.csv  
CSV rows using `YY-MM-DD HH-MM-SS, X` format, where X is speed in kmh (float)
