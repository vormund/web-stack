#!/bin/bash
# Connect together all the docker containers

docker run -d -i -t -p 2200:22 -p 9000:9001 -p 80:80 -p 443:443 -v /vagrant/docker/apache2/var/www:/var/www apache2
