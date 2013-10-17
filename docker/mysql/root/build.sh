#!/bin/bash

cd /root

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Supervisor
apt-get install -y wget supervisor
cp supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup SSH Server
apt-get install -y openssh-server
mkdir -p /var/run/sshd
mkdir -p /root/.ssh
cp id_rsa.pub .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chown root:root -R /root
echo 'AuthorizedKeysFile /root/.ssh/authorized_keys' >> /etc/ssh/sshd_config
echo 'PermitRootLogin without-password' >> /etc/ssh/sshd_config
