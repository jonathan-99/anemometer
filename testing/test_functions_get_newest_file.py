from ..src import functions
import unittest
import datetime

class testGetNewestFile(unittest.TestCase):

    def get_two_dates(self):
        now = datetime.datetime.now()
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        return str(now)[0:10]+".txt", str(yesterday)[0:10]+".txt"
    def test_get_newest_file(self):
        one, two = self.get_two_dates()
        filenames = [one, two]
        output = functions.get_newest_file(filenames)
        with self.subTest():
            self.assertIsInstance(output, str)
        with self.subTest():
            self.assertEqual(one, output)

if __name__ == '__main__':
    unittest.main()