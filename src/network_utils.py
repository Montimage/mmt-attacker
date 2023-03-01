import socket
import netifaces as ni

def get_all_interfaces():
    """Get all available interfaces

    Returns:
        List: List of available interface
    """
    return ni.interfaces()

def check_if_interface_exist(iface):
    """Check if a given interface exist in the machine

    Args:
        iface (String): Interface for testing

    Returns:
        Boolean: True - if the interface exist
                False - otherwise
    """
    if iface in ni.interfaces():
        return True
    return False

def get_ip_address_by_machine_hostname():
    """Get IP address of the current machine by its hostname

    Returns:
        String: The IP address
    """
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    return ipAddress

def get_online_ip_address(online_server_ip="8.8.8.8"):
    """Get the ip address of the current machine which can connect to the given online server

    Args:
        online_server_ip (String, optional): The online server that need to be connected to. Defaults to "8.8.8.8".

    Returns:
        String: The IP address of the current machine which can connect to the given server
        None: if there is no IP address that can reach the given online server
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((online_server_ip,80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_online_interface(online_server_ip = "8.8.8.8"):
    """Get the interface name which can see the given online server

    Args:
        online_server_ip (String, optional): The online server that need to bee seen. Defaults to "8.8.8.8".

    Returns:
        String: The name of the interface
        None: if there is no interface can see the given online server
    """
    online_ip = get_online_ip_address(online_server_ip)
    if online_ip == None:
        print(f"The machine cannot see the given IP address {online_server_ip}")
        return None
    for intf in ni.interfaces():
        intf_addrs = ni.ifaddresses(intf)
        if socket.AF_INET in intf_addrs:
            ip = intf_addrs[socket.AF_INET][0]['addr']
            if ip == online_ip:
                return intf
    return None
