import sys, os
from utils import read_json_file

ATTACK_DATA_PATH = os.path.join(sys.path[0], "attacks.json")


PCAPS_PATH = os.path.join(sys.path[0], "pcaps")
SCRIPTS_PATH = os.path.join(sys.path[0], "scripts")
PCAP_ATTACK = "pcap"
SCRIPT_ATTACK = "script"
allAttacks = []

class MAttack:
  def __init__(self, attackId, attackName, description, attackType, fileName):
    self.attackName = attackName# Name of the attack - to show on the list
    self.attackId = attackId# ID of the attack
    self.description = description# Explain everything about the attack
    self.attackType = attackType# pcap -> attack by replaying a pcap file, script -> attack by executing a script
    self.fileName = fileName# the name of the file to be use for the attack, a pcap file or a script file

class PcapAttack(MAttack):
  def __init__(self, attackId, attackName, description, attackType,fileName, destIP, destPort=None):
    super().__init__(attackId, attackName, description, attackType,fileName)
    self.destPort = destPort
    self.destIP = destIP
  def attack_command(self, appPath, iface, targetIP, targetPort = None):
    """Generate the attack command to be executed in shell

    Args:
        appPath (String): The path to the tcpreplay-edit application
        iface (String): The interface will be send the traffic to
        targetIP (String): The target IP address
        targetPort (String, optional): The target port number. Defaults to None.

    Returns:
        String: a command to be executed in shell
    """
    cmd = f"{appPath} -i {iface} -tK --loop 1 -D {self.destIP}:{targetIP} -S {self.destIP}:{targetIP}"
    if targetPort != None:
      cmd = f"{cmd} -r {self.destPort}:{targetPort}"
    cmd = f"{cmd} {self.fileName}"
    return cmd

class ScriptAttack(MAttack):
  def __init__(self, attackId, attackName, description, attackType,fileName, exeApp):
    super().__init__(attackId, attackName, description, attackType,fileName)
    self.exeApp = exeApp
  def attack_command(self, appPath, targetIP, targetPort = None):
    """Generate the attack command to be executed in shell

    Args:
        appPath (String): The path to the script application, for example: /usr/bin/python, /usr/bin/python3.9, /usr/bin/node,
        iface (String): The interface will be send the traffic to
        targetIP (String): The target IP address
        targetPort (String, optional): The target port number. Defaults to None.

    Returns:
        String: a command to be executed in shell
    """
    return f"{appPath} {self.fileName} {targetIP} {targetPort}"

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
          if str(attack['fileName']).endswith('.py'):
            exeApp = "python"
          elif str(attack['fileName']).endswith('.js'):
            exeApp = "node"
          elif str(attack['fileName']).endswith('.sh'):
            exeApp = "sh"
          else:
            print(f"ERROR: Cannot find the executable application for the script: {attack['fileName']}")
            continue
        allAttacks.append(ScriptAttack(attack['attackId'], attack['attackName'], attack['description'], SCRIPT_ATTACK, os.path.join(SCRIPTS_PATH, attack['fileName']), exeApp))
      elif attack['attackType'] == PCAP_ATTACK:
        allAttacks.append(PcapAttack(attack['attackId'], attack['attackName'], attack['description'], PCAP_ATTACK, os.path.join(PCAPS_PATH, attack['fileName']), attack['destIP'], attack['destPort']))
      else:
        print(f"ERROR: Unsupported attack type: {attack['attackType']}")
        continue
    print(f"Total number of available attacks: {len(allAttacks)}")

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