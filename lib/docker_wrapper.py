from util import run
import os, shutil

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

    def ps(self):
        headers = ['Image', 'Id', 'Status', 'Command']
        print format_as_table(self.client.containers(), headers, headers)

    def run(self, image):
        containerInfo = self.client.create_container(image, None)
        self.client.start(containerInfo['Id'])
        print "Image [%s] started, container=%s." % (image, containerInfo['Id'])

    def kill(self, containerId):
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

    def removeImage(self, imageId):
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
            