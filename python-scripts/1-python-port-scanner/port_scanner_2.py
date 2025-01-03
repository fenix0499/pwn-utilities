#!/usr/bin/env python3

import socket
import argparse
import sys
from termcolor import colored

def get_arguments():
  parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
  parser.add_argument("-t", "--target", dest="target", help="Victim target to scan (Ex: -t 192.168.100.1)")
  parser.add_argument("-p", "--port", dest="port", help="Port range to scan (Ex: -p 1-100)")
  options = parser.parse_args()

  if options.target is None or options.port is None:
    parser.print_help()
    sys.exit(1)
  
  return options.target, options.port

def create_socket():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(1)
  return s

def port_scanner(host, port, s):
  try:
    s.connect((host, port))
    print(colored(f"\n[+] El puerto {port} está abierto", "green"))
  except (socket.timeout, ConnectionRefusedError):
    pass
  finally:
    s.close()

def parse_ports(portsString):
  if '-' in portsString:
    [startPort, endPort] = map(int, portsString.split('-'))
    return range(startPort, endPort + 1)
  elif ',' in portsString:
    return [int(port) for port in portsString.split(',')]
  else:
    return [int(portsString)]
  
def execute_scan(host, ports):
  for port in ports:
    socket = create_socket()
    port_scanner(host, port, socket)

def main():
  # host = input("\n[+] Introduce la dirección IP: ")
  host, portsString = get_arguments()
  formatted_ports = parse_ports(portsString)
  execute_scan(host, formatted_ports)


if __name__ == '__main__':
  main()
