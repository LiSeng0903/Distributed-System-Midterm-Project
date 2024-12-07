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

# list all files in the directory
files = os.listdir(DIRACTORY_PATH)
file_hashes = [hash(file) for file in files]

# get predecessor and predecessor's predecessor
me_client = new_client(MY_IP, CHORD_PORT)
me_id = me_client.call('get_info')[2]
predecessor = me_client.call('get_predecessor')
predecessor_client = new_client(predecessor[0].decode(), CHORD_PORT)
predecessor_predecessor = predecessor_client.call('get_predecessor')

# check if any file should be migrated
for i in range(len(files)):
    if shoud_migrate(file_hashes[i], predecessor_predecessor[2], predecessor[2]):
        print('Migrating file:', files[i], f' from {MY_IP} {me_id} to {predecessor[0].decode()} {predecessor[2]}')
        try:
            file = {
                'files': open(DIRACTORY_PATH + files[i], 'rb'),
            }
            response = requests.post('http://{}:5058/upload'.format(predecessor[0].decode()), files=file)
            os.remove(DIRACTORY_PATH + files[i])
            print('File migrated:', files[i])
        except :
            print('Failed to migrate file:', files[i])
            continue
    else:
        print('No need to migrate file:', files[i])
