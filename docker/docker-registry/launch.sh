#!/bin/bash

## The following environmental variables should exist prior to exection of this docker container
# SETTINGS_FLAVOR=prod
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# S3_BUCKET=
docker run -d samalba/docker-registry
