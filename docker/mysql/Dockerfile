### MySQL
FROM    ubuntu:12.04

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN apt-get update

# Essentials
RUN apt-get install -y -q curl git vim aptitude wget openssh-server

# Setup MySQL
#RUN debconf-set-selections \<\<\< 'mysql-server-<version> mysql-server/root_password password ""'
#RUN debconf-set-selections \<\<\< 'mysql-server-<version> mysql-server/root_password_again password ""'
RUN apt-get -y install mysql-server

EXPOSE 22
EXPOSE 3306

