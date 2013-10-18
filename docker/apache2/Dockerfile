### Apache
FROM    ubuntu:12.04

ADD     root/ /root/
RUN     /bin/bash /root/build.sh

EXPOSE  22 80 443

CMD     ["/bin/bash", "/root/bootstrap.sh"]
VOLUME  ["/etc/apache2", "/var/www"]