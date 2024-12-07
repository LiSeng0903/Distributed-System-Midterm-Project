import boto3
import msgpackrpc
import requests
import sys

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

my_public_IPAddr = requests.get('https://api.ipify.org?format=json').json()['ip']

id = int(sys.argv[1])

my_chord_client = new_client(my_public_IPAddr, 5057)
print(my_chord_client.call('find_successor', id)) 