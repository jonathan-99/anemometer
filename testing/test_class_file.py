import os
import unittest
import json
import src.class_file as ConfigData

class TestConfigData(unittest.TestCase):

    def setUp(self):
        self.config = ConfigData.ConfigData()

    def test_read_json_data_from_file_success(self):
        data = self.config.read_json_data_from_file('test_class_file.json')
        expected_data = {"path": "/anemometer/testing", "log_filename": "test.log"}
        self.assertDictEqual(data, expected_data)

    def test_read_json_data_from_file_file_not_found(self):
        data = self.config.read_json_data_from_file('non_existent_file.json')
        self.assertEqual(data, {"Error": "File not found"})

    def test_read_json_data_from_file_invalid_json(self):
        data = self.config.read_json_data_from_file('invalid.json')
        self.assertEqual(data, {"Error": "Invalid JSON format or empty file"})

    def test_init_with_config_file(self):
        config_object = ConfigData.ConfigData('test_config.json')
        data = config_object.get_path()
        self.assertEqual(data, "/opt/anemometer/testing/")

    def test_get_path(self):
        self.assertEqual(self.config.get_path(), "/opt/anemometer/")

    def test_get_logging_path(self):
        self.assertEqual(self.config.get_logging_path(), "logging/")

    def test_get_log_filename(self):
        self.assertEqual(self.config.get_log_filename(), "debugging.log")

    def test_get_data_location(self):
        self.assertEqual(self.config.get_data_location(), "data/")

    def test_get_server_port(self):
        self.assertEqual(self.config.get_server_port(), 6000)

    def test_get_logging_level(self):
        self.assertEqual(self.config.get_logging_level(), "logging.debug")

    def test_set_all_default(self):
        self.config.set_all_default()
        self.assertEqual(self.config.get_path(), "/opt/anemometer/")
        self.assertEqual(self.config.get_logging_path(), "logging/")
        self.assertEqual(self.config.get_log_filename(), "debugging.log")
        self.assertEqual(self.config.get_data_location(), "data/")
        self.assertEqual(self.config.get_server_port(), 6000)
        self.assertEqual(self.config.get_logging_level(), "logging.debug")

    def test_show_all(self):
        expected_output = {
            "path": "/opt/anemometer/",
            "logging_path": "logging/",
            "log_filename": "debugging.log",
            "data_location": "data/",
            "server_port": 6000,
            "logging_level": "logging.debug"
        }
        self.assertEqual(self.config.show_all(), expected_output)

if __name__ == '__main__':
    unittest.main()
