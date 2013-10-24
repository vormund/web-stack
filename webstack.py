#!/usr/bin/python
import argparse, subprocess, re, sys, os, shutil, time, json
import docker, vagrant
from lib.dict2table import *

VERSION="0.1";

def run(cmd, returncode=False, echo=True, **kargs):
    """ Executes a shell command and prints out STDOUT / STDERROR, exits on failure by default """
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, **kargs)
    if echo:
        print "$ %s" % cmd
    
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    if returncode:
        return process.returncode
    else:
        if process.returncode != 0:
            print "Something went wrong! returncode=%s" % process.returncode
            sys.exit(1)

class NoArgHelpParser(argparse.ArgumentParser):
    """ Extend parser to show help screen whene executed with no arguments """

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)            


class VagrantWrapper(object):
    """ Small wrapper around some commonly used vagrant operations """

    def vagrant(self, operation):
        run('vagrant %s' % operation)

    def up(self):
        self.vagrant('up')

        # Wait for VirtualBox tools to come online
        if not os.environ.get('VAGRANT_DEFAULT_PROVIDER') or os.environ.get('VAGRANT_DEFAULT_PROVIDER') == 'virtualbox':            
            # Wait for VirtualBox to restart
            time.sleep(30)

            while run('vagrant ssh --command "pgrep -f VBoxService"', returncode=True, echo=False):
                sys.stdout.write(".")
            print "."

        self.vagrant('reload')

    def destroy(self):
        self.vagrant('destroy')

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
            

class CommandInterpreter(object):

    vagrant = None
    docker = None

    def __init__(self, vagrant=None, docker=None):
        self.vagrant = vagrant
        self.docker = docker

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

    def dock(self, args):

        dockConfig = json.load(open('dock.json'))

        for dockName in args.configuration:
            if not dockConfig['docks'].get(dockName):
                print 'No such dock configuration [%s] found.' % dockName
                sys.exit(1)
    
            run('vagrant ssh --command "python /vagrant/scripts/dns.py %s"' % dockName)

            # f = open('','w')
            # f.write('')
            # f.close()

            #dock

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
                self.docker.removeImage(image)

        elif args.action == 'run':
            for image in args.image:
                self.docker.run(image)

    def container(self, args):
        if args.action == 'list':
            #self.docker.containers()
            self.docker.ps()

        elif args.action == 'kill':
            for container in args.container:
                self.docker.kill(container)
        
### Parse command-line arguments
rootParser = NoArgHelpParser(description='''Web-Stack Common Operation Helper''',)

## Modules
moduleSubparsers = rootParser.add_subparsers(dest='module', help='_')
stackParser = moduleSubparsers.add_parser('stack', help='Stack related commands, can combine vagrant + docker commands into a single command')
dockerParser = moduleSubparsers.add_parser('docker', help='Execute Docker related tasks from the host')

## Module - Vagrant
# vagrantParser = moduleSubparsers.add_parser('vagrant', help='Vagrant related tasks')
# subparser = vagrantParser.add_subparsers(dest='operation', help='Vagrant operations')

## Module - Stack
stackSubparsers = stackParser.add_subparsers(dest='operation', help='Stack operations')

# Stack - up
parser = stackSubparsers.add_parser('up', help='Create Vagrant VM, build Docker containers')

# Stack - down
parser = stackSubparsers.add_parser('down', help='Destroy Vagrant VM')

# Stack - 
parser = stackSubparsers.add_parser('start', help='Start a dock configuration')
parser.add_argument('configuration', type=str, nargs='+', help='Dock configuration')

parser = stackSubparsers.add_parser('stop', help='Stop a dock configuration')
parser.add_argument('configuration', type=str, nargs='+', help='Dock configuration')

## Module - Docker
dockerSubparsers = dockerParser.add_subparsers(dest='operation', help='Docker operations help')

# Exec
parser = dockerSubparsers.add_parser('command', help='Execute command')
parser.add_argument('arg', type=str, nargs='+', help='Execution arguments')

# Docker - build
parser = dockerSubparsers.add_parser('build', help='Build Docker containers')
parser.add_argument('docker', type=str, nargs='+', help='Docker container names')

# Docker - images
parser = dockerSubparsers.add_parser('image', help='Image operations')
subparser = parser.add_subparsers(dest='action', help='Image operations')
parser = subparser.add_parser('list', help='List images')
parser = subparser.add_parser('remove', help='Remove image(s)')
parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
parser = subparser.add_parser('create', help='Create image(s)')
parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
parser = subparser.add_parser('run', help='Run image(s)')
parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
parser = subparser.add_parser('history', help='Kill container(s)')

parser = dockerSubparsers.add_parser('container', help='Container operations')
subparser = parser.add_subparsers(dest='action', help='Container operations')
parser = subparser.add_parser('list', help='List container(s)')
parser = subparser.add_parser('kill', help='Kill container(s)')
parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
# parser = subparser.add_parser('restart', help='Restart a running container')
# parser = subparser.add_parser('stop', help='Stop a running container')
# parser = subparser.add_parser('top', help='Lookup the running processes of a container')
# parser = subparser.add_parser('wait', help='Block until a container stops, then print its exit code.')
# parser = subparser.add_parser('logs', help='Fetch the logs of a container')
# parser = subparser.add_parser('inspect', help='Return low-level information on a container')
# parser = subparser.add_parser('diff', help='Inspect changes on a container\'s filesystem')
# parser = subparser.add_parser('copy', help='Copy files/folders from the containers filesystem to the host path.')
# parser = subparser.add_parser('commit', help='Create a new image from a container\'s changes')
# parser = subparser.add_parser('export', help='Export the contents of a filesystem as a tar archive')


#listParser = imagesSubparsers.add_parser('list', help='List')
# removeParser = imagesSubparsers.add_parser('remove', help='Remove')
# removeParser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')

# dockerSubparsers.add_parser('ps', help='List docker containers')
# killParser = dockerSubparsers.add_parser('kill', help='Kill a running container')
# killParser.add_argument('container', type=str, nargs='+', help='Container name, \'all\' for all')

# runParser = dockerSubparsers.add_parser('run', help='Run a docker container')
# runParser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')

## Help
rootParser.add_argument('--version', action='version', version=VERSION, help="Return version of script")
args = rootParser.parse_args()

## Setup command interpreter through reflection
commandInterpreter = globals().get(args.module.capitalize() + 'CommandInterpreter')
if not commandInterpreter:
    print "Unable to find a command interpreter for [%s]" % args.module
    sys.exit(1)

# Execute
commandInterpreter = commandInterpreter( \
    vagrant=VagrantWrapper(), \
    docker=DockerWrapper(client=docker.Client(base_url='http://127.0.0.1:5555', version="1.6")))
commandInterpreter.execute(args)

