try:
    import os
    import sys
    import csv
    import json
    import logging
    import ast
    import src.file_handler_class as filehander
except ImportError as e:
    sys.exit("Importing error: " + str(e))



class ConfigData:
    """
    This holds and retrieves the config file for all other files to call on.
    """


    def __init__(self, filename='config.json'):
        print("--This is the path -- {} - {} - {}".format(os.path.isfile(filename), os.path.exists(filename), filename))

        fileObject = filehander.FileHandlerClass(filename)
        data = fileObject.read_json_data_from_file(filename)
        print("Error trapping: {} - {}".format(type(data), data))
        if "error" in str(data).lower():
            self.set_all_default()
            print("__init__ if default")
        else:
            print("__init__ else - {}".format(data))
            self._set_path(data['path'])
            self._set_logging_path(data['logging_path'])
            self._set_log_filename(data['log_filename'])
            self._set_data_location(data['data_path'])
            self._set_server_port(data['simple-server-port'])
            self._set_logging_level(data['logging-level'])


    def _set_path(self, path_location="/opt/anemometer/") -> None:
        self.path = path_location

    def _set_logging_path(self, log_path="logging/") -> None:
        self.logging_path = log_path

    def _set_log_filename(self, filename="debugging.log") -> None:
        self.log_filename = filename

    def _set_data_location(self, location="data/") -> None:
        self.data_location = location

    def _set_server_port(self, number=6000) -> None:
        self.server_port = number

    def _set_logging_level(self, log_level="logging.DEBUG") -> None:
        self.logging_level = log_level

    def get_path(self) -> str:
        return self.path

    def get_logging_path(self) -> str:
        return self.logging_path

    def get_log_filename(self) -> str:
        return self.log_filename

    def get_data_location(self) -> str:
        return self.data_location

    def get_server_port(self) -> int:
        return int(self.server_port)

    def get_logging_level(self) -> str:
        return self.logging_level

    def set_all_default(self) -> None:
        self._set_path()
        self._set_logging_path()
        self._set_log_filename()
        self._set_data_location()
        self._set_server_port()
        self._set_logging_level()

    def show_all(self) -> str:
        output_string = str(self.path) \
            + str(self.logging_path) \
            + str(self.log_filename) \
            + str(self.data_location) \
            + str(self.server_port) \
            + str(self.logging_level)
        return output_string

