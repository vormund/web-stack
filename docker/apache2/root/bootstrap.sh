#!/bin/bash

export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
export APACHE_LOG_DIR=/var/log/apache2
export APACHE_RUN_DIR=/var/run/apache2$SUFFIX
export APACHE_PID_FILE=/var/run/apache2$SUFFIX.pid
export APACHE_LOCK_DIR=/var/lock/apache2$SUFFIX

/usr/local/bin/supervisord -c /etc/supervisord.conf
