### Apache
FROM    ubuntu:12.04

ADD root/ /root/
RUN /bin/bash /root/build.sh

EXPOSE 22
EXPOSE 80
EXPOSE 443

CMD ["/bin/bash", "/root/bootstrap.sh"]
