#!/bin/bash

export JENKINS_HOME=/jenkins
chown jenkins /jenkins

/usr/local/bin/supervisord -c /etc/supervisord.conf
