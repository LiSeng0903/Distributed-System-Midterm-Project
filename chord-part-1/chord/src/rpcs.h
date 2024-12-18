#ifndef RPCS_H
#define RPCS_H

#include "chord.h"
#include "rpc/client.h"


Node self, successor, predecessor;

int table_size = 4;

Node* finger_table = new Node[table_size];
std::vector<Node> successor_list(table_size);
// Node* successor_list = new Node[table_size];

int next = 0;

bool is_between(uint64_t id, uint64_t a, uint64_t b) {
  if (a < b) {
    return id > a && id < b;
  } else {
    return id > a || id < b;
  }
}

uint64_t mod2pow32(uint64_t num) { return num & 0xFFFFFFFF; }

void print_finger_table(){
  for (int i = 0; i < table_size; i++) {
    std::cout << "Finger table " << i << " : " << finger_table[i].id << std::endl;
  }
}

void print_successor_list(){
  for (int i = 0; i < table_size; i++) {
    std::cout << "Successor list " << i << " : " << successor_list[i].id << std::endl;
  }
}

Node get_info() { return self; } // Do not modify this line.

Node get_predecessor() { return predecessor; }

Node get_successor() { return successor; }

std::vector<Node> get_successor_list() { return successor_list; }

void update_successor_list(Node new_successor, std::vector<Node> successor_successor_list) {
  successor_successor_list.pop_back();
  successor_successor_list.insert(successor_successor_list.begin(), new_successor);
  successor_list = successor_successor_list;
}

Node closest_preceding_node(uint64_t id) {
  for (int i = table_size - 1; i >= 0; i--) {
    if (is_between(finger_table[i].id, self.id, id)) {
      return finger_table[i];
    }
  }
  for (int i = table_size - 1; i >= 0; i--) {
    if (is_between(successor_list[i].id, self.id, id)) {
      return successor_list[i];
    }
  }
  return successor;
}

int count_hop(uint64_t id) {
  if  (successor.ip == "") {
    return 0;
  }
  if (self.id == successor.id) {
    return 1;
  }
  if (is_between(id, self.id, successor.id) || id == successor.id) {
    return 1;
  }
  Node n = closest_preceding_node(id);
  rpc::client client(n.ip, n.port);
  try{
    return 1 + client.call("count_hop", id).as<int>();
  } catch (std::exception &e) {
    for (int i = table_size - 1; i >= 0; i--) {
      if (is_between(finger_table[i].id, self.id, id) && finger_table[i].id != n.id) {
        try{
          rpc::client client2(finger_table[i].ip, finger_table[i].port);
          return 1 + client2.call("count_hop", id).as<int>();
        } catch (std::exception &e) {
          continue;
        }
      }
    }
    for (int i = table_size - 1; i >= 0; i--) {
      if (is_between(successor_list[i].id, self.id, id) && finger_table[i].id != n.id) {
        try{
          rpc::client client2(successor_list[i].ip, successor_list[i].port);
          return 1 + client2.call("count_hop", id).as<int>();
        } catch (std::exception &e) {
          continue;
        }
      }
    }
    return 1;
  }
}

void create() {
  predecessor.ip = "";
  successor = self;
}

void join(Node n) {
  predecessor.ip = "";
  rpc::client client(n.ip, n.port);
  successor = client.call("find_successor", self.id).as<Node>();
  rpc::client client2(successor.ip, successor.port);
  client2.call("notify", self);
}

Node find_successor(uint64_t id) {
  // TODO: implement your `find_successor` RPC
  if  (successor.ip == "") {
    return self;
  }
  if (self.id == successor.id) {
    return self;
  }
  if (is_between(id, self.id, successor.id) || id == successor.id) {
    return successor;
  }
  Node n = closest_preceding_node(id);
  rpc::client client(n.ip, n.port);
  try{
    return client.call("find_successor", id).as<Node>();
  } catch (std::exception &e) {
    for (int i = table_size - 1; i >= 0; i--) {
      if (is_between(finger_table[i].id, self.id, id) && finger_table[i].id != n.id) {
        try{
          rpc::client client2(finger_table[i].ip, finger_table[i].port);
          return client2.call("find_successor", id).as<Node>();
        } catch (std::exception &e) {
          continue;
        }
      }
    }
    for (int i = table_size - 1; i >= 0; i--) {
      if (is_between(successor_list[i].id, self.id, id) && finger_table[i].id != n.id) {
        try{
          rpc::client client2(successor_list[i].ip, successor_list[i].port);
          return client2.call("find_successor", id).as<Node>();
        } catch (std::exception &e) {
          continue;
        }
      }
    }
    return successor;
  }
}

void stabilize() {
  if (successor.ip == "") {
    return;
  }
  try{
    rpc::client client(successor.ip, successor.port);
    Node x = client.call("get_predecessor").as<Node>();
    if (is_between(x.id, self.id, successor.id) && x.ip != "") {
      successor = x;
    }
    rpc::client client2(successor.ip, successor.port);
    std::vector<Node> successor_successor_list = client2.call("get_successor_list").as<std::vector<Node>>();
    update_successor_list(successor, successor_successor_list);
  } catch (std::exception &e) {
    for (int i = 1 ; i < table_size ; i++) {
      try{
        rpc::client client(successor_list[i].ip, successor_list[i].port);
        std::vector<Node> successor_successor_list = client.call("get_successor_list").as<std::vector<Node>>();
        update_successor_list(successor_list[i], successor_successor_list);
        successor = successor_list[0];
        break;
      }catch (std::exception &e) {
        continue;
      }
    }
  }
  // notify successor
  rpc::client client2(successor.ip, successor.port);
  client2.call("notify", self);
}

void notify(Node n) {
  if (predecessor.ip == "" || is_between(n.id, predecessor.id, self.id)) {
    predecessor = n;
  }
}

void check_predecessor() {
  try {
    rpc::client client(predecessor.ip, predecessor.port);
    Node n = client.call("get_info").as<Node>();
  } catch (std::exception &e) {
    predecessor.ip = "";
  }
}

void fix_fingers() {
  next = (next + 1) % table_size;
  uint64_t gap = mod2pow32((1 << (32 - 4 + next)));
  uint64_t id = mod2pow32(self.id + gap);
  finger_table[next] = find_successor(id);
}

void register_rpcs() {
  add_rpc("get_info", &get_info); // Do not modify this line.
  add_rpc("get_predecessor", &get_predecessor);
  add_rpc("get_successor", &get_successor);
  add_rpc("get_successor_list", &get_successor_list);
  add_rpc("create", &create);
  add_rpc("join", &join);
  add_rpc("find_successor", &find_successor);
  add_rpc("notify", &notify);
  add_rpc("print_finger_table", &print_finger_table);
  add_rpc("print_successor_list", &print_successor_list);
  add_rpc("count_hop", &count_hop);
}

void register_periodics() {
  add_periodic(check_predecessor);
  add_periodic(stabilize);
  add_periodic(fix_fingers);
}

#endif /* RPCS_H */
