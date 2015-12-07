#!/usr/bin/python
#
# Script for sending commands via telnet to OpenWrt host
#
# Usage: telnet.py [host] [wait for] [command1] [command2] ... [command1]
#
# @author: Aleksandr Karpov <keyfour13@gmail.com>
# @version: 0.1
import getpass
import sys
import telnetlib

if len(sys.argv) < 4:
    sys.exit(1)

commands = sys.argv[3:]
remote_command = ""

for command in commands:
    remote_command += command + "\n"

tn = telnetlib.Telnet(sys.argv[1])
tn.read_until(sys.argv[2])
tn.write(remote_command + "\n")
tn.write("exit\n")

print tn.read_all()
