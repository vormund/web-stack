#!/usr/bin/python
import argparse, subprocess, re, sys

VERSION="0.1";

parser = argparse.ArgumentParser(description='''Vagrant Operation Helper''',)
subparsers = parser.add_subparsers(help='Setup / Teardown help')

#group = parser.add_mutually_exclusive_group()
#group.add_argument('--up', action='store_true', help="Setup camp")
#group.add_argument('--down', action='store_true', help="Teardown camp")

upParser = subparsers.add_parser('up', help='Setup help')
upParser.add_argument('docker', type=int, nargs='*', help='bar help')
upParser.add_argument('bar', type=int, help='bar help')

downParser = subparsers.add_parser('down', help='Teardown help')
downParser.add_argument('bar', type=int, help='bar help')

parser.add_argument('--version', action='version', version=VERSION, help="Return version of script")
args = parser.parse_args()
