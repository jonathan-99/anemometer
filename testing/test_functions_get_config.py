from src.class_file import ConfigData
import unittest
class testGetConfig(unittest.TestCase):
    def test_get_config(self):
        """
        need testing config location
        """
        configObject = ConfigData
        with self.subTest():
            self.assertEqual(configObject.get_logging_path(), 'logging/')
        with self.subTest():
            self.assertEqual(configObject.get_log_filename(), 'debugging.log')
        with self.subTest():
            self.assertIsInstance(configObject.show_all(), str)

if __name__ == '__main__':
    unittest.main()