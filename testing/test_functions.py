import unittest
from ..src import functions


class TestFunction(unittest.TestCase):
    global correct_list, correct_date_regex, correct_kph_regex, incorrect_date_regex, test_incorrect_time_list

    correct_list = ['22-06-16 22', '12.3', '22-06-16 23', '10.3', '22-06-17 00', '8.0']
    correct_date_regex = "([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])"
    correct_kph_regex = "([0-9]+).([0-9]+)"
    incorrect_date_regex = "([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)"
    test_incorrect_time_list = ["2022-11-04 13:42:00.041034", "0.12", "2022-11-04 13:42:10.079134", "0.0"]


    def test_correct_list(self):
        """
        This has the correct format of dates (inc hours) and values (ticks).
        """
        global correct_list, correct_date_regex, correct_kph_regex, incorrect_date_regex, test_incorrect_time_list

        expected_date = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        expected_value = ['12.3', '10.3', '8.0']

        output_1, output_2 = functions.split_list(correct_list)
        with self.subTest():
            self.assertEqual(output_1, expected_date)
        with self.subTest():
            self.assertEqual(output_2, expected_value)


    def test_incorrect_time(self):
        actual_date = ['2022-11-04 13:42:00.041034', '2022-11-04 13:42:10.079134']
        expected_date = ['2022-11-04 13', '2022-11-04 13']
        expected_value = ['0.12', '0.0']
        with self.subTest():
            output_1 = functions.handle_input_list_datetime(actual_date)
            self.assertEqual(output_1, expected_date)


if __name__ == '__main__':
    unittest.main()
