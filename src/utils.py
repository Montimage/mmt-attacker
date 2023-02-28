import subprocess, socket, json

allNetworkInterfaces = []
def exec_command(cmd):
    """Execute a command in shell and return the output

    Args:
        cmd (String): The command to be executed

    Returns:
        String: The output after executing the command
    """
    try:
        output = subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        print("\nERROR: command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        return None

def get_application_path(appName):
    """Get the absolute path of a given application
    Only work on the system with `which` command

    Args:
        appName (String): application name

    Returns:
        String: absoluted path of the application
        None: if the application does not exist
    """
    cmd = "which " + appName
    return exec_command(cmd)

def get_all_interfaces():
    """Get all available interfaces

    Returns:
        List: List of available interface
        None: if there is no interface
    """
    if len(allNetworkInterfaces) == 0:
        for iface in socket.if_nameindex():
            allNetworkInterfaces.append(iface[1])
    return allNetworkInterfaces

def check_if_interface_exist(iface):
    """Check if a given interface exist in the machine

    Args:
        iface (String): Interface for testing

    Returns:
        Boolean: True - if the interface exist
                False - otherwise
    """
    get_all_interfaces()
    if iface in allNetworkInterfaces:
        return True
    return False

def get_ip_address():
    """Get IP address of the current machine by its hostname

    Returns:
        String: The IP address
    """
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    return ipAddress

def read_json_file(filePath):
    """Read a json file and return JSON object(s)

    Args:
        filePath (String): path to the JSON file

    Returns:
        JSONObject: JSONObject
    """
    try:
        # Open the JSON file for reading
        with open(filePath, 'r') as f:
            # Load the contents of the file into a dictionary
            jsonData = json.load(f)
            # Access the contents of the dictionary
            return jsonData
    except FileNotFoundError:
        print('Error: File not found.')
        return None
    except json.JSONDecodeError:
        print('Error: Invalid JSON format.')
        return None
    except Exception as e:
        print('Error:', e)
        return None
