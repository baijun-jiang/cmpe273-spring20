import math
import hashlib
import mmh3

from server_config import NODES

class NodeRing():

    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes
    
    # Rendezvous hashing
    def get_node(self, key_hex):
        score = - math.inf
        dest_node = None

        for node in self.nodes:
            hash_score = mmh3.hash(key_hex, node.get_hashed_seed())

            if hash_score >= score:
                dest_node = node
                score = hash_score

        return dest_node


def test():
    ring = NodeRing(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
# test()
