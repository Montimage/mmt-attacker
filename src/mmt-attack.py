import sys
from attacks import find_attack_by_id, PCAP_ATTACK, SCRIPT_ATTACK
from utils import exec_command, get_application_path, check_if_interface_exist

TCPREPLAY_APP_NAME = 'tcpreplay-edit'
MMT_ATTACKER_VERSION = "0.1.0"


def startAttack(attackID, iface, targetIP, targetPort=None):
  """Start an attack

  Args:
      attackID (String): The attack ID
      targetIP (String): The target Ip address
      targetPort (String, optional): The target port number. Defaults to None.

  Returns:
      Boolean: True - the attack has been done
                False - cannot perform the attack
  """
  attack = find_attack_by_id(attackID)
  if attack != None:
    attackCMD = ""
    # Check the type of attack
    if attack.attackType == PCAP_ATTACK:
      tcpreplay_edit_path = get_application_path(TCPREPLAY_APP_NAME)

      if tcpreplay_edit_path == None:
        print(f"Need to install {TCPREPLAY_APP_NAME}")
        return False
      if not check_if_interface_exist(iface):
        print(f"Interface does not exist {iface}")
        return False
      attackCMD = attack.attack_command( tcpreplay_edit_path, iface, targetIP, targetPort)
    elif attack.attackType == SCRIPT_ATTACK:
      script_path = get_application_path(attack.exeApp)
      if script_path == None:
        print(f"Need to install {attack.exeApp}")
        return False
      attackCMD = attack.attack_command(script_path, iface, targetIP, targetPort)
    else:
      print(f"Unsupported attack type: {attack.attackType}")
      return False
    # Now we have the attack command
    print("Command to be executed: ")
    print(attackCMD)
    output = exec_command(attackCMD)
    print("Attack output:")
    print(output)
    return True
  else:
    print(f"Unknown attack: {attackID}")
    return False

if __name__ == '__main__':
  # attackID, iface, targetIP, targetPort=None
  argv_len = len(sys.argv)
  if  argv_len < 4:
    print("Invalid input arguments")
    print("python mmt-attack.py <attackID> <iface> <targetIP> [targetPort]")
  elif argv_len == 4:
    ret = startAttack(sys.argv[1],sys.argv[2],sys.argv[3])
    print(f"Attack result: {ret}")
  else:
    ret = startAttack(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print(f"Attack result: {ret}")
