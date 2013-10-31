from util import run
import os, shutil
from dict2table import *

class DockerWrapper(object):
    """ Small wrapper around Docker """

    baseDir = '/vagrant/docker'
    client = None

    def __init__(self, client=None):
        self.client = client

    def images(self):
        #print self.client.images()
        headers = ['Repository', 'Tag', 'Id']
        print format_as_table(self.client.images(), headers, headers)

    def build(self, docker):

        if not os.path.isdir('docker/%s' % docker):
            return

        # Copy our public key to docker directory to propegate inside our containers
        shutil.copy(os.path.expanduser("~") + '/.ssh/id_rsa.pub', 'docker/%s/root' % docker)

        run('vagrant ssh --command "cd %s/%s && docker build -t=\"%s\" ."' % (self.baseDir, docker, docker), cwd="docker/%s" % docker)

    def listContainers(self):
        headers = ['Image', 'Id', 'Status', 'Command']
        print format_as_table(self.client.containers(), headers, headers)

    def runByName(self, name):
        containerInfo = self.client.create_container(name, None)
        self.startContainerById(containerInfo['Id'])

        return containerInfo['Id']

    def runByConfiguration(self, configuration):
        
        #c.create_container(image, command=None, hostname=None, user=None, 
        #detach=False,stdin_open=False, tty=False, mem_limit=0, ports=None, environment=None,
        #dns=None,volumes=None, volumes_from=None, privileged=False)

        containerInfo = self.client.create_container(configuration.getName(), None, dns=configuration.getDns(), volumes=configuration.getVolumes())
        self.startContainerById(containerInfo['Id'])

        return containerInfo['Id']

    def startContainerById(self, containerId):

        self.client.start(containerId)

        name = self.client.inspect_container(containerId)['Config']['Image']
        print "Image [%s] started, container=%s." % (name, containerId)


    def killContainerById(self, containerId):
        if containerId == 'all':
            containers = self.client.containers()     
        else:
            containers = [{'Id':containerId}]

        for containerInfo in containers:
            try:
                self.client.kill(containerInfo['Id'])
                print "Container [%s] killed." % containerInfo['Id']
            except:
                print "Failed killing [%s] container." % containerInfo['Id']

    def removeImageById(self, imageId):
        if imageId == 'all':
            images = self.client.images()     
        else:
            images = [{'Id':imageId}]

        for imageInfo in images:
            try:
                self.client.remove_image(imageInfo['Id'])
                print "Image [%s] removed." % imageInfo['Id']
            except:
                print "Failed removing [%s] image." % imageInfo['Id'] 

        
            