"""
This is as the name suggests, standard functions extrapolated.
"""

import datetime


class WeatherData:
    def __init__(self, init_time: datetime, init_speed: str):
        self.time = init_time
        self.speed = init_speed

    def get_data(self):
        return self.time, self.speed


class ListOfWeatherData:
    def __init__(self):
        self.list = []

    def add_data(self, input_data: WeatherData):
        self.list.append(input_data)

    def get_data(self):
        return self.list

    def print_data(self):
        for lis in self.list:
            print("Date and Time: ", lis)


def sort_dates(input_list):
    date_output_list = ListOfWeatherData()
    for i in input_list:
        date_output_list.add_data(datetime.datetime(int(i[0] + i[1]),
                                                    int(i[3] + i[4]),
                                                    int(i[6] + i[7])),
                                                    int(i[9] + i[10]))
    # date_output_list.sort()  # this should go in ascending order
    return date_output_list


def open_file(input_value):
    output = ""
    try:
        output = open(input_value, "r")
    except Exception as err:
        print("error opening file: ", err)
    if output is not None:
        pass
    else:
        output = "Error"
    #   print("Output in opening file ", output)
    return output
