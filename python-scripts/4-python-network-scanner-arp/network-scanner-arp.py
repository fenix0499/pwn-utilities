#!/usr/bin/env python3

import scapy.all as scapy
import argparse

def getArguments():
  parser = argparse.ArgumentParser(description="ARP Scanner...")
  parser.add_argument("-t", "--target", required=True, dest="target", help="Host / IP Range to Scan")

  args = parser.parse_args()

  return args.target

def scan(ip):
  # scapy.arping(ip)

  arpPacket = scapy.ARP(pdst=ip)
  broadcastPacket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

  arpPacket = broadcastPacket/arpPacket

  [answered, unanswered] = scapy.srp(arpPacket, timeout=1, verbose=False)

  response = answered.summary()

  if response:
    print(response)

def main():
  target = getArguments()
  scan(target)

if __name__ == '__main__':
  main()
