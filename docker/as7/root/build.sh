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

# http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
# Setup Oracle Java
apt-get install -y python-software-properties
add-apt-repository -y ppa:webupd8team/java
apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
apt-get install -y oracle-java7-installer oracle-java7-set-default

# Setup JBoss Application Server 7
JBOSS_AS_FILENAME=jboss-as-7.1.1.Final
JBOSS_AS_ARCHIVE_NAME=$JBOSS_AS_FILENAME.tar.gz 
JBOSS_AS_DOWNLOAD_ADDRESS=http://download.jboss.org/jbossas/7.1/$JBOSS_AS_FILENAME/$JBOSS_AS_ARCHIVE_NAME
JBOSS_AS_FULL_DIR=$INSTALL_DIR/$JBOSS_AS_FILENAME
JBOSS_AS_DIR=$INSTALL_DIR/jboss-as
JBOSS_AS_USER="jboss"
JBOSS_AS_STARTUP_TIMEOUT=240

INSTALL_DIR=/opt
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installation..."
wget $JBOSS_AS_DOWNLOAD_ADDRESS
mkdir $JBOSS_AS_FULL_DIR
tar -xzf $JBOSS_AS_ARCHIVE_NAME -C $INSTALL_DIR
ln -s $JBOSS_AS_FULL_DIR/ $JBOSS_AS_DIR
useradd -s /bin/bash $JBOSS_AS_USER
chown -R $JBOSS_AS_USER:$JBOSS_AS_USER $JBOSS_AS_DIR
chown -R $JBOSS_AS_USER:$JBOSS_AS_USER $JBOSS_AS_DIR/
rm $JBOSS_AS_ARCHIVE_NAME

echo "Configurating..."
sed -i -e 's,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000"/>,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000" deployment-timeout="'$JBOSS_AS_STARTUP_TIMEOUT'"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<virtual-server name="default-host" enable-welcome-root="true">,<virtual-server name="default-host" enable-welcome-root="false">,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<inet-address value="${jboss.bind.address:127.0.0.1}"/>,<any-address/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="ajp" port="8009"/>,<socket-binding name="ajp" port="28009"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="http" port="8080"/>,<socket-binding name="http" port="28080"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="https" port="8443"/>,<socket-binding name="https" port="28443"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="osgi-http" interface="management" port="8090"/>,<socket-binding name="osgi-http" interface="management" port="28090"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml

echo "Done."
