try:
    import os
    import sys
    import csv
    import json
    import logging
    import ast
except ImportError as e:
    logging.debug("Importing error: " + str(e))


class ConfigData:
    """
    This holds and retrieves the config file for all other files to call on.
    """

    @staticmethod
    def read_json_data_from_file(filename: str) -> dict:
        logging.debug("read_json_data_from_file({})".format(filename))
        try:
            with open(filename, 'r', encoding="utf-8") as fileObject:
                data = json.load(fileObject)
                logging.debug("read_json_data_from_file() - data contents: {}".format(data))
                return data
        except FileNotFoundError:
            logging.warning("current files - {} ".format(os.listdir('.')))
            logging.warning("JSON file not found: {}".format(filename))
            return {"Error": "File not found"}
        except json.decoder.JSONDecodeError as err:
            logging.warning("current files - {} ".format(os.listdir('.')))
            logging.error("Error reading JSON file: {}".format(err))
            return {"Error": "Invalid JSON format or empty file"}

    def __init__(self, filename='config.json'):
        logging.debug("--This is the path -- {} - {} - {}".format(os.path.isfile(filename),
                                                                  os.path.exists(filename), filename))
        try:
            file_object = self.read_json_data_from_file(filename)
            print("Error trapping: {} - {}".format(type(file_object), file_object))
            if "error" in str(file_object).lower() or not file_object:
                self.set_all_default()
                print("__init__ if default")
            else:
                print("__init__ else - {}".format(file_object))
                self._set_path('/opt/anemometer/')
                self._set_logging_path('logging/')
                self._set_log_filename('debugging.log')
                self._set_data_location('data/')
                self._set_server_port(6000)
                self._set_logging_level('logging.debug')
        except ImportError as err:
            logging.error("Importing error: " + str(err))

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

    def show_all(self) -> dict:
        output_dict = {
            "path": str(self.path),
            "logging_path": str(self.logging_path),
            "log_filename": str(self.log_filename),
            "data_location": str(self.data_location),
            "server_port": str(self.server_port),
            "logging_level": str(self.logging_level)
        }

        return output_dict
