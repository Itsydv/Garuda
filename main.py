#!/usr/bin/env python3

from src.Garuda import Garuda
import argparse
from src import printcolors as pc
from src import artwork
import sys
import signal


def printlogo():
    pc.printout(artwork.ascii_art, pc.YELLOW)
    pc.printout("\nVersion 1 - Developed by @Itsydv\n", pc.YELLOW)


def cmdlist():
    pc.printout("check\t\t")
    print("Check who haven't followed you back")
    pc.printout("target\t\t")
    print("Set new target")
    pc.printout("cache\t\t")
    print("Clear cache of the tool")


def signal_handler(sig, frame):
    pc.printout("\nGoodbye!\n", pc.RED)
    sys.exit(0)


def _quit():
    pc.printout("Goodbye!\n", pc.RED)
    sys.exit(0)

parser = argparse.ArgumentParser(
    description='Garuda is a OSINT tool on Instagram. It helps you in finding who haven\'t following you. ')

parser.add_argument('id', type=str, help='username')
parser.add_argument('-C', '--cookies',
                    help='clear\'s previous cookies', action="store_true")
parser.add_argument(
    '-c', '--command', help='run in single command mode & execute provided command', action='store')

args = parser.parse_args()

api = Garuda(args.id, args.command, args.cookies)

commands = {
    'target': api.change_target,
    'check': api.check_not_following,
    'help': cmdlist,
    'cache': api.clear_cache,
    'quit': _quit,
    'exit': _quit
}

signal.signal(signal.SIGINT, signal_handler)

if not args.command:
    printlogo()

while True:
    if args.command:
        cmd = args.command
        _cmd = commands.get(args.command)
    else:
        pc.printout("\nRun a command: ", pc.YELLOW)
        cmd = input()
        _cmd = commands.get(cmd)

    if _cmd:
        _cmd()
    elif cmd == "":
        print("")
    else:
        pc.printout("Unknown command\n", pc.RED)

    if args.command:
        break
