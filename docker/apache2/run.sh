#!/bin/bash
# Connect together all the docker containers

docker run -d -i -t -dns 172.17.42.1 -dns 8.8.8.8 -dns 8.8.4.4 -p 2200:22 -v /vagrant/docker/apache2/var/www:/var/www apache2
