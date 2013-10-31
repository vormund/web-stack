#!/usr/bin/python
import argparse, sys, json
import docker
from lib import *

VERSION = '0.1'
DOCKER_URL = 'http://127.0.0.1:5555'
DOCKER_API_VERSION = '1.6'

class NoArgHelpParser(argparse.ArgumentParser):
    """ Extend parser to show help screen whene executed with no arguments """

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)            


### Parse command-line arguments
rootParser = NoArgHelpParser(description='''Web-Stack Common Operation Helper''',)

## Modules
moduleSubparsers = rootParser.add_subparsers(dest='module', help='_')
stackParser = moduleSubparsers.add_parser('stack', help='Stack related commands, can combine vagrant + docker commands into a single command')
dockerParser = moduleSubparsers.add_parser('docker', help='Execute Docker related tasks from the host')
dockyardParser = moduleSubparsers.add_parser('dockyard', help='Dockyard related operations')

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
parser.add_argument('hash', type=str, nargs='+', help='Container hash, \'all\' for all')

## Module - Dockyard
dockyardSubparsers = dockyardParser.add_subparsers(dest='operation', help='Docker operations help')

parser = dockyardSubparsers.add_parser('init', help='Initialize Dockyard')
parser = dockyardSubparsers.add_parser('list', help='List active Dockyards')

# Dockyard - start
parser = dockyardSubparsers.add_parser('start', help='Start dockyard(s)')
parser.add_argument('dockyard', type=str, nargs='+', help='Dockyard container names')

# Dockyard - stop
parser = dockyardSubparsers.add_parser('stop', help='Stop dockyard(s)')
parser.add_argument('dockyard', type=str, nargs='+', help='Dockyard name or id')

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

# Inject Dependencies
dockyardConfig = json.load(open('dockyard.json'))
dockerWrapper = DockerWrapper(client=docker.Client(base_url=DOCKER_URL, version=DOCKER_API_VERSION))
commandInterpreter = commandInterpreter( \
    vagrant=VagrantWrapper(), \
    docker=dockerWrapper, \
    dockyard=Dockyard(dockyardConfig=dockyardConfig, docker=dockerWrapper, dockerImageFactory=DockerImageFactory(defaults=dockyardConfig['default'])) )
commandInterpreter.execute(args)

