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

    def test_create_instance(self):
        """
        Test that an instance is created.
        """
        with self.subTest():
            seconds = 5
            pin = 17
            a = counter.WindMonitor(seconds, pin)
            self.assertIsInstance(a, counter.WindMonitor)

    def test_add_tick(self):
        """
        Test that you can: add 5 ticks to an instance then, you can recall the interval, then reset count.
        """
        seconds = 5
        pin = 17
        b = counter.WindMonitor(seconds, pin)
        with self.subTest():
            b.add_count()
            b.add_count()
            b.add_count()
            b.add_count()
            b.add_count()
            self.assertEqual(b.show_count(), 5)
        with self.subTest():
            self.assertEqual(b.get_interval(), 5)
        with self.subTest():
            b.reset()
            self.assertEqual(b.show_count(), 0)

if __name__ == '__main__':
    unittest.main()
