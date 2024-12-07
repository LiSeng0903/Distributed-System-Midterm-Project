#!/usr/bin/python3

import sys
import os
import requests
import msgpackrpc
import hashlib
import json

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def hash(str):
	return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)

def split_file(file_path, chunk_size):
    chunks = []
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

### constant ###
CHUNK_SIZE = 10 * 1024 # 10 KB
### constant ###


filename = sys.argv[1]
ip = sys.argv[2]

chunks = split_file(filename, CHUNK_SIZE)

filepath = filename
metadata_filename = filename + '_metadata.txt'
slashs = [i for i, c in list(enumerate(filepath)) if c == '/']
if len(slashs) != 0:
	filename = filename[max(slashs) + 1:]
client = new_client(ip, 5057)

# store metadata on server
metadata = {
    'filename': filename,
    'num_chunks': len(chunks),
}
with open(metadata_filename, 'w') as file:
        json.dump(metadata, file)
h = hash(metadata_filename)
print("Hash of {} is {}".format(metadata_filename, h))
node = client.call("find_successor", h)
node_ip = node[0].decode()
files = {
    'files': open(metadata_filename, 'rb'),
}
print("Uploading file to http://{}".format(node_ip))
response = requests.post('http://{}:5058/upload'.format(node_ip), files=files)
os.remove(metadata_filename)

# store chunks on server
for i in range(len(chunks)):
    chunk_filename = filename + f'_{i}.txt'
    with open(chunk_filename, 'wb') as file:
        file.write(chunks[i])
    h = hash(chunk_filename)
    print("Hash of {} is {}".format(chunk_filename, h))
    node = client.call("find_successor", h)
    node_ip = node[0].decode()
    files = {
        'files': open(chunk_filename, 'rb'),
    }
    print("Uploading file to http://{}".format(node_ip))
    response = requests.post('http://{}:5058/upload'.format(node_ip), files=files)
    os.remove(chunk_filename)
