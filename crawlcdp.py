#!/usr/bin/env python
# This script will recursively crawl a Cisco network using CDP to get all 
# the device names.
import sys
from snimpy.manager import (load,Manager)
import snimpy
import snimpy.mib
import pdb
import socket

snimpy.mib.path("netdisco-mibs/rfc:netdisco-mibs/cisco")

load('SNMPv2-MIB')
load('CISCO-CDP-MIB')

device_names = {}

def crawl(host, ipaddr):
	try:
		m=snimpy.manager.Manager(host=host, community="public", version=2)
	except:
		print host + " not resolvable, trying IP address " + ipaddr
		m=snimpy.manager.Manager(host=ipaddr, community="public", version=2)

	try:
		device_ids = []
		for idx in m.cdpCacheDeviceId:
			device_ids.append(idx)

		for i in device_ids:
			name = m.cdpCacheDeviceId[i[0],i[1]]
			ipaddr = m.cdpCacheAddress[i[0],i[1]]
			ipaddr = socket.inet_ntoa(ipaddr)
			#pdb.set_trace()
			if not name in device_names:
				device_names[name] = 1
				print name
				crawl(name, ipaddr)
	except:
		print "Could not communicate with " + host + ", bad credentials?"

if len(sys.argv) != 2:
	print "Usage: crawlcdp HOST"
	sys.exit(0)
crawl(sys.argv[1], 0)
