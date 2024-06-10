#!/usr/bin/env python3

import string
import sys

if len(sys.argv) != 2:
  print(f"\n[!] Uso: python3 {sys.argv[0]} <i_value>\n")
  sys.exit(1)

index = int(sys.argv[1])

for character in string.ascii_uppercase + string.digits:
  value = (ord(character)<<index+1)%256^ord(character)
  print(f"{character}: {value}")
  
