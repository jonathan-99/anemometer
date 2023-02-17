import unittest
import counter


class test_counter(unittest.TestCase):
    def test_calculate_speed(self):
        """
        this tests the output is correct
        """
        good_time = 100
        good_value = 10
        with self.subTest():
            output = counter.calculate_speed(good_time, good_value)
            self.assertEqual(int(output), 12)

if __name__ == '__main__':
    unittest.main()



