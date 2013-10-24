#!/bin/bash
# Connect together all the docker containers

#docker run -d -p 2202:22 -p 5432:5432 postgres

docker run -d -dns 172.17.42.1 -dns 8.8.8.8 -dns 8.8.4.4 -p 2202:22 -p 5432:5432 postgres
