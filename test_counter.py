import unittest
from unittest.mock import patch, call
import counter

# my hope is to test the GPIO input.
@patch("RPi.GPIO.output", autospec=True)
class MyTestCase(unittest.TestCase):
    in1Pin = 17

    def test_init(self, mock_output):
        """If you would counter() stop motor when you build it your test looks like follow code"""
        co = counter(self.in1Pin)
        mock_output.assert_has_calls([call(self.in1Pin, False),call(self.in2Pin, False)],any_order=True)


if __name__ == '__main__':
    unittest.main()
