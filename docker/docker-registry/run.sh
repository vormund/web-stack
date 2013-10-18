#!/bin/bash
# Connect together all the docker containers

docker run -d -p 2203:22 docker-registry
