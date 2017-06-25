#!/usr/bin/env python

import json
import math
import socket
import struct
import zlib
import sys
import pickle
#from termcolor import colored

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('',6454))

dmxeq = {}

import serial
if __name__ == "__main__":
    ser = serial.Serial('COM3', 9600)
def chanval(chan, val):
	ser.write('%dc %dw' % (chan, val))
	sys.stdout.write("\r%d -> %d  \t [master@%f]" % (chan,val,0))
	sys.stdout.flush()

print "Hello"

dmxstates = []
dmxinit = False

for i in xrange(1,514):
	dmxstates.append(-1)

def lhex(h):
    return ':'.join(x.encode('hex') for x in h)
def setDmxValue(i, val):
	if dmxstates[i] == -1:
		dmxstates[i] = val
	if dmxstates[i] != val:
		dmxstates[i] = val
		# DMX UPDATE!!! WOW!!!
		print "Setting channel %d to %d" % (i,ord(val))
		chanval(i,ord(val))
	
while True:
  data = sock.recv(10240)
  
  if len(data) < 20:
	continue

  if data[0:7] != "Art-Net" or data[7] != "\0":
	# artnet package
	continue
  
  if ord(data[8]) != 0x00 or ord(data[9]) != 0x50:
	# OpDmx
	continue
  
  protverhi = ord(data[10])
  protverlo = ord(data[11])
  sequence  = ord(data[12])
  physical  = ord(data[13])
  subuni    = ord(data[14])
  net       = ord(data[15])
  lengthhi  = ord(data[16])
  length    = ord(data[17])
  dmx       = data[18:]
  
  for i in xrange(0,510):
	setDmxValue(i+1,dmx[i])
	
  #print data[0:4]
  
  #print lhex(dmx)
