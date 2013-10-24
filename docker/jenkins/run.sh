#!/bin/bash
# Connect together all the docker containers

docker run -d -p 2204:22 -dns 172.17.42.1 -dns 8.8.8.8 -dns 8.8.4.4 jenkins