#!/bin/bash

cd /root

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Supervisor
apt-get install -y wget supervisor
cp /root/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup SSH Server
apt-get install -y openssh-server
mkdir -p /var/run/sshd
mkdir -p /root/.ssh
cp id_rsa.pub .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chown root:root -R /root
echo 'AuthorizedKeysFile /root/.ssh/authorized_keys' >> /etc/ssh/sshd_config
echo 'PermitRootLogin without-password' >> /etc/ssh/sshd_config

# Add Jenkins user to get UID 1000, so we don't have permission problems with volumes
useradd -s /bin/bash jenkins

# Setup Jenkins
wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
/bin/bash -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
apt-get update
apt-get install -y net-tools jenkins

