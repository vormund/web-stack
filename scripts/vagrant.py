#!/usr/bin/python
import argparse, subprocess, re, sys

VERSION="0.1";

parser = argparse.ArgumentParser(description='''Vagrant Operation Helper''',)
parser.add_argument('--up', '--down' type=str, help="Setup or Teardown")
parser.add_argument('--version', action='version', version=VERSION, help="Return version of script")
args = parser.parse_args()
