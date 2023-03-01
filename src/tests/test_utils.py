import subprocess
import unittest
from unittest.mock import patch
from ..utils import get_application_path, exec_command

class TestUtils(unittest.TestCase):
    # def test_get_application_path_success(self):
    #     appName = 'tcpreplay-edit'
    #     expected_app_path = '/usr/bin/tcpreplay-edit'
    #     self.assertEqual(getApplicationPath(appName), expected_app_path)

    def test_get_application_path_failure(self):
        appName = 'non_existent_app'
        self.assertIsNone(get_application_path(appName))

    @patch('subprocess.check_output')
    def test_exec_command_success(self, mock_check_output):
        # Define a test command and its expected output
        test_cmd = 'echo "Hello, World!"'
        expected_output = 'Hello, World!'

        # Configure the mock check_output function to return the test output
        mock_check_output.return_value = expected_output.encode()

        # Call the function and check the result
        result = exec_command(test_cmd)
        self.assertEqual(result, expected_output)

    @patch('subprocess.check_output')
    def test_exec_command_error(self, mock_check_output):
        # Define a test command that will raise an error
        test_cmd = 'invalid_command'

        # Configure the mock check_output function to raise a CalledProcessError
        mock_check_output.side_effect = subprocess.CalledProcessError(1, test_cmd, b'Command not found')

        # Call the function and check that it returns None
        result = exec_command(test_cmd)
        self.assertIsNone(result)
if __name__ == '__main__':
    unittest.main()
