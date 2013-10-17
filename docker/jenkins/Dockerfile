### Jenkins
FROM    ubuntu:12.04

ADD root/ /root/
RUN /bin/bash /root/build.sh

EXPOSE 8080 22
CMD ["/bin/bash", "/root/bootstrap.sh"]
VOLUME ["/jenkins"]
