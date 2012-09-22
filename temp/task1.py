#!/usr/bin/python

from my.snmpiface import SnmpIface

def list_union(a,b):
	for item in b:
		if not item in a:
			a.append(item)
	return a

def getRouterInfo(host):
	router = SnmpIface(host = host)
	routername = router.getObject(router.oid_sysName)
	num_ifs = int(router.getObject(router.oid_ifNumber))
	interfaces = router.getBulk(router.oid_ifDescr,num_ifs).values()
	neighbours = router.getSubtree(router.oid_ipRouteNextHop).values()
	ips = router.getSubtree(router.oid_ipAdEntAddr).values()
	neighbours = list(set(neighbours).difference(ips))
	return { 'name':routername, 'interfaces':interfaces, 'neighbours': neighbours, 'ips':ips }

def printRouterInfo(info):
	print "Router %s:" % info['name']
	print "        IP addresses: "
	for item in info['ips']:
		print "                %s" % item
	print "        Interfaces: "
	for item in info['interfaces']:
		print "                %s" % item
	print "        Link-layer neighbours: "
	for item in info['neighbours']:
		print "                %s" % item
	print

if __name__=='__main__':
	routers = ['192.168.1.10']
	visited = []
	for router in routers:
		if router in visited:
			continue
		info = getRouterInfo(router)
		printRouterInfo(info)
		routers = list_union(routers,info['neighbours'])
		visited += info['ips']