#!/usr/bin/python
#
# @author Aleksandr Karpov <karpov@angtel.ru> 2015
#
#  Script for configuring Sapfir Wireless AP with WiMark clinet (wtp)
#
import sys
import telnetlib
import argparse
import paramiko

promt=["root@Sapfir:/# "]

# Payload body
def get_payload():
    payload = "ls -l "

    return payload

# Connect via telnet
def send_by_telnet( cmd, login, password, host = "192.168.1.254" ):
    if len( cmd ) <= 0:
        print "Bad command!"
        return

    tn = telnetlib.Telnet( host )
    if login:
        tn.read_until("login: ")
        tn.write(login + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    tn.expect( promt )
    tn.write(cmd + "\n")
    tn.write("exit\n")
    print tn.read_all()
    return

# Connect via ssh
def send_by_ssh( cmd, login, password, host = "192.168.1.254" ):
    if len( cmd ) <= 0:
        print "Bad command!"
        return

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=login, password=password, port=22)
    stdin, stdout, stderr = client.exec_command( cmd )
    data = stdout.read() + stderr.read()
    client.close()
    print data
    return


# Parameters and help info
parser = argparse.ArgumentParser(description = "Connect by telnet or ssh to  \
    remote host and send command")
parser.add_argument("target", help="target ip address")
parser.add_argument("connect", choices  =["telnet", "ssh"], help = "connection type")
parser.add_argument("-l", "--login", help="target login")
parser.add_argument("-p", "--password", help="target password")
parser.add_argument("-r", "--promt", nargs="+", help="wait for promts")
args = parser.parse_args()

if args.promt and len(args.promt) > 0:
    promt = args.promt

if args.connect == "telnet":
    send_by_telnet(host=args.target, cmd=get_payload(), login=args.login, password=args.password)
else:
    send_by_ssh(host=args.target, cmd=get_payload(), login=args.login, password=args.password)
