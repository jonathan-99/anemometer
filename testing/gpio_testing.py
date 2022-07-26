import unittest
from unittest.mock import patch, call
import counter

''' This test checks the GPIO

https://www.reddit.com/r/Python/comments/5eddp5/mock_testing_rpigpio/
'''


@patch("RPi.GPIO.output", autospec=True)
class TestCounter(unittest.TestCase):
    inPin = 17

    def test_init(self, mock_output):
        """If you would MoterManager() stop motor when you build it your test looks like follow code"""
        mm = Counter(self.inPin)
        mock_output.assert_has_calls([call(self.in1Pin, False), False)], any_order=True)

    def test_10_clicks(self, mock_output):
        mm = MoterManager(self.in1Pin)
        mock_output.reset_mock
        mm.stop()
        mock_output.assert_has_calls([call(self.in1Pin, True), False)], any_order=True)

if __name__ == '__main__':
    unittest.main()
