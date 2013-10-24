#!/bin/bash
# Connect together all the docker containers

# docker run -i -t -d -p 2204:22 -p 9004:9001 -p 8012:8009 \
# -v /vagrant/docker/wildfly/opt/wildfly:/wildfly -e=WILDFLY_BASE_DIR="/wildfly/standalone",WILDFLY_CONFIG_DIR="/wildfly/standalone/configuration" wildfly /bin/bash

# docker run -i -t -d -p 2204:22 -p 9001:9001 -p 8009:8009 \
#  -v /vagrant/docker/wildfly/opt/wildfly:/wildfly -e=WILDFLY_BASE_DIR="/wildfly/standalone" -e=WILDFLY_CONFIG_DIR="/wildfly/standalone/configuration" wildfly

docker run -i -t -d -dns 172.17.42.1 -dns 8.8.8.8 -dns 8.8.4.4 -p 2205:22 \
 -v /vagrant/docker/wildfly/opt/wildfly:/wildfly -e=WILDFLY_BASE_DIR="/wildfly/standalone" -e=WILDFLY_CONFIG_DIR="/wildfly/standalone/configuration" wildfly

# -v /vagrant/docker/wildfly/root:/root \
 
