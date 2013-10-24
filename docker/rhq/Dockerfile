### Jenkins
FROM    ubuntu:12.04

ADD     root/ /root/
RUN     /bin/bash /root/build.sh

EXPOSE  22 8080
CMD     ["/bin/bash", "/root/bootstrap.sh"]
