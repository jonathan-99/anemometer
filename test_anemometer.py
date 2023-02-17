import unittest
import anemometer

class test_anemometer(unittest.TestCase):
    def test_main_function(self):
        """
        Test arg parser.
        """
        with self.subTest():
            parser = anemometer.setup_argparse()
            parsed = parser.parse_args('-c')
            self.assertTrue(parsed.capture)

if __name__ == '__main__':
    unittest.main()