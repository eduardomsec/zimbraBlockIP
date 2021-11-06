#!/usr/bin/python3 

from collections import Counter
from os import popen
import argparse
import re


class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'


ips = []
networks = '(10|172)\.\d+\.\d+\.\d+'


def findMail(file):
    read = open(file, 'r', encoding='utf-8', errors='ignore')
    content = read.readlines()

    for i in content:
        if 'SASL LOGIN authentication failed' in i:
            matchNetworks = re.search(networks, i)
            if matchNetworks == None:
                ip = re.findall(r'\d+\.\d+\.\d+\.\d+', i)
                ips.append(ip[0])


def blockIP(ip, debug):
    command = "iptables -nL"
    status = popen(command).read()

    if ip in status:
        if debug == True:
            print("{}{} ip blocked in another opportunity{}".format(color.YELLOW, ip, color.END))

    else:
        command = "iptables -A INPUT -p tcp -s {} -j DROP".format(ip)
        status = popen(command).read()
        print("{}Block IP - {}{}".format(color.RED, ip, color.END))


parser = argparse.ArgumentParser(description='Block Zimbra Authentication')
parser.add_argument('--file', type=str, help='File zimbra.log', default='/var/log/zimbra.log')
parser.add_argument('--authentication', type=int, help='Number of authentication failed', default=10)
parser.add_argument('--debug', type=bool, help='Active DEBUG\tTrue or False', default=False)
options = parser.parse_args()

findMail(options.file)
countIPS = Counter(ips)
if countIPS:
    for ip in countIPS:
        if options.debug == True:
            print('IP: {}\tRequests --> {}'.format(ip, countIPS.get(ip)))
        if countIPS.get(ip) >= options.authentication:
            blockIP(ip, options.debug)
