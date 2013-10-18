#!/bin/bash

cd /root

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Essentials
apt-get install -y wget vim python-setuptools

# Setup Supervisor
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

# http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
# Setup Oracle Java
apt-get install -y python-software-properties
add-apt-repository -y ppa:webupd8team/java
apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
apt-get install -y oracle-java7-installer oracle-java7-set-default

# Setup JBoss WildFly
INSTALL_DIR=/opt
WILDFLY_VERSION=8.0.0.Beta1
WILDFLY_ARCHIVE_NAME=wildfly-$WILDFLY_VERSION.tar.gz 
WILDFLY_DOWNLOAD_ADDRESS=http://download.jboss.org/wildfly/$WILDFLY_VERSION/$WILDFLY_ARCHIVE_NAME
WILDFLY_FULL_DIR=$INSTALL_DIR/wildfly-$WILDFLY_VERSION
WILDFLY_DIR=$INSTALL_DIR/wildfly
WILDFLY_USER="wildfly"
WILDFLY_STARTUP_TIMEOUT=240

echo "Installation..."
wget $WILDFLY_DOWNLOAD_ADDRESS
mkdir $WILDFLY_FULL_DIR
tar -xzf $WILDFLY_ARCHIVE_NAME -C $INSTALL_DIR
ln -s $WILDFLY_FULL_DIR/ $WILDFLY_DIR
useradd -s /bin/bash $WILDFLY_USER
chown -R $WILDFLY_USER:$WILDFLY_USER $WILDFLY_DIR
chown -R $WILDFLY_USER:$WILDFLY_USER $WILDFLY_DIR/
rm $WILDFLY_ARCHIVE_NAME

echo "Configurating..."
sed -i -e 's,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000"/>,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000" deployment-timeout="'$WILDFLY_STARTUP_TIMEOUT'"/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<virtual-server name="default-host" enable-welcome-root="true">,<virtual-server name="default-host" enable-welcome-root="false">,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<inet-address value="${jboss.bind.address:127.0.0.1}"/>,<any-address/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="ajp" port="8009"/>,<socket-binding name="ajp" port="28009"/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="http" port="8080"/>,<socket-binding name="http" port="28080"/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="https" port="8443"/>,<socket-binding name="https" port="28443"/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="osgi-http" interface="management" port="8090"/>,<socket-binding name="osgi-http" interface="management" port="28090"/>,g' $WILDFLY_DIR/standalone/configuration/standalone.xml

echo "Done."
