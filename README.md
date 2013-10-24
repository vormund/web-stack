## web-stack

Includes the following technologies, playing together...

### Underneath
  - [✓] [Vagrant](http://www.vagrantup.com/) + [Docker](https://github.com/dotcloud/docker)

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
  - [ ] [WildFly](https://www.wildfly.org)
  - [ ] [Maven](http://maven.apache.org/)
  - [ ] [Hibernate](http://www.hibernate.org/)
  - [ ] [MySQL](http://www.mysql.com/) or [PostgreSQL](http://www.postgresql.org/)
  - [ ] [RestEasy](http://www.jboss.org/resteasy) + [Skeleton Key (OAuth2)](http://docs.jboss.org/resteasy/docs/3.0-beta-2/userguide/html/oauth2.html)
  - [ ] [Arquillian](http://arquillian.org/)

### Extra
  - [ ] [RHQ](http://www.jboss.org/rhq)
  - [ ] [Webmin](http://www.webmin.com/)


Getting Going
----------------

    Windows users can omit the 'sudo' in console commands below.

1. Download & install [lastest version of VirtualBox](https://www.virtualbox.org/)
2. Download & install [lastest version of Vagrant](http://downloads.vagrantup.com/)
3. Download & install Python 2.7 (Standard with OSX)
4. Download & Install [latest version of SetupTools](https://pypi.python.org/pypi/setuptools)
        
        $ sudo python setup.py install    
        $ sudo easy_install docker-py python-vagrant

5. Stack setup

        $ python webstack.py stack up

    This command will setup a Ubuntu flavored Vagrant box, install Docker, and setup docker containers for all of our services.

6. More to come soon!!