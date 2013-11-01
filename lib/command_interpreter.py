import os, sys, time
import vagrant

class CommandInterpreter(object):

    vagrant = None
    docker = None
    dockYard = None
    dns = None

    def __init__(self, vagrant=None, docker=None, dockyard=None, dns=None):
        self.vagrant = vagrant
        self.docker = docker
        self.dockyard = dockyard
        self.dns = dns

    def execute(self, args):
        """ Execute command via reflection """
        method = getattr(self, args.operation)
        method(args)        

class StackCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Stack related tasks """

    def up(self, args):
        
        # Bring Vagrant UP
        v = vagrant.Vagrant()
        if not v.status()['default'] == 'running':
            self.vagrant.up()

        # Verify Vagrant is UP
        i = 0
        while not v.status()['default'] == 'running':
            print "waiting for Vagrant box.."
            time.sleep(1)
            i = i + 1
            if i > 5:
                print "Something went wrong, Vagrant box is still not up."
                sys.exit(1)

        # Get a list of the docker containers we have built already
        dockerDirs = filter(lambda x: os.path.isdir('docker/' + x), os.listdir('docker'))
        imagesBuilt = [] 
        for imageInfo in self.docker.client.images():
            imagesBuilt.append(imageInfo['Repository'])

        # Build docker containers
        for dockerName in list(set(dockerDirs) - set(imagesBuilt)):
            self.docker.build(dockerName)

    def down(self, args):
        self.vagrant.destroy()

    def start(self, args):
        for dockName in args.configuration:
            self.dockyard.start(dockName)

        # dockConfig = json.load(open('dock.json'))

        # for dockName in args.configuration:
        #     if not dockConfig['docks'].get(dockName):
        #         print 'No such dock configuration [%s] found.' % dockName
        #         sys.exit(1)
    
        #     run('vagrant ssh --command "python /vagrant/scripts/dns.py %s"' % dockName)

        #     # f = open('','w')
        #     # f.write('')
        #     # f.close()

        #     #dock


    def stop(self, args):

        for id in args.configuration:
            self.dockyard.stop(id)


class DockerCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Docker related tasks """

    def build(self, args):

        # Compile a list of valid dockers to build
        dockers = []
        if 'all' in args.docker:
            dockers = os.listdir('docker')
        else:
            dockers = list(set(args.docker) & set(os.listdir('docker')))
            dockers = filter(lambda x: os.path.isdir('docker/' + x), dockers)

        # Get a list of docker containers that we want to initialize after vagrant comes up        
        for docker in dockers:
            self.docker.build(docker)

    def kill(self, args):        
        for container in args.container:
            self.docker.kill(container)

    def command(self, args):
        print args
        run('vagrant ssh --command "docker %s"' % (' '.join(args.arg)))

    def image(self, args):
        if args.action == 'list':
            self.docker.images()

        elif args.action == 'remove':
            for image in args.image:
                self.docker.removeImageById(image)

        elif args.action == 'run':
            for name in args.image:
                self.docker.runByName(name)

    def container(self, args):
        if args.action == 'list':
            #self.docker.containers()
            self.docker.listContainers()

        elif args.action == 'kill':
            for hash in args.hash:
                self.docker.killContainerById(hash)


class DockyardCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Docker related tasks """

    def init(self, args):
        self.dockyard.init()

    def list(self, args):
        self.dockyard.list()

    def start(self, args):
        for dockyardName in args.dockyard:
            self.dockyard.start(dockyardName)
            self.dns.configure(dockyardName)

    def stop(self, args):
        for dockyardName in args.dockyard:
            self.dockyard.stop(dockyardName)
            self.dns.configure(dockyardName)



