### MySQL
FROM    ubuntu:12.04

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN apt-get update

# Setup Supervisor
RUN apt-get install -y wget supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD bootstrap.sh /root/bootstrap.sh

# Setup SSH Server
RUN apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh
ADD id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN chown root:root /root/.ssh/authorized_keys
RUN echo 'AuthorizedKeysFile   /root/.ssh/authorized_keys' > /etc/ssh/sshd_config
RUN echo 'PermitRootLogin without-password' > /etc/ssh/sshd_config

# Setup Jenkins
RUN wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
RUN /bin/bash -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt-get update
RUN apt-get install -y net-tools jenkins
ENV JENKINS_HOME /jenkins


EXPOSE 8080 22
CMD ["/bin/bash", "/root/bootstrap.sh"]
VOLUME ["/jenkins"]
