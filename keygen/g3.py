#!/usr/bin/env python3

from itertools import product
import string

p1 = product(string.ascii_uppercase, repeat=2)
p1 = [ "".join(i) for i in p1 ]

uniques = {}

for couple in p1:
  for index in range(0,10):
    cadena = f"XP{couple}{index}"
    value = sum(bytearray(cadena.encode()))
    # print(f"{cadena}: {value}")

    uniques[value] = cadena

print("\n".join(uniques.values()))
