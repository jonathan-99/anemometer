import unittest
import master as an
import argparse


class TestAnemometer(unittest.TestCase):
    def test_main_function(self):
        """
        How do I test argparse?
        """
        parser = an.setup_argparse()
        with self.subTest():
            print("here: ")
            self.assertIsInstance(parser, argparse.ArgumentParser)

if __name__ == '__main__':
    unittest.main()