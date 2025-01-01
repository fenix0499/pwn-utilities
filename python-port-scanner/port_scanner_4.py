#!/usr/bin/env python3

import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

open_sockets = []

def def_handler(sig, frame):
  print(colored("\n[!] Saliendo del programa...", "red"))

  for s in open_sockets:
    s.close()

  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
  parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
  parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scan (Ex: -t 192.168.100.1)")
  parser.add_argument("-p", "--port", dest="port", required=True, help="Port range to scan (Ex: -p 1-100)")
  options = parser.parse_args()
  
  return options.target, options.port

def create_socket():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(1)
  open_sockets.append(s)
  return s

def port_scanner(host, port):
  new_socket = create_socket()

  try:
    new_socket.connect((host, port))
    new_socket.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
    response = new_socket.recv(1024).decode(errors='ignore').split('\n')
    if response:
      print(colored(f"\n[+] El puerto {port} está abierto - {response[0]}", "green"))
      for line in response:
        print(colored(line, 'grey'))
    else:
      print(colored(f"\n[+] El puerto {port} está abierto", "green"))
  except (socket.timeout, ConnectionRefusedError):
    pass
  finally:
    new_socket.close()

def parse_ports(portsString):
  if '-' in portsString:
    [startPort, endPort] = map(int, portsString.split('-'))
    return range(startPort, endPort + 1)
  elif ',' in portsString:
    return [int(port) for port in portsString.split(',')]
  else:
    return [int(portsString)]
  
def execute_scan(host, ports):
  # threads = []

  # for port in ports:
  #   thread = threading.Thread(target=port_scanner, args=(host, port))
  #   threads.append(thread)
  #   thread.start()

  # for thread in threads:
  #   thread.join()
  with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(lambda port: port_scanner(host, port), ports)

def main():
  # host = input("\n[+] Introduce la dirección IP: ")
  host, portsString = get_arguments()
  formatted_ports = parse_ports(portsString)
  execute_scan(host, formatted_ports)


if __name__ == '__main__':
  main()
