import sys
import socket
import hashlib
import mmh3

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from consistent_hashing_node_ring import NodeRing as C_Node_Ring

BUFFER_SIZE = 1024


class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()
    
    # Rendezvous hashing generate hash seed
    def get_rendezvous_hashed_seed(self):
        return mmh3.hash(str(self.host) + ':' + str(self.port))
    
    # Consistent hashing generated hash seed support with/out replica
    def get_hash_seed_with_virtual_node(self, replica):
        if replica != 0:
            key = (str(self.host) + ':' + str(self.port) + ":" + "replica:" + str(replica)).encode()
        
        key = (str(self.host) + ':' + str(self.port)).encode()

        hash_code = hashlib.md5(key)
        return hash_code.hexdigest()



def process(udp_clients)
    client_ring = C_Node_Ring(udp_clients, 5)

    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = put(u)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        hash_codes.add(str(response.decode()))


    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = get(hc)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)


def get(id):
    return serialize_GET(id)

def put(object):
    envelope_bytes, id = serialize_PUT(object)
    return envelope_bytes, id

def delete(id):
    return serialize_DELETE(id)

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)