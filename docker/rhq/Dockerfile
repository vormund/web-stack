### Jenkins
FROM    ubuntu:12.04

ADD     root/ /root/
RUN     /bin/bash /root/build.sh
ADD     opt/rhq/bin/rhq-server.properties /opt/rhq/bin/rhq-server.properties

EXPOSE  22 8080
CMD     ["/bin/bash", "/root/bootstrap.sh"]
