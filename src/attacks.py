import sys, os
from utils import read_json_file

ATTACK_DATA_PATH = os.path.join(sys.path[0], "attacks.json")


PCAPS_PATH = os.path.join(sys.path[0], "pcaps")
SCRIPTS_PATH = os.path.join(sys.path[0], "scripts")
PCAP_ATTACK = "pcap"
SCRIPT_ATTACK = "script"
allAttacks = []

class MAttack:
  def __init__(self, attackId, attackName, description, attackType):
    self.attackName = attackName# Name of the attack - to show on the list
    self.attackId = attackId# ID of the attack
    self.description = description# Explain everything about the attack
    self.attackType = attackType# pcap -> attack by replaying a pcap file, script -> attack by executing a script

class PcapAttack(MAttack):
  def __init__(self, attackId, attackName, description, attackType, pcapFileName, destIP, destPort=None):
    super().__init__(attackId, attackName, description, attackType)
    self.pcapFileName = pcapFileName
    self.destPort = destPort
    self.destIP = destIP
  def attack_command(self, appPath, iface, arguments):
    """Generate the attack command to be executed in shell

    Args:
        appPath (String): The path to the tcpreplay-edit application
        iface (String): The interface will be send the traffic to
        targetIP (String): The target IP address
        targetPort (String, optional): The target port number. Defaults to None.

    Returns:
        String: a command to be executed in shell
    """
    if len(arguments) < 1:
      print(f"ERROR: Missing input")
      return False
    targetIP = arguments[0]
    cmd = f"{appPath} -i {iface} -tK --loop 1 -D {self.destIP}:{targetIP} -S {self.destIP}:{targetIP}"
    if len(arguments) == 2:
      targetPort = arguments[1]
      cmd = f"{cmd} -r {self.destPort}:{targetPort}"
    cmd = f"{cmd} {self.pcapFileName}"
    return cmd

class ScriptAttack(MAttack):
  def __init__(self, attackId, attackName, description, attackType, scriptFileName, exeApp, extraParametersHelper):
    super().__init__(attackId, attackName, description, attackType)
    self.scriptFileName = scriptFileName
    self.exeApp = exeApp
    self.extraParametersHelper = extraParametersHelper

  def attack_command(self, appPath, arguments):
    """Generate the attack command to be executed in shell

    Args:
        appPath (String): The path to the script application, for example: /usr/bin/python, /usr/bin/python3.9, /usr/bin/node,
        arguments (String, optional): The input arguments of the attack script. Defaults to None - means execute the script without any parameter.

    Returns: con
        String: a command to be executed in shell
    """
    inputParameter = ' '.join(arguments)
    print(f"Arguments: {inputParameter}")
    return f"{appPath} {self.scriptFileName} {inputParameter}"

def load_attacks_file(attacksFilePath):
  if len(allAttacks) > 0:
    print("All attacks have been loaded")
    return
  print(f"Loading the attack data from {attacksFilePath}")
  jsonData = read_json_file(attacksFilePath)
  if jsonData != None and len(jsonData) > 0:
    print(f"Number of attack json objects: {len(jsonData)}")
    for attack in jsonData:
      if attack['attackType'] == SCRIPT_ATTACK:
        exeApp = attack['exeApp']
        if exeApp == None:
          # auto detect the exeApp by extension of the script
          if str(attack['scriptFileName']).endswith('.py'):
            exeApp = "python"
          elif str(attack['scriptFileName']).endswith('.js'):
            exeApp = "node"
          elif str(attack['scriptFileName']).endswith('.sh'):
            exeApp = "sh"
          else:
            print(f"ERROR: Cannot find the executable application for the script: {attack['scriptFileName']}")
            continue
        allAttacks.append(ScriptAttack(attack['attackId'], attack['attackName'], attack['description'], SCRIPT_ATTACK, os.path.join(SCRIPTS_PATH, attack['scriptFileName']), exeApp, attack['extraParametersHelper']))
      elif attack['attackType'] == PCAP_ATTACK:
        if hasattr(attack, 'destPort'):
          allAttacks.append(PcapAttack(attack['attackId'], attack['attackName'], attack['description'], PCAP_ATTACK, os.path.join(PCAPS_PATH, attack['pcapFileName']), attack['destIP'], attack['destPort']))
        else:
          allAttacks.append(PcapAttack(attack['attackId'], attack['attackName'], attack['description'], PCAP_ATTACK, os.path.join(PCAPS_PATH, attack['pcapFileName']), attack['destIP'], None))
      else:
        print(f"ERROR: Unsupported attack type: {attack['attackType']}")
        continue
    print(f"Total number of available attacks: {len(allAttacks)}")
    # print(allAttacks)

def get_all_attacks():
  """Get all available attacks

  Returns:
      List: List of all attack
  """
  if len(allAttacks) == 0:
    load_attacks_file(ATTACK_DATA_PATH)
  return allAttacks

def get_all_attack_ides():
  """Get all attack ids

  Returns:
      List: list of id of all available attack
  """
  ids = []
  if len(allAttacks) == 0:
    load_attacks_file(ATTACK_DATA_PATH)
  for a in allAttacks:
    ids.append(a.attackId)
  return ids

def find_attack_by_id(attackId):
  """Find an attack by givenID

  Args:
      attackId (String): The ID of the attack

  Returns:
      MAttack: the attack to be executed
      None: the attack does not exist
  """
  if len(allAttacks) == 0:
    load_attacks_file(ATTACK_DATA_PATH)
  for a in allAttacks:
    if a.attackId == attackId:
      return a
  return None

# load_attacks_file(ATTACK_DATA_PATH)