# Consistent Hashing and RHW Hashing

The distributed cache you implemented in the midterm is based on naive modula hashing to shard the data.

## Part I.

Implement Rendezvous hashing to shard the data.


## Part II.

Implement consistent hashing to shard the data.

Features:

* Add virtual node layer in the consistent hashing.
* Implement virtual node with data replication. 

## TO Run

This assignment is written based on midterm code. The udp server nodes will have two way of generating hash seed, one is for rendezvous hashing and the other is used for consistent hashing. And the actual implementation for rendezvous hashing and consistent hashing are in rendezvous_hashing_node_ring.py and consistent_hashing_node_ring.py. In consistent_hashing_node_ring.py it supports adding any number of replications. To use it simply run the class signuture NodeRing(nodes, number_of_replications)

To avoid complications, you can choose to test rendezvous hashing and consistent hashing by running rendezvous_hashing_cache_client.py and consistent_hashing_cache_client.py respectfully.