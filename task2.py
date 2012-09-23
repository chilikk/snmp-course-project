#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time, sys, pickle
from my.debug import debugmsg, printmsg, printerrmsg

def poll(routerid):
	return routers[routerid].pollLinksLoad()

pollinterval = 5
num_samples = 200

if __name__=='__main__':
	try:
		routers = pickle.load(open('routers.dat','r'))
		routers = [router.restoresnmpiface() for router in routers]
	except Exception:
		from my.debug import printerrmsg
		printerrmsg('routers.dat not found! run main.py first')
		import sys
		sys.exit()
	stats = NetStatistics()
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, threshold, alarm = stats.getNetState()
		if netstate != "start":
			if threshold:
				printmsg("\t%d\t\t%d\t%s" % (netstate, threshold, alarm))
			else:
				printmsg("\t%d" % netstate)
		else:
			printerrmsg("start polling\ntime\t\tnetwork load\talarm threshold")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
