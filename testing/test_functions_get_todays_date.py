import src.functions as functions
import unittest
import datetime

class testGetTodaysDate(unittest.TestCase):
    def get_two_dates(self):
        now = datetime.datetime.now()
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        return 'data/' + str(now)[0:10] + '.txt', 'data/' + str(yesterday)[0:10]+'.txt'
    def test_get_todays_date(self):
        one, two = self.get_two_dates()
        filenames = [one, two]
        output = functions.get_todays_date()
        with self.subTest():
            self.assertEqual(output, one)
        with self.subTest():
            self.assertIsInstance(output, str)

if __name__ == '__main__':
    unittest.main()