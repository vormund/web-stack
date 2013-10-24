#!/bin/bash
# Connect together all the docker containers

docker run -d -dns 172.17.42.1 -dns 8.8.8.8 -dns 8.8.4.4 -p 2202:22 -p 3306:3306 mysql
