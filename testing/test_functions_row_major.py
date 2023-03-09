import src.functions as functions
import unittest

class testRowMajor(unittest.TestCase):
    def test_row_major_1(self):
        input_list = ['1', '2', '3']
        sub_len = len(input_list)
        output = functions.row_major(input_list, sub_len)
        with self.subTest():
            self.assertIsInstance(output, list)
        with self.subTest():
            self.assertEqual(input_list, output)

    def test_row_major_2(self):
        input_list = ['2022-11-04 13', '2.3', '2022-11-04 14', '4.2']
        sub_len = len(input_list)
        output = functions.row_major(input_list, sub_len)
        with self.subTest():
            self.assertIsInstance(output, list)
        with self.subTest():
            self.assertEqual(input_list, output)


if __name__ == '__main__':
    unittest.main()