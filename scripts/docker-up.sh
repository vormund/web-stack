#!/bin/bash

# Build AS7 container
cd /vagrant/docker/as7
docker build -t="as7" .

# Build MySql cotnainer
cd /vagrant/docker/mysql
docker build -t="mysql" .

# Build Apache container
cd /vagrant/docker/apache
docker build -t="apache" .