import src.functions as functions
import unittest

class testHTMLTable(unittest.TestCase):
    def test_html_table(self):
        input_list = ['gpio_testing', 'main_testing', 'test_counter', 'test_faile_handler_functions', 'test_functions']
        output = functions.html_table(input_list)
        with self.subTest():
            self.assertIsInstance(output, list)
        with self.subTest():
            last_item = output[len(output)-1]
            self.assertEqual(last_item, '</table>')

if __name__ == '__main__':
    unittest.main()