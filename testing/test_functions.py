import unittest
from src import functions


class TestReformatData(unittest.TestCase):

    def test_input_list(self, test_list, expected_a, expected_b):
        actual_a, actual_b = functions.reformat_data(test_list)
        with self.subTest():
            self.assertEqual(actual_a, expected_a)
        with self.subTest():
            self.assertEqual(actual_b, expected_b)


class TestFunction(TestReformatData):
    test_correct_list = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]

    correct_date_regex = "([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])"
    correct_kph_regex = "([0-9]+).([0-9]+)"
    incorrect_date_regex = "([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)"
    test_incorrect_time_list = ["2022-11-04 13:42:00.041034","0.12","2022-11-04 13:42:10.079134", "0.0"]

    def test_correct_list(self, test_correct_list):
        expected_date = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        expected_value = ['12.3', '10.3', '8.0']
        self.test_input_list(test_correct_list, expected_date, expected_value)


    def test_incorrect_time(self, test_incorrect_time_list):
        expected_date = ['2022-11-04 13:42:00.041034', '2022-11-04 13:42:10.079134']
        expected_value = ['0.12', '0.0']
        self.test_input_list(test_incorrect_time_list, expected_date, expected_value)

if __name__ == '__main__':
    unittest.main()
