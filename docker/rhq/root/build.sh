#!/bin/bash

cd /root

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Essentials
apt-get install -y wget vim zip net-tools inetutils-ping aptitude

# Setup Supervisor
apt-get install -y python-setuptools
easy_install supervisor
mv /root/supervisord.conf /etc

# Setup SSH Server
apt-get install -y openssh-server
mkdir -p /var/run/sshd
mkdir -p /root/.ssh
mv id_rsa.pub /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
chown root:root -R /root
echo 'AuthorizedKeysFile  /root/.ssh/authorized_keys' >> /etc/ssh/sshd_config
echo 'PermitRootLogin  without-password' >> /etc/ssh/sshd_config

# Setup OpenJDK - Oracle JDK has problems
apt-get install -y openjdk-7-jre-headless

# Download and move RHQ
wget http://downloads.sourceforge.net/project/rhq/rhq/rhq-4.9.0/rhq-server-4.9.0.zip
unzip rhq-server-4.9.0.zip
mv rhq-server-4.9.0 /opt/rhq

# Download Postgres client
add-apt-repository ppa:pitti/postgresql
apt-get update
apt-get install -y postgresql-client

# Setup Postgres PGPASS file
echo 'postgres.webstack.com:5432:*:docker:docker' > /root/.pgpass
chmod 600 /root/.pgpass
