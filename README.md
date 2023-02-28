mmt-attacker

Generate the attack traffic from a pcap file or by executing a script

# Install

```sh
pip install -r requirements.txt
```

# Commands

```sh
cd mmt-attacker/
python  src/mmt-attack.py <attack_id> <interface> <target_ip> [target_port]
```
Example

```sh
python3.10  src/mmt-attack.py script-attack-01 enp0s1 192.168.64.5 22
```

```sh
python3.10  src/mmt-attack.py pcap-attack-71 enp0s1 192.168.64.5
```

# References

[PCAP FROM WEB SERVER WITH LOG4J ATTEMPTS & LOTS OF OTHER PROBING/SCANNING](https://www.malware-traffic-analysis.net/2021/12/14/index.html)

