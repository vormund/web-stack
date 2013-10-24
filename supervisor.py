#!/usr/bin/python

import xmlrpclib
import httplib
#print server.supervisor.getState()
#print server.system.listMethods()
#print server.supervisor.readLog(0,0)
#print server.supervisor.getAllProcessInfo()

titles = { 'docker': 'DOCKER', 'description': 'DESCRIPTION', 'pid': 'PID', 'name': 'NAME', 'state': 'STATE' }

print "%(docker)8s | %(pid)10s | %(name)-20s | %(description)-20s" % titles
print "---------------------------------------------------------------------"

for i in range(0,3):
    
    try :
        server = xmlrpclib.Server('http://localhost:%d/RPC2' % (9000+i))
        for process in server.supervisor.getAllProcessInfo():
            process['docker'] = i
            print "%(docker)8d | %(pid)10s | %(name)-20s | %(description)-20s" % process
    except httplib.BadStatusLine:
        pass


