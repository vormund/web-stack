# This file describes the environment needed for web-stack
#
# Usage:
#
#
#

FROM	ubuntu:12.04

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN	apt-get update

# Essentials
RUN	apt-get install -y -q curl git vim aptitude wget openssh-server unzip

# http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
# Setup Oracle Java
RUN apt-get install -y python-software-properties
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java7-installer oracle-java7-set-default

# Setup MySQL
#RUN debconf-set-selections \<\<\< 'mysql-server-<version> mysql-server/root_password password ""'
#RUN debconf-set-selections \<\<\< 'mysql-server-<version> mysql-server/root_password_again password ""'
RUN apt-get -y install mysql-server

# Setup Apache
RUN apt-get -y install libapache2-mod-jk

# Setup Webmin
#RUN wget http://prdownloads.sourceforge.net/webadmin/webmin_1.660_all.deb

# Add users
ADD docker/ /docker
RUN /bin/bash /docker/jboss-install.sh
RUN /bin/bash /docker/startup.sh

EXPOSE 80
EXPOSE 443
EXPOSE 22
EXPOSE 9000
