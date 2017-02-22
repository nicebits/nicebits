#!/usr/bin/env python
# This script will recursively crawl a Cisco network using CDP to get all 
# the device names.
import sys
from snimpy.manager import (load,Manager)
import snimpy
import snimpy.mib

snimpy.mib.path("netdisco-mibs/rfc:netdisco-mibs/cisco")

load('SNMPv2-MIB')
load('CISCO-CDP-MIB')

device_names = {}

def crawl(host):
	m=snimpy.manager.Manager(host=host, community="public", version=2)

	device_ids = []
	for idx in m.cdpCacheDeviceId:
		device_ids.append(idx)

	for i in device_ids:
		name = m.cdpCacheDeviceId[i[0],i[1]]
		if not name in device_names:
			device_names[name] = 1
			crawl(name)

crawl(sys.argv[1])
for key in device_names:
	print key
