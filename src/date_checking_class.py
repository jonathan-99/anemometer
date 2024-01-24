try:
    import os
    import sys
    import csv
    import json
    import logging
    import datetime
    import re
except ImportError as e:
    logging.error("Importing error: " + str(e))


class DateCheckingClass:

    def __init__(self):
        self.good_date_regex = '([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])'
        self.bad_date_regex = '([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)'
        logging.debug("DateCheckingClass initiated")

    def _check_against_good_regex(self, test_item) -> bool:
        logging.debug("_check_against_good_regex()")
        p = re.compile(self.good_date_regex)
        a_match = p.match(test_item)
        if a_match:
            return True
        else:
            return False

    def correct_datetime_against_regex(self, in_list):
        logging.debug("correct_datetime_against_regex()")
        result = ""
        for count, value in enumerate(in_list):
            if not (self._check_against_good_regex(value)):
                result = value.split('.')[0].split(':')[0]
            in_list[count] = result
        return in_list
