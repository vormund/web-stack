#!/bin/bash

export JAVA=/usr/lib/jvm/java-7-oracle/bin/java 
export JAVA_OPTS="-server -Xms64m -Xmx512m -XX:MaxPermSize=256m -XX:+UseCompressedOops"
export WILDFLY_HOME=/opt/wildfly
export WILDFLY_LOG_DIR=/var/log/wildfly
export WILDFLY_CONFIG_DIR=$WILDFLY_HOME/standalone/configuration
export WILDFLY_MODULE_DIR=$WILDFLY_HOME/modules
export WILDFLY_BASE_DIR=$WILDFLY_HOME/standalone

/usr/local/bin/supervisord -c /etc/supervisord.conf
