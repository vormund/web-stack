#!/bin/bash
# Connect together all the docker containers

docker run -d -p 2202:22 -p 3306:3306 mysql
