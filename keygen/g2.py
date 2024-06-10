#!/usr/bin/env python3

from itertools import product
import string

p1 = product(string.ascii_uppercase + string.digits, repeat=3) #ACE
p1 = [ "".join(i) for i in p1 ]

p2 = product(string.ascii_uppercase + string.digits, repeat=2) # BD
p2 = [ "".join(i) for i in p2 ]

for triad in p1:
  for couple in p2:
    if sum(bytearray(triad.encode())) == sum(bytearray(couple.encode())):
      print(triad[0] + couple[0] + triad[1] + couple[1] + triad[2])
