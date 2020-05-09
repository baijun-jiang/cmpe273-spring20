import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT
from node_ring import NodeRing

BUFFER_SIZE = 1024
node_ring = None

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


def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
<<<<<<< HEAD
        # TODO: PART II - Instead of going to server 0, use Naive hashing to split data into multiple servers
        server_shard = node_ring.get_node(key)
        response = udp_clients[get_server_index(udp_clients, server_shard)].send(data_bytes)
        hash_codes.add(response)
        print(response)

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # TODO: PART I
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        server_shard = node_ring.get_node(key)
        response = udp_clients[get_server_index(udp_clients ,server_shard)].send(data_bytes)
        print(response)

def get_server_index(udp_clients, server_node):
    ip = server_node.get('host')
    port = server_node.get('port')

    for i in range(len(udp_clients)):
        if ip == udp_clients[i].host and port == udp_clients[i].port:
            return i
    
    return None


def process(udp_clients):
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        # Handle: PART I
        fix_me_server_id = 0
        response = udp_clients[fix_me_server_id].send(data_bytes)
        hash_codes.add(response)
=======
        response = client_ring.get_node(key).send(data_bytes)
>>>>>>> 556104674fc8fc44f8d4aa3feb2744770a1166d4
        print(response)
        hash_codes.add(str(response.decode()))


    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)


def process_sharding(udp_clients):
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        # Handle: PART II - Instead of going to server 0, use Naive hashing to split data into multiple servers
        server_shard = node_ring.get_node(key)
        response = udp_clients[get_server_index(udp_clients, server_shard)].send(data_bytes)
        hash_codes.add(response)
        print(response)

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        # Handle Part II
        server_shard = node_ring.get_node(key)
        response = udp_clients[get_server_index(udp_clients ,server_shard)].send(data_bytes)
        print(response)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Missing test options. Support option: [1-2]. 1 is for testing part 1, 2 is for testing part 2')
        sys.exit(2)
    
    choice = int(sys.argv[1])
    
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]

    if choice == 1:
        process(clients)
    
    elif choice == 2:
        node_ring = NodeRing(nodes=NODES)
        process_sharding(clients)
    
    else:
        print("Invalid option, Only support option 1 and 2")
        sys.exit(2)
