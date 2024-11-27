import boto3
import msgpackrpc
import requests

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

my_public_IPAddr = requests.get('https://api.ipify.org?format=json').json()['ip']

my_chord_client = new_client(my_public_IPAddr, 5057)
print(my_chord_client.call('get_info')) 