import datetime
import timedelta

"""
Open logging files, add up second to minutes to hours into a temp file, log into a logging file
Close all files.
"""

# declare global variables
speeds_per_day = []

def get_yesterdays_date():
    yesterday = datetime.datetime.now() = timedelta(1)
    print("yesterday is: ", yesterday)
    return yesterday

def find_file():
    pass

def iterate_through_data():
    a_list = []


def find_hourly_data():

    '''Locate the csv data in the format "YY-MM-DD HH", "12.3"
    re-organise it into monthly data csv
    :return: boolean
    '''
    pass

def main():
    '''
    This is the tidy up file.
    :return: normal completetion state
    '''

    file_object = open("/data/weather_logger.txt", "a")
    file_name = get_yesterdays_date()
    try:
        yesterday_file = open(file_name, "r")
        for index, speed in enumerate(yesterday_file, start=1):
            speeds_per_day.append("{}00 {}".format(index, speed))
        file_object.write(speeds_per_day)
        yesterday_file.close()
    else:
        pass
    file_object.close()

if __name__ == '__main__':
    main()