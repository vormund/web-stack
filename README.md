## web-stack

Includes the following technologies, playing together...

### Underneath
  - [x] [Vagrant](http://www.vagrantup.com/) + [Docker](https://github.com/dotcloud/docker)

### Frontend
  - [ ] [NPM](https://npmjs.org/)
  - [ ] [Bower](http://bower.io/)
  - [ ] [Grunt](http://gruntjs.com/)
  - [ ] [AngularJS](http://angularjs.org/)
  - [ ] [RequireJS](http://requirejs.org/)
  - [ ] [Twitter Bootstrap3](http://getbootstrap.com/)
  - [ ] [Jasmine](http://pivotal.github.io/jasmine/) + [Karma](http://karma-runner.github.io)

### Backend - Java
  - [ ] [Apache 2](http://www.apache.org/) + [mod-jk](http://tomcat.apache.org/connectors-doc/)
  - [ ] [Application Server 7](https://www.jboss.org/jbossas)
  - [ ] [Maven](http://maven.apache.org/)
  - [ ] [Hibernate](http://www.hibernate.org/)
  - [ ] [MySQL](http://www.mysql.com/)
  - [ ] [RestEasy](http://www.jboss.org/resteasy) + [Skeleton Key (OAuth2)](http://docs.jboss.org/resteasy/docs/3.0-beta-2/userguide/html/oauth2.html)
  - [ ] [Arquillian](http://arquillian.org/)

### Extra
  - [ ] [Webmin](http://www.webmin.com/)


Getting Going
----------------

1. Install the [lastest version of VirtualBox](https://www.virtualbox.org/)
2. Install the [lastest version of Vagrant](http://downloads.vagrantup.com/)
3. Vagrant setup

    Checkout this github repo, open a terminal to it, type:

        $ vagrant up 

    Takes a few minutues for VirtualBox tools to become available, required for mounting /vagrant

        $ vagrant reload

4. Docker setup

    Enter Vagrant box

        $ vagrant ssh
        $ cd /vagrant
        $ docker build -t="webstack" .

    After this completes you should have docker container complete with Apache, AS7, MySQL services running

5. Coming Soon..
