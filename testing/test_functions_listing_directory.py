from ..src import functions as functions
import unittest
import os

class testListingDirectory(unittest.TestCase):

    def testListingDirectory(self):
        # os.chdir("C:/Users/local_admin/PycharmProjects/anemometer/")
        output = functions.listing_directory('test', 'testing/')
        with self.subTest():
            self.assertIsInstance(output, str)

    def testListFileDirectory(self):
        os.chdir("C:/Users/local_admin/PycharmProjects/anemometer/")
        output = functions.list_file_directory('testing/')
        with self.subTest():
            self.assertIsInstance(output, list)
        with self.subTest():
            self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
