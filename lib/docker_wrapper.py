from util import run
import os, shutil
from dict2table import *

class DockerWrapper(object):
    """ Small wrapper around Docker """

    baseDir = '/vagrant/docker'
    dockerClient = None

    def __init__(self, dockerClient=None):
        self.dockerClient = dockerClient

    def images(self):
        #print self.dockerClient.images()
        headers = ['Repository', 'Tag', 'Id']
        print format_as_table(self.dockerClient.images(), headers, headers)

    def build(self, docker):

        if not os.path.isdir('docker/%s' % docker):
            return

        # Copy our public key to docker directory to propegate inside our containers
        shutil.copy(os.path.expanduser("~") + '/.ssh/id_rsa.pub', 'docker/%s/root' % docker)

        run('vagrant ssh --command "cd %s/%s && docker build -t=\"%s\" ."' % (self.baseDir, docker, docker), cwd="docker/%s" % docker)

    def listContainers(self):
        headers = ['Image', 'Id', 'Status', 'Command']
        print format_as_table(self.dockerClient.containers(), headers, headers)

    def runByName(self, name):
        containerInfo = self.dockerClient.create_container(name, None)
        self.startContainerById(containerInfo['Id'])

        return containerInfo['Id']

    def runByConfiguration(self, configuration):
        
        #c.create_container(image, command=None, hostname=None, user=None, 
        #detach=False,stdin_open=False, tty=False, mem_limit=0, ports=None, environment=None,
        #dns=None,volumes=None, volumes_from=None, privileged=False)

        containerInfo = self.dockerClient.create_container(configuration.getName(), None, dns=configuration.getDns(), volumes=configuration.getVolumes())
        self.startContainerById(containerInfo['Id'])

        return containerInfo['Id']

    def startContainerById(self, containerId):

        self.dockerClient.start(containerId)

        name = self.dockerClient.inspect_container(containerId)['Config']['Image']
        print "Image [%s] started, container=%s." % (name, containerId)


    def killContainerById(self, containerId):
        if containerId == 'all':
            containers = self.dockerClient.containers()     
        else:
            containers = [{'Id':containerId}]

        for containerInfo in containers:
            try:
                self.dockerClient.kill(containerInfo['Id'])
                print "Container [%s] killed." % containerInfo['Id']
            except:
                print "Failed killing [%s] container." % containerInfo['Id']

    def removeImageById(self, imageId):
        if imageId == 'all':
            images = self.dockerClient.images()     
        else:
            images = [{'Id':imageId}]

        for imageInfo in images:
            try:
                self.dockerClient.remove_image(imageInfo['Id'])
                print "Image [%s] removed." % imageInfo['Id']
            except:
                print "Failed removing [%s] image." % imageInfo['Id'] 

        
            