import unittest
from ..src import functions


class Test_handle_input_list_datetime(unittest.TestCase):
    def test_handle_input_list_datetime(self):
        """
        This puts in a good, and three bad dates at various points in the list.
        """
        good_regex = '([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9])'
        bad_regex = '[a-z]+'
        good_list = ['22-06-16 22', '22-06-16 23', '22-06-17 00']
        bad_list_1 = ['22-06-16 22:02.02392', '22-06-16 23', '22-06-17 00']
        bad_list_2 = ['22-06-16 22', '22-06-16 23:01.2124', '22-06-17 00']
        bad_list_3 = ['22-06-16 22', '22-06-16 23', '22-06-17 00:33.39772']
        out_list = []
        with self.subTest():
            """
            Good list, good regex
            """
            out_list = functions.handle_input_list_datetime(good_list, good_regex)
            self.assertEqual(good_list, out_list)
        with self.subTest():
            """
            Bad list 1, good regex
            """
            out_list = functions.handle_input_list_datetime(bad_list_1, good_regex)
            self.assertEqual(bad_list_1, out_list)
        with self.subTest():
            """
            bad list 2, good regex
            """
            out_list = functions.handle_input_list_datetime(bad_list_2, good_regex)
            self.assertEqual(bad_list_2, out_list)
        with self.subTest():
            out_list = functions.handle_input_list_datetime(bad_list_3, good_regex)
            self.assertEqual(bad_list_3, out_list)

if __name__ == '__main__':
    unittest.main()
