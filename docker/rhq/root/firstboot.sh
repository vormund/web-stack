#!/bin/bash

export RHQ_SERVER_JAVA_EXE_FILE_PATH=/usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java

psql -h postgres.webstack.com -U docker -d postgres -c "CREATE ROLE rhqadmin PASSWORD 'rhqadmin' LOGIN;"
psql -h postgres.webstack.com -U docker -d postgres -c "CREATE DATABASE rhq WITH OWNER = rhqadmin ENCODING = 'SQL_ASCII' TABLESPACE = pg_default LC_COLLATE = 'C' LC_CTYPE = 'C' CONNECTION LIMIT = -1;"
cd /opt/rhq
bash bin/rhqctl install 