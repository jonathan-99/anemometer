#!/usr/bin/env python3
"""Unit tests for the WeatherData and WeatherDataList types"""
import sys
sys.path.append("..")
from weather_class import WeatherData, WeatherDataList
from datetime import datetime, time, date
from typing import List
import unittest

class WD_tests(unittest.TestCase):
    dateTimeFormat = "%a %d %b %H:%M:%S %Z %Y"

    def test_ctors(self):
        testDate = datetime.strptime("Tue 20 Sep 13:55:06 BST 2022", WD_tests.dateTimeFormat)
        test2 = WeatherData(
            datetime.strptime(
                "Tue 20 Sep 13:55:06 BST 2022",
                WD_tests.dateTimeFormat
            ),
            1.0
        )

        # verify that the instance cannot be created without mandatory params
        self.assertRaises(
            TypeError,
            WeatherData,
        )

        # Verify ctor works as expected
        self.assertIsNotNone(test2, "Not instancing correctly - 2")

        # Verify JSON parsing works as expected
        self.assertIsNotNone(
            test2.ToJson(),
            "Cannot parse as JSON. Check outputs"
        )

        # Verify wind speed set
        self.assertEqual(
            first = test2.windSpeed,
            second = 1.0, 
            msg = f"Should be 1.0 - {test2.ToJson()}"
        )

        # Verify event date set
        self.assertEqual(
            first = testDate, 
            second = test2.eventTime, 
            msg = "Incorrect date-time parsing in test2"
        )

        # Verify print method
        self.assertIsNotNone(
            test2.ToString(),
            "Nothing returned by print method"
        )

class WDL_tests(unittest.TestCase):
    """Focused on list-related testing"""

    def test_ctors(self):
        self.assertIsInstance(
            WeatherDataList.CreateFromFile("./test_data_from_counter_parsed.csv"),
            WeatherDataList,
            "Could not create instance of WDL from file"
        )

        #print(f"CTOR Complete, testing printing: {wdlTest.ToString()}")

    def test_sorting(self):
        wdlTest = WeatherDataList.CreateFromFile("./test_data_from_counter_parsed.csv")

        self.assertRaises(
            TypeError,
            wdlTest.Sort()
        )

        print(f"Sorted list:\n{wdlTest.ToString()}")

    def test_properties(self):
        wdlTest = WeatherDataList.CreateFromFile("./test_data_from_counter_parsed.csv")

        self.assertGreater(
            wdlTest.Count,
            5,
            "Should have at least 5 items in list: "
        )

if __name__ == '__main__':
    unittest.main()