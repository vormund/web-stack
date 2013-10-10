#!/bin/bash
#title           :jboss-install.sh
#description     :The script to install JBoss AS 7.x
#author          :Dmitriy Sukharev
#date            :20130106
#usage           :/bin/bash jboss-install.sh

JBOSS_AS_FILENAME=jboss-as-7.1.1.Final
JBOSS_AS_ARCHIVE_NAME=$JBOSS_AS_FILENAME.tar.gz 
JBOSS_AS_DOWNLOAD_ADDRESS=http://download.jboss.org/jbossas/7.1/$JBOSS_AS_FILENAME/$JBOSS_AS_ARCHIVE_NAME

INSTALL_DIR=/opt
JBOSS_AS_FULL_DIR=$INSTALL_DIR/$JBOSS_AS_FILENAME
JBOSS_AS_DIR=$INSTALL_DIR/jboss-as

JBOSS_AS_USER="jboss-as"
JBOSS_AS_SERVICE="jboss-as"

JBOSS_AS_STARTUP_TIMEOUT=240

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Cleaning up..."
rm "$JBOSS_AS_ARCHIVE_NAME"
rm "$JBOSS_AS_DIR"
rm -r "$JBOSS_AS_FULL_DIR"
rm -r "/var/run/$JBOSS_AS_SERVICE/"
rm /etc/init.d/$JBOSS_AS_SERVICE

echo "Installation..."
wget $JBOSS_AS_DOWNLOAD_ADDRESS
mkdir $JBOSS_AS_FULL_DIR
tar -xzf $JBOSS_AS_ARCHIVE_NAME -C $INSTALL_DIR
ln -s $JBOSS_AS_FULL_DIR/ $JBOSS_AS_DIR
useradd -s /bin/bash $JBOSS_AS_USER
chown -R $JBOSS_AS_USER:$JBOSS_AS_USER $JBOSS_AS_DIR
chown -R $JBOSS_AS_USER:$JBOSS_AS_USER $JBOSS_AS_DIR/
rm $JBOSS_AS_ARCHIVE_NAME

echo "Registrating JBoss as service..."
mv /docker/functions /etc/init.d
#sed -e 's,${JBOSS_AS_USER},'$JBOSS_AS_USER',g; s,${JBOSS_AS_FILENAME},'$JBOSS_AS_FILENAME',g; s,${JBOSS_AS_SERVICE},'$JBOSS_AS_SERVICE',g; s,${JBOSS_AS_DIR},'$JBOSS_AS_DIR',g' $SCRIPT_DIR/jboss-as.template > /etc/init.d/$JBOSS_AS_SERVICE
#chmod 755 /etc/init.d/$JBOSS_AS_SERVICE

echo "Configurating..."
sed -i -e 's,/bin/sh,/bin/bash,g' $JBOSS_AS_DIR/bin/init.d/jboss-as-standalone.sh
#sed -i -e 's,. /etc/init.d/functions,. /lib/lsb/init-functions,g' $JBOSS_AS_DIR/bin/init.d/jboss-as-standalone.sh
sed -i -e 's,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000"/>,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000" deployment-timeout="'$JBOSS_AS_STARTUP_TIMEOUT'"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<virtual-server name="default-host" enable-welcome-root="true">,<virtual-server name="default-host" enable-welcome-root="false">,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
sed -i -e 's,<inet-address value="${jboss.bind.address:127.0.0.1}"/>,<any-address/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="ajp" port="8009"/>,<socket-binding name="ajp" port="28009"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="http" port="8080"/>,<socket-binding name="http" port="28080"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="https" port="8443"/>,<socket-binding name="https" port="28443"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml
#sed -i -e 's,<socket-binding name="osgi-http" interface="management" port="8090"/>,<socket-binding name="osgi-http" interface="management" port="28090"/>,g' $JBOSS_AS_DIR/standalone/configuration/standalone.xml

echo "Done."
