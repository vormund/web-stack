# This file describes the environment needed for web-stack
#
# Usage:
#
#
#

### JBoss Application Server 7
FROM	ubuntu:12.04

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN apt-get update

# Essentials
RUN apt-get install -y -q curl git vim aptitude wget

# Setup SSH Server
RUN apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh
ADD id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN chown root:root /root/.ssh/authorized_keys
RUN echo 'AuthorizedKeysFile   /root/.ssh/authorized_keys' > /etc/ssh/sshd_config
RUN echo 'PermitRootLogin without-password' > /etc/ssh/sshd_config

# http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
# Setup Oracle Java
RUN apt-get install -y python-software-properties
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java7-installer oracle-java7-set-default

# Add users
ADD . /docker
RUN /bin/bash /docker/jboss-install.sh

EXPOSE 22

ENTRYPOINT ["/opt/jboss-as/bin/standalone.sh"]
#CMD ["-D", "FOREGROUND"]