import unittest
from ..network_utils import get_all_interfaces, check_if_interface_exist, get_ip_address_by_machine_hostname, get_online_interface, get_online_ip_address

class TestNetworkUtils(unittest.TestCase):
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

    def test_get_online_ip_address(self):
        expected_output = '192.168.64.4'
        actual_output = get_online_ip_address()
        self.assertEqual(expected_output, actual_output)

    def test_get_online_interface(self):
        expected_output = 'enp0s1'
        actual_output = get_online_interface()
        self.assertEqual(expected_output, actual_output)

    def test_get_ip_address_by_machine_hostname(self):
        expected_output = '192.168.64.4'
        actual_output = get_ip_address_by_machine_hostname()
        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
