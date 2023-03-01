mmt-attacker

Generate the attack traffic from a pcap file or by executing a script

# Install

Install some dependencies

```sh
sudo apt-get install python3.9-dev
```

```sh
pip install -r requirements.txt
```

# Commands

```sh
cd mmt-attacker/
python  src/mmt-attack.py <attack_id> <interface> <target_ip> [target_port]
```

# Example

## SSH brute force attack
```sh
python3.10  src/mmt_attack.py ssh-bruteforce-attack 192.168.64.5 22
```

```sh
python3.10  src/mmt_attack.py sql-injection-attack 192.168.64.5 80
```

```sh
python3.10  src/mmt_attack.py http-version-not-correct 192.168.64.5
```

# Add a new attack

Open and modify the `src/attacks.json` file with the required informations:
For a pcap based attack
```jsonc
  {
    "attackId":"pcap-attack-71", # Unique ID to identify the attack
    "attackName":"HTTP version is not correct", # Name of the attack - can be use to show on a dropdown menu
    "description":"Detect a request which has a HTTP version is not normal", # Description of the attack - describe what is the attack about, etc...
    "attackType": "pcap", # Type of the attack - support: pcap - attack based on a pcap file, script - attack by executing a script
    "fileName":  "71.http_version.pcap", # pcap file name which contains the attack -> the pcap file must be placed in location: src/pcaps/
    "destIP": "192.168.56.1", # The destination of the attack (target IP) in the original pcap file (can be found by using Wireshark - or MMT security)
    "destPort": 80 # The target port of original pcap file
  }
```

For a script based attack
```jsonc
{
    "attackId":"script-attack-01",
    "attackName":"SSH BruteForce Attack",
    "description":"SSH BruteForce Attack",
    "attackType": "script",
    "fileName":  "ssh-brute-force.py", # The script that will be execute to generate the attack - must be placed in location: src/scripts/
    "exeApp": "python3.10" # The execute application to launch the attack, depends on the script: python, node, or sh (shell)
  }
```
# References

[PCAP FROM WEB SERVER WITH LOG4J ATTEMPTS & LOTS OF OTHER PROBING/SCANNING](https://www.malware-traffic-analysis.net/2021/12/14/index.html)