# SKYNET (Peer to Peer file sharing)
### Overview (Targets)
1. No Peers, distributed storage and search
2. Caching of enteries at multiple nodes for performance
3. Incentives/penalties to foster collaboration 

###### We use a 3 layered network where

Layer | Description
------------ | -------------
Layer 1 | Master Servers
Layer 2 | Peer Servers (servers in this layer have peer to peer connections)
Layer 3 | Clients (connected to servers in layer 2)

![Network Structure](https://github.com/Pratyush380/skynet/blob/master/project_network.jpg)
The modules for the nodes of all three layers are constructed using Python. 

###### Adding nodes

The master server(s) is/are like SuperPeer(s) in a hybrid peer network. Whenever a new server with enough resources (processing power, memory) intends to join the network it is added to Layer 2 where it establishes a connection with the master server (if already present) or designates itself as the master server (If no master server is present).

A incoming server also connects with a peer server in layer 2 (if present) apart from the master server. The new servers create a hash table to establish a virtual connection with servers in layer two. Virtual connections - new nodes have topology information of layer 2.

If the master(s) is/are overloaded, servers from layer 2 maybe promoted to a be a master in layer 1 if they have sufficient free bandwidth and processing power.

Incoming clients are added to layer 3 where they connect with a server in layer 2 assigned to them by the master server(s) in layer 1. The server a incoming client connects to is decided on the basis of load, where the server with minimum load is provided to the client (by the master server(s)).

###### File upload

When a client uploads a file it is stored using the pastry protocol - at the server with hash index value closest to the file hash. The files location information is stored at the intermidiate server. The intermidiate server has a query based map of the files (to speed up retrieval).

###### File name Storage and Search

File names (when a new file is uploaded) are stored at the master server using the Trie data structure - an ordered tree data structure that is used to store a dynamic set or associative array where the keys are usually strings. 

The principle advantage of using trie (over a binary search tree/hash table) is that:

* Looking up data in a trie is faster (prefix based search).
* A trie can provide an alphabetical ordering of the entries by key.

Any new file name such as geo_node_one is first broken down into contiguous strings 'geo','node' & 'one' using regular expression (Regex) "([A-Za-z])\w+". Each string is now stored in the trie and the final letter of each string eg. o(geo), e(node), e(one) points to the filename it was derived from eg. geo_node_one. 

This improves search speed. All filenames containing a particular search query can be listed since the final letter of the query will point to all filenames it is a part of. For multiple search queries filenames containing both search queries can be listed (ranked) first followed by the filenames containing only one search query. Precedence to search queries (and corresponding files) will be based on their alphabetical order. Also ordering withing all files corresponding to a particular search query is also alphabetical.  

![A trie](https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/250px-Trie_example.svg.png)

###### File retrieval

When a query is made by a client it is forwarded to the master server through the intermidiate server. The master server then returns the list of available filenames to the intermidiate server to forward to the client. The client now selects the file it intends to retrieve. The intermidiate server now determines the peer server the desired file is stored at using the distributed hash table and provides the address to the client. The client now establishes a direct connection with the said server and retrieves the file.

***the intermidiate server uses a distributed hash table (query based map) to store location of uploaded files and to speed up retrieval***  (Caching of enteries at multiple nodes for performance)

###### Going forward

1. Security
2. Chunking of files
3. Distributed Trie tree


###### Progress

- [x] Network modules constructed (master, server, client) and tested.
- [x] File upload and download tested.
- [x] Trie module implemented. 
- [x] Single point database
- [ ] Master election from layer 2
- [ ] Pastry protocol implementation
- [ ] Caching of enteries at multiple nodes for performance (DHT implementation)
- [ ] Incentives/penalties to foster collaboration (Increased bandwidth allocation to clients providing maximum uploads)

