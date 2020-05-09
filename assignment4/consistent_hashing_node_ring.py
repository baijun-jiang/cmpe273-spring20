import math
import hashlib

from server_config import NODES

class NodeRing():

    def __init__(self, nodes, virtual_node_count=0):
        assert len(nodes) > 0
        self.virtual_node_count = virtual_node_count
        self.node_ring = dict()
        self.node_keys = []

        for node in nodes:
            self.add_node(node)
    

    def add_node(self, node):

        for i in range(0, self.virtual_node_count):
            key = node.get_hash_seed_with_virtual_node(i)
            self.node_ring[key] = node
            self.node_keys.append(key)
        
        if self.virtual_node_count == 0:
            key = node.get_hash_seed_with_virtual_node(0)
            self.node_ring[key] = node
            self.node_keys.append(key)
        
        self.node_keys.sort()

    def get_node(self, key_hex):

        for i in range(0, len(self.node_keys)):
            if key_hex <= self.node_keys[i]:
                return self.node_ring[self.node_keys[i]]
        
        return self.node_ring[self.node_keys[0]]



