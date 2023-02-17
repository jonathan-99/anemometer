import unittest
from unittest.mock import patch, call
import counter

# @patch("RPi.GPIO.output", autospec=True)
class test_counter(unittest.TestCase):
    """
    This class tests all of the counter.py code
    """
    global in1pin
    in1pin = 17

    def test_calculating_speed(self):
        """
        This tests the calculating_speed() function within counter.py
        co = counter(self.in1Pin)
        mock_output.assert_has_calls([call(self.in1Pin, False),call(self.in2Pin, False)],any_order=True)
        """
        input_a = 100
        input_b = 10
        with self.subTest():
            """
            Correct values
            """
            output = counter.calculate_speed(input_a, input_b)
            self.assertTrue(output == 12, "Calculating speed works")
        with self.subTest():
            """
            Wrong values.
            """
            output = counter.calculate_speed(input_a, input_b)
            self.assertFalse(output == 10)



if __name__ == '__main__':
    unittest.main()
