#!/usr/bin/env python3

import argparse
from termcolor import colored
import subprocess
from typing import List
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
  print("\n[!] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def getArguments():
  parser = argparse.ArgumentParser(description="Herramienta para descubrir hosts activos en una red (ICMP)")
  parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

  args = parser.parse_args()

  return args.target

def parseTarget(targetString: str):
  # 192.168.100.1-100
  targetStringSplited = targetString.split('.')
  firstThreeOctets = '.'.join(targetStringSplited[:3])

  if len(targetStringSplited) == 4:
    if "-" in targetStringSplited[3]:
      [start, end] = targetStringSplited[3].split('-')
      return [f"{firstThreeOctets}.{i}" for i in range(int(start), int(end) + 1)]
    else:
      return [targetString]
  else:
    print(colored("[!] El formato de IP o rango de IP no es valido...", 'red'))
    sys.exit(1)

def hostDiscovery(target: str):
  try:
     ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)

     if ping.returncode == 0:
       print(colored(f"\t[i] La IP {target} - ACTIVE", 'green'))
  except subprocess.TimeoutExpired:
    pass

def main():
  targetString = getArguments()
  targets: List[str] = parseTarget(targetString)

  print("\n[+] Hosts activos en la red...\n")

  maxThreads = 100

  with ThreadPoolExecutor(max_workers=maxThreads) as executor:
    executor.map(hostDiscovery, targets)


if __name__ == '__main__':
  main()
