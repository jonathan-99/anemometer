from ..src import functions
import unittest
import datetime

class testGetYesterdaysDate(unittest.TestCase):

    def get_two_dates(self):
        now = datetime.datetime.now()
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        return str(now)[0:10], str(yesterday)[0:10]

    def test_get_yesterdays_date(self):
        one, two = self.get_two_dates()
        filenames = [one, two]
        output = functions.get_yesterdays_date()
        with self.subTest():
            self.assertEqual(output, two)
        with self.subTest():
            self.assertIsInstance(output, str)

if __name__ == '__main__':
    unittest.main()