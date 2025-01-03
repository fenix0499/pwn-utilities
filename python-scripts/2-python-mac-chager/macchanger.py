#!/usr/bin/env python3

import argparse
import subprocess
from termcolor import colored
import signal
import sys
import re

# Para listar OUI's para una nueva mac
# macchanger -l

# Para revisar el status de la interfaz de red\
# macchanger -s ens33

# Para volver a asignar la mac predeterminada...
# macchanger -p ens33

def def_handler(sig, frame):
  print(colored("\n[+] Saliendo...\n", 'red'))
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def getArguments():
  parser = argparse.ArgumentParser(description="Herramienta para cambiar la direccion MAC de una interfaz de red.")
  parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red.")
  parser.add_argument("-m", "--mac", required=True, dest="macAddress", help="Nueva direccion MAC para la interfaz de red.")

  options = parser.parse_args()
  return options.interface, options.macAddress

def isValidInput(interface: str, macAddress: str):
  isValidInterface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
  isValidMacAddress = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}', macAddress)
  return isValidInterface and isValidMacAddress

def changeMacAddress(interface: str, macAddress: str):
  if isValidInput(interface, macAddress):
    subprocess.run(["ifconfig", interface, "down"]) # Dar de baja la interfaz...
    subprocess.run(["ifconfig", interface, "hw", "ether", macAddress]) # Cambio de mac address...
    subprocess.run(["ifconfig", interface, "up"]) # Dar de alta la interfaz...

    print(colored("\n[+] La MAC ha sido cambiada exitosamente...\n"))
  else:
    print(colored("\n[!] Los datos introducidos no son correctos...\n", 'red'))

def main():
  [interface, macAddress] = getArguments()
  changeMacAddress(interface, macAddress)

if __name__ == '__main__':
  main()
