#!/bin/bash

export JAVA=
export JAVA_OPTS='"-Dprogram.name=JBossTools: JBoss 7.1 Runtime Server" -server -Xms64m -Xmx512m -XX:MaxPermSize=256m -Dorg.jboss.resolver.warning=true -Djava.net.preferIPv4Stack=true -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000 -Djboss.modules.system.pkgs=org.jboss.byteman -Djava.awt.headless=true "-Dorg.jboss.boot.log.file=/Users/josh/servers/jboss-as7/standalone/log/boot.log" "-Dlogging.configuration=file:/Users/josh/servers/jboss-as7/standalone/configuration/logging.properties" "-Djboss.home.dir=/Users/josh/servers/jboss-as7"'
export JBOSS_LOG_DIR=
export JBOSS_CONFIG_DIR=
export JBOSS_MODULEPATH=

/usr/bin/supervisord