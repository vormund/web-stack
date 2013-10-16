#!/usr/bin/python
import argparse, subprocess, re, sys, os, shutil, time

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

    def destroy(self, args):
        self.vagrant('destroy')

class DockerWrapper(object):
    """ Small wrapper around Docker """

    baseDir = '/vagrant/docker'

    def build(self, dockers):
        for docker in dockers:
            # Copy our public key to docker directory to propegate inside our containers
            shutil.copy(os.path.expanduser("~") + '/.ssh/id_rsa.pub', 'docker/%s' % docker)

            run('vagrant ssh --command "cd %s/%s && docker build -t=\"%s\" ."' % (self.baseDir, docker, docker), cwd="docker/%s" % docker)


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
        self.vagrant.up()

        # Get a list of docker containers that we want to initialize after vagrant comes up        
        dockerDirs = list(set(args.docker) & set(os.listdir('docker'))) if len(args.docker) > 0 else os.listdir('docker')        
        self.docker.build(dockerDirs)

    def destroy(self, args):
        self.vagrant.destroy()

class DockerCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Docker related tasks """

    def build(self, args):
        # Get a list of docker containers that we want to initialize after vagrant comes up        
        dockerDirs = list(set(args.docker) & set(os.listdir('docker'))) if len(args.docker) > 0 else os.listdir('docker')
        self.docker.build(dockerDirs)         
    

    

### Parse command-line arguments
parser = NoArgHelpParser(description='''Web-Stack Common Operation Helper''',)

## Modules
moduleSubparsers = parser.add_subparsers(dest='module', help='Module help')
stackParser = moduleSubparsers.add_parser('stack', help='Stack related commands')
dockerParser = moduleSubparsers.add_parser('docker', help='Docker related commands')

## Module - Vagrant
vagrantSubparsers = stackParser.add_subparsers(dest='operation', help='Vagrant operations help')

# Stack - up
upParser = vagrantSubparsers.add_parser('up', help='Setup')
upParser.add_argument('docker', type=str, nargs='*', help='Docker container names')

# Stack - destroy
downParser = vagrantSubparsers.add_parser('destroy', help='Teardown')
#downParser.add_argument('bar', type=int, help='bar help')

## Module - Docker
dockerSubparsers = dockerParser.add_subparsers(dest='operation', help='Docker operations help')

# Docker - build
buildParser = dockerSubparsers.add_parser('build', help='Build Docker containers')
buildParser.add_argument('docker', type=str, nargs='*', help='Docker container names')

## Help
parser.add_argument('--version', action='version', version=VERSION, help="Return version of script")
args = parser.parse_args()

## Setup command interpreter through reflection
commandInterpreter = globals().get(args.module.capitalize() + 'CommandInterpreter')
if not commandInterpreter:
    print "Unable to find a command interpreter for [%s]" % args.module
    sys.exit(1)

# Execute
commandInterpreter = commandInterpreter(vagrant=VagrantWrapper(), docker=DockerWrapper())
commandInterpreter.execute(args)

