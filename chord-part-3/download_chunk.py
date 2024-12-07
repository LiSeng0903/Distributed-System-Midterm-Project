#!/usr/bin/python3

import sys
import requests
import msgpackrpc
import hashlib
import json

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def hash(str):
	return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)

filename = sys.argv[1]
ip = sys.argv[2]

client = new_client(ip, 5057)

# find metadata file
metadata_filename = filename + '_metadata.txt'
h = hash(metadata_filename)
print("Hash of {} is {}".format(metadata_filename, h))
node = client.call("find_successor", h)
node_ip = node[0].decode()
print("Downloading metadata from http://{}".format(node_ip))
response = requests.get("http://{}:5058/{}".format(node_ip, metadata_filename))
decode_response = response.content.decode('utf-8')
response_dict = json.loads(decode_response)
chunk_num = response_dict['num_chunks']

# download chunks
content = []
for i in range(chunk_num):
    chunk_filename = filename + f'_{str(i)}.txt'
    h = hash(chunk_filename)
    print("Hash of {} is {}".format(chunk_filename, h))
    node = client.call("find_successor", h)
    node_ip = node[0].decode()
    print("Downloading chunk from http://{}".format(node_ip))
    response = requests.get("http://{}:5058/{}".format(node_ip, chunk_filename))
    content.append(response.content)

# write to file
with open(filename, 'wb') as f:
    for i in range(chunk_num):
        f.write(content[i])

