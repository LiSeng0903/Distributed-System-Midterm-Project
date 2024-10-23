#!/usr/bin/python3

import msgpackrpc
import time
import sys
import random

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

if __name__ == "__main__":
	n = int(sys.argv[1])
	base = 5057
 
	clients = []
	for i in range(n):
		clients.append(new_client("127.0.0.1", base + i))
		print(clients[i].call("get_info"))

	clients[0].call("create")
	print("create")
	for i in range(1, n):
		clients[i].call("join", clients[i - 1].call("get_info"))
		print(base + i, "joined")
		time.sleep(2)
	sys.exit()
    
	for i in range(n):
		print(base + i)
		print(clients[i].call("get_predecessor"))
		print(clients[i].call("get_successor"))


	print("=====================================================")
	time.sleep(20)
	for i in range(5):
		key = random.getrandbits(32)
		print("key: ", key)
		for j in range(n):
			print(base + j, clients[j].call("find_successor", key))
			time.sleep(2)
    
# client_1 = new_client("127.0.0.1", 5057)
# client_2 = new_client("127.0.0.1", 5058)
# client_3 = new_client("127.0.0.1", 5059)

# print(client_1.call("get_info"))
# print(client_2.call("get_info"))
# print(client_3.call("get_info"))

# client_1.call("create")
# print("create")
# time.sleep(2)
# client_2.call("join", client_1.call("get_info"))
# print("5058 joined")
# time.sleep(2)
# client_3.call("join", client_2.call("get_info"))
# print("5059 joined")
# time.sleep(2)
# print("5057")
# print(client_1.call("get_successor"))
# print(client_1.call("get_predecessor"))
# print("5058")
# print(client_2.call("get_successor"))
# print(client_2.call("get_predecessor"))
# print("5059")
# print(client_3.call("get_successor"))
# print(client_3.call("get_predecessor"))

# test the functionality after all nodes have joined the Chord ring
# print(client_1.call("find_successor", 123))
# print(client_2.call("find_successor", 123))
# print(client_1.call("find_successor", 716540892))
# print(client_2.call("find_successor", 716540892))
# print(client_1.call("find_successor", 5057))
# print(client_2.call("find_successor", 5057))

# ./chord 127.0.0.1 5057 & ./chord 127.0.0.1 5058 & ./chord 127.0.0.1 5059 &