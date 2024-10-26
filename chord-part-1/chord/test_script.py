#!/usr/bin/python3

import msgpackrpc
import time
import sys
import random

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def find_successor(id, ring):
    for i in range(len(ring) - 1):
        if ring[i] < id <= ring[i + 1]:
            return ring[i + 1]
    return ring[0]

def kill_node(num):
    info = clients[num].call("get_info")
    clients[num].call("kill") 
    ids.remove(info[2])
    print(f"Node {info[1]} killed")
    
def print_all_info():
    for i in range(n):
        if i in kill_list:
            continue
        print("Node: ", base + i)
        print("Predecessor", clients[i].call("get_predecessor"))
        print("Successor", clients[i].call("get_successor"))
        clients[i].call("print_finger_table")
        clients[i].call("print_successor_list")

if __name__ == "__main__":
	n = int(sys.argv[1])
	base = 5057
	kill_list = [3, 7]
	lookup_times = 30

	clients = []
	ids = []
	for i in range(n):
		clients.append(new_client("127.0.0.1", base + i))
		tmp = clients[i].call("get_info")
		ids.append(tmp[2])
		print(tmp)
	ids.sort()

	clients[0].call("create")
	print("create")
	for i in range(1, n-5):
		clients[i].call("join", clients[i - 1].call("get_info"))
		print(base + i, "joined")
		time.sleep(2)
	time.sleep(20)

	print("Ring: ", ids)

	print("=====================================================")
	for i in kill_list:
		kill_node(i)
	time.sleep(40)
	print("=====================================================")
	for i in range(n-5, n):
		clients[i].call("join", clients[i - 1].call("get_info"))
		print(base + i, "joined")
		time.sleep(2)
	time.sleep(20)
	print("=====================================================")
	kill_node(11)
	time.sleep(20)
	kill_node(14)
	kill_node(15)
	time.sleep(40)
	kill_list = [3, 7, 11, 14, 15]	
  
	print("Ring: ", ids)
	# total_hops = 0
	for i in range(lookup_times):
		key = random.getrandbits(32)
		target = find_successor(key, ids)
		for j in range(n):
			if j in kill_list:
				continue
			# hop = clients[j].call("count_hop", key)
			# total_hops += hop
			# print(f"Node: {base+j}, Key: {key}, Target: {target}, Hop: {hop}")
			print(f"Node: {base+j}, Key: {key}, Target: {target}")
			try:
				assert clients[j].call("find_successor", key)[2] == target
			except:
				print("Key ", key)
				print("Target ", target)
				print("Client ", clients[j].call("get_info"))
				print("Client answer ", clients[j].call("find_successor", key))
				# clients[j].call("print_finger_table")
				exit()
			time.sleep(2)
		# break
	# print("Average hops: ", total_hops / (lookup_times*n))
	print("All lookup tests passed!")
	print("=====================================================")
    
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