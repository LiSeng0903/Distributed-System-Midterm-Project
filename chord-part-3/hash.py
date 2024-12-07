#!/usr/bin/python3

import sys
import os
import requests
import msgpackrpc
import hashlib

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def hash(str):
	return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)

def is_between(target_id, predecessor_id, node_id):
    if predecessor_id < node_id:
        return predecessor_id < target_id and target_id <= node_id
    else:
        return predecessor_id < target_id or target_id <= node_id
    
def shoud_migrate(target_id, predecessor_predecessor_id, predecessor_id):
    if predecessor_predecessor_id != predecessor_id:
        return is_between(target_id, predecessor_predecessor_id, predecessor_id)
    else:
        return False
    
### constant ###
CHORD_PORT = 5057
FILE_SERVER_PORT = 5058
DIRACTORY_PATH = '/home/ec2-user/files/'
# DIRACTORY_PATH = '/Users/changliseng/Projects/Distributed-System-Midterm-Project/chord-part-3/'
MY_IP = requests.get('https://api.ipify.org?format=json').json()['ip']
### constant ###

filename = sys.argv[1]

print(hash(filename))