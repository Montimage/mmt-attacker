import sys
from attacks import find_attack_by_id, PCAP_ATTACK, SCRIPT_ATTACK, get_all_attack_ides
from utils import exec_command, get_application_path
from network_utils import get_online_interface

TCPREPLAY_APP_NAME = 'tcpreplay-edit'
MMT_ATTACKER_VERSION = "0.3.0"


def startAttack(attackID, arguments):
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
      iface = get_online_interface()
      if iface == None:
        print(f"Cannot get an online interface")
        return False
      print(f"Attack will be done on interface: {iface}")
      attackCMD = attack.attack_command( tcpreplay_edit_path, iface, arguments)
    elif attack.attackType == SCRIPT_ATTACK:
      script_path = get_application_path(attack.exeApp)
      if script_path == None:
        print(f"Need to install {attack.exeApp}")
        return False
      attackCMD = attack.attack_command(script_path, arguments)
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
  if  argv_len < 3:
    print("Invalid input arguments")
    print("python mmt-attack.py <attackID> <arguments>")
    print("Available attacks:")
    print(get_all_attack_ides())
  else:
    attackId = sys.argv[1].strip()
    arguments = sys.argv[2:]
    ret = startAttack(attackId, arguments)
    print(f"Attack result: {ret}")
