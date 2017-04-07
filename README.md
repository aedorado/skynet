# SKYNET (Peer to Peer file sharing)
### Overview (Targets)
1. No Peers, distributed storage and search
2. Caching of enteries at multiple nodes for performance
3. Incentives/penalties to foster collaboration 

###### We use a 3 layered network where

Layer | Description
------------ | -------------
Layer 1 | Master Server
Layer 2 | Peer Servers (servers in this layer have peer to peer connections)
Layer 3 | Clients (connected to servers in layer 2)

![Network Structure](https://github.com/Pratyush380/skynet/blob/master/project_network.jpg)
The modules for the nodes of all three layers are constructed using Python. 

###### Files Storage and Search

File names (when a new file is uploaded) are stored at the master server using the Trie data structure - an ordered tree data structure that is used to store a dynamic set or associative array where the keys are usually strings. 

The principle advantage of using trie (over a binary search tree/hash table) is that:

* Looking up data in a trie is faster (prefix based search).
* A trie can provide an alphabetical ordering of the entries by key.

Any new file name such as geo_node_one is first broken down into contiguous strings 'geo','node' & 'one' using regular expression (Regex) "([A-Za-z])\w+". Each string is now stored in the trie and the final letter of each string points eg. o(geo), e(node), e(one) points to the filename it was derived from eg. geo_node_one. 

This improves search speed. All filenames containing a particular search query can be listed since the final letter of the query will point to all filenames it is a part of. For multiple search queries filenames containing both search queries can be listed (ranked) first followed by the filenames containing only one search query. Precedence to search queries (and corresponding files) will be based on their alphabetical order, ordering withing all files corresponding to a particular search query is also alphabetical.  

![A trie](https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/250px-Trie_example.svg.png)



###### Progress

- [x] Network modules constructed (master, server, client) and tested.
- [x] Basic file upload and download tested.
- [x] Trie module implemented. 
- [ ] Caching of enteries at multiple nodes for performance
- [ ] Incentives/penalties to foster collaboration 

