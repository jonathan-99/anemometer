import unittest
import os


def import_all_tests(directory="anemometer/testing/"):
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        # Get a list of all files in the directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"Error: {e}")
        return []


class TestAll(unittest.TestCase):

    def run_all_tests(self):
        loader = unittest.TestLoader()

        # Load tests from the specified files
        suite = loader.discover(start_dir='.', pattern='test_*.py', top_level_dir='.')

        # Run the tests
        runner = unittest.TextTestRunner()
        return runner.run(suite)


if __name__ == '__main__':
    file_list = import_all_tests("anemometer/testing/")  # perhaps unnecessary.
    test_result = TestAll()

    # Print the test result
    print(f"Tests run: {test_result.testsRun}")
    print(f"Failures: {len(test_result.failures)}")
    print(f"Errors: {len(test_result.errors)}")
