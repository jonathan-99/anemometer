try:
    import os
    import sys
    import csv
    import json
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))

class config_data():
    """
    This holds and retrieves the config file for all other files to call on.
    """

    def __init__(self):
        self.logging_location = ""
        self.data_location = ""
        self.server_port = ""

    def set_logging_location(self, location="opt/anemometer/logging/log.txt") -> None:
        self.logging_location = location

    def set_data_location(self, location="opt/anemometer/data") -> None:
        self.data_location = location

    def set_server_port(self, number=6000) -> None:
        self.server_port = number

    def get_logging_location(self) -> str:
        return self.logging_location

    def get_data_location(self) -> str:
        return self.data_location

    def get_server_port(self) -> int:
        return self.server_port

    def show_all(self) -> str:
        output_string = str(self.logging_location) \
            + str(self.data_location) \
            + str(self.server_port)
        return output_string