#!/bin/bash

cd /root

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Essentials
apt-get install -y wget vim python-software-properties software-properties-common sudo net-tools inetutils-ping

# Setup Supervisor
apt-get install -y wget python-setuptools
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

# Setup PostgreSQL
useradd -b / -s /bin/bash postgres # Do it before install so we get uid 1000
add-apt-repository ppa:pitti/postgresql
apt-get update
apt-get -y install postgresql-9.2 postgresql-client-9.2 postgresql-contrib-9.2

# Configure PostgreSQL
sudo -u postgres psql -c "CREATE ROLE docker PASSWORD 'docker' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
service stop postgres

mkdir -p /postgres
mv /var/lib/postgresql/9.2/main /postgres/data
mv /etc/postgresql/9.2/main/postgresql.conf /postgres/data

echo "host    all             all             0.0.0.0/0               md5" >> /etc/postgresql/9.2/main/pg_hba.conf
sed -i -e "s,'/var/lib/postgresql/9.2/main','/postgres/data',g" /postgres/data/postgresql.conf
sed -i -e "s,#listen_addresses = 'localhost',listen_addresses='*',g" /postgres/data/postgresql.conf