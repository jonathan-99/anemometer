from ..src import functions as functions
import unittest

class testCreateHTMLPageWrapper(unittest.TestCase):
    def test_create_html_page_wrapper(self):
        output_title, end_tags = functions.create_html_page_wrapper('test')
        with self.subTest():
            if 'test' in output_title:
                self.assertTrue
            else: self.assertFalse
        with self.subTest():
            self.assertEqual(end_tags, "</body></html>")


if __name__ == '__main__':
    unittest.main()