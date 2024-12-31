#!/usr/bin/env python3

import socket
from termcolor import colored

host = input("\n[+] Introduce la dirección IP: ")
# port = int(input("\n[+] Introduce el puerto a escanear: "))

def create_socket():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Este timeout es para cuando la direccion ipv4 a la que nos estamos queriendo conectar no exista, delimitar que  tiene un segundo para conectarse o aborte la conexion...
  s.settimeout(1)
  return s


def port_scanner(port, s):
  try:
    # Esta forma de hacer la conexion si el puerto esta cerrado el metodo mandara un error...
    s.connect((host, port))
    print(colored(f"\n[+] El puerto {port} está abierto", "green"))

    # s.close()
  except (socket.timeout, ConnectionRefusedError):
    pass
    # print(colored(f"[!] El puerto {port} está cerrado", "red"))
  finally:
    s.close()

  # Esta forma de hacer la conexion, el metodo devuelve un valor, si el puerto esta cerrado devolvera un codigo de estado mayor a 0
  # if s.connect_ex((host, port)):
  #   print(colored(f"\n[!] El puerto {port} está cerrado...", "red"))
  # else:
  #   print(colored(f"\n[+] El puerto {port} está abierto...", "green"))

def main():
  for port in range(1, 1000):
    s = create_socket()
    port_scanner(port, s)

if __name__ == '__main__':
  main()
