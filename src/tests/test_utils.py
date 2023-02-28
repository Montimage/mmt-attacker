import subprocess
import socket
import unittest
from unittest.mock import patch
from ..utils import get_application_path, exec_command, get_all_interfaces, check_if_interface_exist, get_ip_address

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

    def test_get_all_interfaces(self):
        expected_output = ['lo','enp0s1']
        actual_output = get_all_interfaces()
        self.assertEqual(expected_output, actual_output)

    # @patch('socket.if_nameindex', return_value=[])
    # def test_get_all_interfaces_no_interfaces(self, mock_if_nameindex):
    #     expected_output = []
    #     actual_output = get_all_interfaces()
    #     self.assertEqual(expected_output, actual_output)

    def test_interface_exists(self):
        iface = 'enp0s1'
        expected_output = True
        actual_output = check_if_interface_exist(iface)
        self.assertEqual(expected_output, actual_output)

    def test_interface_does_not_exist(self):
        iface = 'eth0'
        expected_output = False
        actual_output = check_if_interface_exist(iface)
        self.assertEqual(expected_output, actual_output)

    def test_get_ip_address(self):
        expected_output = '192.168.64.4'
        actual_output = get_ip_address()
        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
