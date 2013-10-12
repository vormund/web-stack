### Apache
FROM    ubuntu:12.04

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN apt-get update

# Essentials
RUN apt-get install -y -q curl git vim aptitude wget openssh-server

# Setup Apache
RUN apt-get -y install libapache2-mod-jk

EXPOSE 22
EXPOSE 80
EXPOSE 443

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]

### Extra

# Setup Webmin
#RUN wget http://prdownloads.sourceforge.net/webadmin/webmin_1.660_all.deb
