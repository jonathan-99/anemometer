#!/usr/bin/env python3

"""
Class file that covers all.
"""

from argparse import ArgumentError
from datetime import datetime, timedelta
from os.path import exists
from typing import Iterable, List
import json, json.encoder
import csv


class WeatherData:
    pass

class WeatherData:
    """This is as the name suggests, standard functions extrapolated & encapsulated."""

    def __init__(self, init_time: datetime, init_speed: float) -> None:
        self.eventTime = init_time or datetime.now()
        self.windSpeed = init_speed or 0.0

    def get_data(self) -> str:
        """REVIEW: I would question why you would do this at all - you have an instance with attributes..."""
        return self.eventTime, self.windSpeed

    def ToString(self) -> str:
        return f"{self.eventTime},{self.windSpeed}"

    def __str__(self):
        return json.dumps(
            self, 
            cls=WeatherDataEncoder, 
            ensure_ascii=False
        )

    def __repr__(self):
        return self.__str__()

    def __lt__(self, rhs: WeatherData) -> bool:
        """Returns true if this is less than RHS. Required for the list sort"""
        #print(f"lhs: {self.eventTime} rhs: {rhs.eventTime} eval {self.eventTime < rhs.eventTime}")
        return self.eventTime < rhs.eventTime

    def __gt__(self, rhs: WeatherData) -> bool:
        """Returns true if this is less than RHS. Required for the list sort"""
        return self.eventTime > rhs.eventTime

    def ToJson(self) -> str:
        return self.__str__()

class WeatherDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, WeatherData)):
            return obj.__dict__
        if (isinstance(obj, datetime)):
            return obj.__str__()
        else:
            return obj.__dict__

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, (datetime, datetime.date, datetime.time))):
            return obj.isoformat()
        elif (isinstance(obj, timedelta)):
            return (datetime.min + obj).time().isoformat()
        

class WeatherDataList:
    """Used to allow definition of methods which refer to current type declaration. Partial declaration below this"""
    pass

class WeatherDataList:
    """
    REVIEW: there is no WeatherData specific functionality in this list, and there are two functions external to any classes. Is this intentional?
    REVIEW: Class name should be WeatherDataList
    REVIEW: Do not name variables as per types"""

    # class atribute for date format
    OSDateTimeFormat = "%a %d %b %H:%M:%S %Z %Y"
    RawDataDateTimeFormat = "%y-%m-%d %H:%M:%S"

    def __init__(self) -> WeatherDataList:
        self.dataList: List[WeatherData] = []

    def add_data(self, input_data: WeatherData) -> None:
        if (input_data is None):
           raise ArgumentError("input_data is None")
            
        self.dataList.append(input_data)

    @property
    def InnerList(self) -> List:
        """REVIEW: May be better to present an enumerator rather than exposing inner types - see GetEnumerator"""
        return self.dataList

    def GetEnumerator(self) -> Iterable:
        """Returns an enumerable based on the current list state"""
        return enumerate(self.dataList, start=0)

    @property
    def Count(self) -> int:
        """Returns number of WD items in the instance list"""
        return len(self.dataList)

    def ToString(self) -> str:
        buffer = ""

        for listItem in self.dataList:
            if (len(buffer) > 0):
                buffer += "\n"

            buffer += f"Date and time: {listItem.ToString()}"

        return buffer

    def print_data(self):
        for listItem in self.dataList:
            print(f"Date and Time: {listItem.ToString()}")

    def Sort(self):
        self.dataList.sort()

    @staticmethod
    def CreateFromFile(sourcePath: str) -> WeatherDataList:
        """Creates an instance of WDL from a file (exists check needed)"""

        if (exists(sourcePath)):
            retVal = WeatherDataList()
            try:
                with open(sourcePath, "r") as sourceData:
                    # some code which absorbs the file stream as a WDL instance
                    rdr = csv.reader(sourceData, delimiter=',')
                    for row in rdr:
                        eventTime = datetime.strptime(row[0], WeatherDataList.RawDataDateTimeFormat)
                        windSpeed = float(row[1])
                        retVal.add_data(
                            WeatherData(eventTime, windSpeed)
                        )

            except Exception as err:
                # TODO should really use the logger implementation from arp_v
                print(f"Error opening file {sourcePath}: {json.dumps(err)}")

            finally:
                # temp return to demo code technique
                return retVal
        else:
            raise ArgumentError(f"Could not access file at {sourcePath}")

###### Review the following for purpose
def sort_dates(input_list):
    """REVIEW: Should this be part of the WeatherDataList class as a static method? Have created a sort method on WDL"""
    date_output_list = WeatherDataList()
    for i in input_list:
        date_output_list.add_data(datetime.datetime(int(i[0] + i[1]),
                                                    int(i[3] + i[4]),
                                                    int(i[6] + i[7])),
                                  int(i[9] + i[10]))

    # date_output_list.sort()  # this should go in ascending order
    return date_output_list


def open_file(input_value):
    """REVIEW: If this is used to create a WeatherDataList from a file, this should be a static method of WeatherDataList (returning and instance of WDL), or an instance
    method which loads from a specific path"""
    error_flag = False
    try:
        output = open(input_value, "r")
    except Exception as err:
        print("error opening file: {} because {}".format(input_value, err))
        error_flag = True
    if not error_flag:
        return output
    else:
        return "Error"
