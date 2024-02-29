import unittest
from ..src import functions


class TestFunction(unittest.TestCase):

    correct_date_regex = "([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])"
    correct_kph_regex = "([0-9]+).([0-9]+)"
    incorrect_date_regex = "([0-9]+-[0-9]+-[0-9]+ [0-9]+):([0-9]+):([0-9]+)"


    def test_split_list_function(self):
        """
        Does this split the inputted data files data correctly (date, speed, date, speed etc)?
        """

        test_correct_list = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]
        test_incorrect_list = ["22-06-16 22", "22-06-16 23", "10.3", "8.0"]
        expected_date = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        expected_value = ['12.3', '10.3', '8.0']
        output_date, output_value = functions.split_list(test_correct_list)
        with self.subTest():
            """
            Correctly handle correct date list.
            """
            self.assertEqual(output_date, expected_date)
        with self.subTest():
            """
            Correctly handle correct value list.
            """
            self.assertEqual(output_value, expected_value)
        wrong_output_date, wrong_output_value = functions.split_list(test_incorrect_list)
        with self.subTest():
            """
            How should I handle wrong input (date)?
            """
            self.assertFalse(wrong_output_date == expected_date)
        with self.subTest():
            """
            How should I handle wrong input (value)?
            """
            self.assertFalse(wrong_output_value == expected_value)


    def test_correct_list_function(self):

        test_correct_list = ["22-06-16 22", "12.3", "22-06-16 23", "10.3", "22-06-17 00", "8.0"]
        expected_date = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        expected_value = ['12.3', '10.3', '8.0']
        actual_a, actual_b = functions.split_list(test_correct_list)
        actual_a = functions.handle_input_list_datetime(actual_a)
        with self.subTest():
            self.assertEqual(actual_a, expected_date)
        with self.subTest():
            self.assertEqual(actual_b, expected_value)

    def test_incorrect_time(self):
        test_incorrect_time_list = ["2022-11-04 13:42:00.041034", "0.12", "2022-11-04 13:42:10.079134", "0.0"]
        expected_date = ['2022-11-04 13', '2022-11-04 13']
        expected_value = ['0.12', '0.0']
        actual_a, actual_b = functions.split_list(test_incorrect_time_list)
        actual_a = functions.handle_input_list_datetime(actual_a)
        with self.subTest():
            self.assertEqual(actual_a, expected_date)
        with self.subTest():
            self.assertEqual(actual_b, expected_value, "sub test 2-b success")

if __name__ == '__main__':
    unittest.main()
