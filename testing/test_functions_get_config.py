import src.functions as functions
import unittest
class testGetConfig(unittest.TestCase):
    def test_get_config(self):
        test_config = functions.get_config()
        with self.subTest():
            self.assertEqual(test_config.get_logging_path(), 'logging/')
        with self.subTest():
            self.assertEqual(test_config.get_log_filename(), 'debugging.log')
        with self.subTest():
            self.assertIsInstance(test_config.show_all(), str)

if __name__ == '__main__':
    unittest.main()