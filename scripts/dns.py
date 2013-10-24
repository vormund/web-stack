import json
import docker
import sys
import subprocess
import re

def run(cmd, returncode=False, echo=True, **kargs):
    """ Executes a shell command and prints out STDOUT / STDERROR, exits on failure by default """
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, **kargs)
    if echo:
        print "$ %s" % cmd
    
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    if returncode:
        return process.returncode
    else:
        if process.returncode != 0:
            print "Something went wrong! returncode=%s" % process.returncode
            sys.exit(1)

dockConfig = json.load(open('/vagrant/dock.json'))
client = docker.Client(base_url='http://127.0.0.1:5555', version="1.6")
dockName = sys.argv[1]
domainName = dockConfig['docks'][dockName]['domain']

activeContainers = []
for containerInfo in client.containers():
    inspectInfo = client.inspect_container(containerInfo['Id'])
    activeContainers.append({ 'name': containerInfo['Image'].split(':')[0] , 'ip': inspectInfo['NetworkSettings']['IPAddress'] })


content = open('/vagrant/scripts/dns.tpl').read()

# Compile list of A entries
aEntries = ''
for container in activeContainers:
    aEntries = aEntries + '%(name)s   IN  A   %(ip)s\n' % container

replace = {'hostname': dockConfig['docks'][dockName]['domain'], 'aEntries': aEntries}

f = open('/vagrant/temp','w')
f.write(content % replace)
f.close()

# Copy new zone file into bind directory, set ownership / privileges correctly
run('sudo cp /vagrant/temp /etc/bind/%s' % domainName)
run('sudo chown bind:bind /etc/bind/%s' % domainName)

# Check to see if we have the zone included
zoneFile = '/etc/bind/named.conf.default-zones';
zoneContents = open(zoneFile).read()

match = re.search(domainName, zoneContents, re.IGNORECASE)
if not match:
    zoneContents = zoneContents + 'zone "%s" { type master; file "/etc/bind/%s"; };\n' % (domainName, domainName)
    f = open('/vagrant/temp','w')
    f.write(zoneContents)
    f.close()
    run('sudo cp /vagrant/temp %s' % zoneFile)
    run('sudo chown bind:bind %s' % zoneFile)

run('sudo service bind9 reload')

