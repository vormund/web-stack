### Apache

echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
apt-get update

# Setup Supervisor
apt-get install -y wget supervisor
cp /root/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup SSH Server
apt-get install -y openssh-server
mkdir -p /var/run/sshd
mkdir -p /root/.ssh
ADD id_rsa.pub /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
chown root:root -R /root
echo 'AuthorizedKeysFile  /root/.ssh/authorized_keys' >> /etc/ssh/sshd_config
echo 'PermitRootLogin  without-password' >> /etc/ssh/sshd_config

# Setup Apache
apt-get -y install libapache2-mod-jk

