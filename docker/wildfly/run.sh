#!/bin/bash
# Connect together all the docker containers

docker run -i -t -d -p 2201:22 -p 9001:9001 -p 8009:8009 -v /vagrant/docker/wildfly/opt/wildfly:/wtf wildfly
