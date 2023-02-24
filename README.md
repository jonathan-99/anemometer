# anemometer

This is about setting up, and charting a wind speed checker with a raspberry pi.

 

I wanted a system where I could buy all the bits off the internet without much knowledge required. The HAT is purchased from BC robotics and very little soldering is required. The tutorial below is where I developed, original.py.

 

It started as original.py, then became counter.py. There is another adaptation called Capture.py.

 

Reference URL

https://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/

 

 

## Architecture

Description.

This was designed to be run in three manners: directly with original.py; indirectly and directly (including crontab) with counter.py; and with full functionality of anemometer.py

 

>All generated data should be stored in data folder under a text file called by the day it was generated.

- data /

 

>The testing folder holds all tests.

- test /

gpio_testing.py

main_testing.py

test_counter.py

> This is for logging. Error.log should catch any errors from the bash script (run_script); script.log should catch bash script (run_script) output; and log.txt should catch all code logging in all files.

- error.log

- script.log

- log.txt

> You can execute counter directly with a default of 57 minutes on PIN 17. Or you can create an instance of the weather_class and change PIN and time for script to run. Functions hold all generic functions.

- counter.py

functions.py

weather_class.py

>The browser element is designed to allow debugging - answer the question 'are we generating data?'.

- simple_browser.py

index.html

table.html

default_plot.png

> This can be run directly and will default on some data to prove matplotlib works.

- basic_plotting.py

> These are developments which were not the focus of development.

- original.py

- Capture.py

> This is the master (c2) script which can be used to run all other scripts.

- anemometer.py

> This script should install all the key libraries and set all key environmental variables on a raspberry pi to run these scripts.

- install.sh

> This script simply enables crontab to run counter.py and collect all logging. (Crontab disregards all logging data.)

- run_script.sh

 

## Installs

I have now created a bash script which should install all the below on linux but require sudo priv.

 

```

sudo apt-get update && sudo apt-get upgrade

sudo pip3 install --upgrade setuptools

pip3 install numpy

pip3 install RPI.GPIO

pip3 install adafruit-blinka

python3 -m pip install python3-matplotlib

```

### Issues with installs

I have had to cycle through the following commands in different orders to finalise them.

```

sudo locale-gen en_GB.UTF-8 UTF-8

export LANGUAGE=en_GB.UTF-8

export LC_ALL=en_GB.UTF-8

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# issues with this one sudo update-locale en_GB.UTF-8 UTF-8

```

 

### Setting up crontab

This is the current layout of my crontab. It should run counter.py at one minute past the hour, every hour for about 57 minutes. 
Thus, it will give you roughly an hour's worth of data in each hour. 
The output is done within the code, so any further output should just be piped to standard out.

Note that all code should be in ~opt/ so that it can run as root.

 

```

sudo crontab -e"

with

MAILTO=""

```

at the top of the file and

```

1 * * * * python3 /opt/weather/run_script.sh 2>&1

```

at the bottom. Remember to

```sudo chmod +x run_script.sh```

 

## Description on architecture

Plotting

Counting and Capture

Browsing as a debugger

The output

test_data_from_counter.csv

CSV rows using YY-MM-DD HH-MM-SS, X format, where X is speed in kmh (float)

Notes

======= This is the current layout of my crontab. 
It should run counter.py at one minute past the hour, every hour for about 57 minutes. 
Thus, it will give you roughly an hour's worth of data in each hour. 
The output is done within the code, so any further output should just be piped to standard out. 
I have considered adding this element at the bottom of crontab. 
Upon reboot of the device, it should run this script again. 
I removed this as it might reboot mid-hour and that would mess up the data files.

Coverage Report (17/02/23)

| Name                                      | Stmts | Miss      | Cover     |
|-------------------------------------------|-------|-----------|-----------|
| src\Capture.py                            | 29    | 13        | 55%       |
| src\basic_plotting.py                     | 44    | 30        | 32%       |
| src\class_file.py                         | 43    | 22        | 49%       |
| src\functions.py                          | 144   | 90        | 38%       |
| src\organise_counter_data.py              | 23    | 23        | 0%        |
| src\original.py                           | 24    | 24        | 0%        |
| src\simple_browser.py                     | 55    | 55        | 0%        |
| src\weather_class.py                      | 101   | 101       | 0%        |
| ------------------------------------------| -     | -     | -     |
| TOTAL                                     | 463   | 358       | 23%       |