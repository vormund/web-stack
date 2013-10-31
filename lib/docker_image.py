
class DockerImage(object):

    image = None
    hash = None
    dns = None
    volumes = None
    instances = None

    def __init__(self, image=None, hash=None, dns=[], volumes={}, instances=1):
        self.image = image
        self.hash = hash
        self.dns = dns
        self.volumes = volumes
        self.instances = instances

    def getName(self):
        return self.image

    def getDns(self):
        return self.dns

    def getVolumes(self):
        return self.volumes

    def getHash(self):
        return self.hash

    def setHash(self, hash):
        self.hash = hash

    def getInstances(self):
        return self.instances