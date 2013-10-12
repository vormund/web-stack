#!/bin/sh
### BEGIN INIT INFO
# Provides:          ${JBOSS_AS_SERVICE}
# Required-Start:    $local_fs $remote_fs $network $syslog
# Required-Stop:     $local_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start/Stop ${JBOSS_AS_FILENAME}
### END INIT INFO

JBOSS_USER=${JBOSS_AS_USER}
JBOSS_DIR=${JBOSS_AS_DIR}

case "$1" in
start)
echo "Starting ${JBOSS_AS_FILENAME}..."
start-stop-daemon --start --background --chuid $JBOSS_USER --exec $JBOSS_DIR/bin/standalone.sh
exit $?
;;
stop)
echo "Stopping ${JBOSS_AS_FILENAME}..."

start-stop-daemon --start --quiet --background --chuid $JBOSS_USER --exec $JBOSS_DIR/bin/jboss-cli.sh -- --connect command=:shutdown
exit $?
;;
log)
echo "Showing server.log..."
tail -500f $JBOSS_DIR/standalone/log/server.log
;;
*)
echo "Usage: /etc/init.d/jboss-as {start|stop}"
exit 1
;;
esac
exit 0