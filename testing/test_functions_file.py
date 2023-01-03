import unittest
from src import functions


class TestFunction(unittest.TestCase):

    correct_date_regex = "([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])"
    correct_kph_regex = "([0-9]+).([0-9]+)"
    incorrect_date_regex = "([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)"

    def test_correct_list_function(self):
        test_correct_list = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]
        expected_date = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        expected_value = ['12.3', '10.3', '8.0']
        actual_a, actual_b = functions.reformat_data(test_correct_list)
        with self.subTest():
            print("sub test 1-a ")
            self.assertEqual(actual_a, expected_date)
        with self.subTest():
            print("sub test 1-b:")
            self.assertEqual(actual_b, expected_value)

    def test_incorrect_time(self):
        print("test 2")
        test_incorrect_time_list = ["2022-11-04 13:42:00.041034", "0.12", "2022-11-04 13:42:10.079134", "0.0"]
        expected_date = ['2022-11-04 13', '2022-11-04 13']
        expected_value = ['0.12', '0.0']
        actual_a, actual_b = functions.reformat_data(test_incorrect_time_list)
        with self.subTest():
            print("sub test 2-a:")
            self.assertEqual(actual_a, expected_date)
        with self.subTest():
            print("sub test 2-b:")
            self.assertEqual(actual_b, expected_value)

if __name__ == '__main__':
    unittest.main()
