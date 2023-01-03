import datetime

"""
Open logging files, add up second to minutes to hours into a temp file, log into a logging file
Close all files.
"""

# declare global variables
speeds_per_day = []


def get_yesterdays_date():
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    print("Yesterday is: ", str(yesterday)[0:10])
    return str(yesterday)[0:10]


def find_hourly_data():

    """Locate the csv data in the format "YY-MM-DD HH", "12.3"
    re-organise it into monthly data csv
    :return: boolean
    """
    pass


def main():
    """
    This is the tidy up file.
    :return: normal completion state
    """

    file_object = open("../data/weather_logger.txt", "a")
    file_name = "data/" + get_yesterdays_date() + ".txt"
    try:
        yesterday_file = open(file_name, "r")
        for index, speed in enumerate(yesterday_file, start=1):
            speeds_per_day.append("{}00 {}".format(index, speed))
            print("speeds per day: ", speeds_per_day)
            file_object.write("{}00, {}".format(str(index), str(speed)))
        yesterday_file.close()
    except Exception as err:
        print("Error opening file: {} was {}".format(file_name, err))
    file_object.close()


if __name__ == '__main__':
    main()
