### PostgreSQL
FROM    ubuntu:12.04

ADD     root/ /root/
RUN     /bin/bash /root/build.sh

EXPOSE  22 5432

CMD     ["/bin/bash", "/root/bootstrap.sh"]
