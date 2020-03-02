import time
from collections import namedtuple
from typing import Callable, Hashable, Any

class Node:
    def __init__(self, key : Hashable, value : Any, expires : bool = True):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        self.expires = expires # whether this node expires, should be true for all nodes except the dummy head and tail nodes
        self._refresh()

    def set_value(self, value : Any):
        self.value= value
        self._refresh()

    def _refresh(self):
        self.last_refresh = time.monotonic() # now

    def _get_last_refresh(self):
        return self.last_refresh if self.expires else time.monotonic()

    def get_time_since_last_refresh(self):
        return time.monotonic() - self._get_last_refresh()

class LRUCache:
    """
    Implementation of the Least Recently Used Cache as a Doubly-Linked List (DLL), going from least recently to most recently used as we traverse the DLL from head to tail.

    Each instance of the LRUCache class represents an independant LRUCache data structure.

    The DLL implementing the cache comprises Nodes, analogous to a cache line in a physical cache comprising cache blocks.
    Each Node holds some value identified by a key, analogous to a cache block holding some data identified by an adress.

    The LRUCache has a maximum size representing the maximum number of Nodes that can be placed into the DLL.
    The LRUCache has an maximum age representing the maximum time that can elapse since a Node's value was last updated after which reading the value will invalidate the Node (remove it from the cache).
    
    Rather than having a daemon thread continuously monitoring the validity of all cache DLL nodes, although this approach would benefit from concurrency we assume the server processor time will be costly,
        so cache nodes are only invalidated when "poked" (i.e. the age of a Node is polled and verified to be below the threshold at each retrieval), which does incur some overhead at each retrieval, but reduces the idle cost.
    
    The cache performance info (maximum size, current size, number of cache hits, number of cache misses, number of evicitions, number of expiries) is stored as instance variables, and can be retrieved as a named tuple by calling the cache_info method on the given LRUCache instance.
    
    Although the cache nodes themselves are stored in the DLL, the LRUCache indexes the DLL with an internal lookup table as a hash map where each item in the dict is a Node's key as the item key and the Node itself (by reference) as the item value.
    By doing this, we get O(1) access time when retrieving a Node by key (i.e. when retrieving a block of cache by its key) because of the O(1) lookup time of the hash map that indexes the DLL that allows us to skip directly to that Node in the DLL instead of traversing (as well as O(1) time when deleting an invalidated item from the hash map),
        and we get O(1) insert time when adding a Node anywhere into the DLL (for our purposes we insert only at the DLL's tail), and O(1) time when removing a Node anywhere from the DLL. Thus any get or put operation on the LRU cache is O(1).
    
    There is an optional miss_callback that can be supplied to the 
    """
    def __init__(self, max_size : int = 1000, max_age : int = 86400, miss_callback : Callable[[Hashable], Any] = None):
        if (max_size <=0):
            raise ValueError(max_size)
        if (max_age <= 0):
            raise ValueError(max_age)
        
        self.max_size = max_size # cache capacity
        self.max_age = max_age # cache expiration
        self.hash_map = {} # lookup table for the cache nodes
        self.head = Node(0, 0, expires=False) # dummy nodes to eliminate edge cases and dealing with None pointers
        self.tail = Node(0, 0, expires=False)
        self.head.next = self.tail # connect the head and tail at the start since the DLL is empty
        self.tail.prev = self.head # as the DLL grows, Nodes are added between the head and tail, that remain as dummy nodes

        if (miss_callback is not None):
            set_miss_callback(miss_callback)
        else:
            self.miss_callback = None

        self.hits, self.misses, self.evictions, self.expiries = 0, 0, 0, 0 # intialize cache performance info

    def set_miss_callback(self, miss_callback : Callable[[Hashable], Any]):
        """Public method to set the callback function that will be used by the LRUCache instance when a get method call on itself fails (i.e. cache miss).
        The miss_callback parameter is expected to be a callable accepting a key argument (that is hashable such that it can be used as a key in the hash map) and returning an appropriate value.
        The callback function is used when the LRUCache receives a get method call with a key argument that does not correspond to any Node currently in the cache. The key will then be passed to this callable, and the callable is expected to produce some value from this key.
        The value returned by the callable is then put in the cache under the key passed to the get method call, and the value returned by the callable is also returned to the caller of the get method call.
        Thus if a callback is supplied to the LRUCache instance, the get method call behaves the same to the caller regardless of whether a cache hit or miss occured (albeit slower depending on the speed of the callback supplied).
        This functionality is meant to reduce the overhead incurred by the cache consumer that must catch the KeyError otherwise raised when the key passed to the get method call does not correspond to any Node currently in the cache, then internally call some function to produce the value, then call the set method to place the new value in the cache."""
        if callable(miss_callback):
            self.miss_callback == miss_callback
        else:
            ValueError("callback argument " + str(miss_callback) + " must be callable.")

    def get(self, key : Hashable):
        if key in self.hash_map: # if the requested key is in the Cache's hash map, then the Node with that key will be somewhere in the DLL
            node = self.hash_map[key] # O(1) find the Node object by its key in the hash map
            self._remove(node) # remove the node from its current position in the DLL, to eventually be reordered as the most recently used item in the DLL (if it has not expired)

            if (node.get_time_since_last_refresh() < self.max_age): # if the node has not yet expired (it was last updated more recently than the max age threshold)
                self.hits += 1
                self._add(node) # add the node back to the DLL, but as the most recent item (adjacent to the DLL's tail dummy node)
                return node.value # note that this does not refresh the timestamps on this node
            else: # node expired 
                self.expiries += 1
                # the node stays removed from the DLL at this stage. depending on whether a callback was supplied to the LRUCache instance, the node's key will be removed from the ahsh map, or the Node will be put back int the DLL 

        self.misses += 1 # misses include expiries
        if (self.miss_callback is not None): # if there was a valid provided callback
            try:
                node = Node(key, self.read_callback(key)) # timestamps set to now
                self._add(node) # add this new node as MRU 
                return node.value
            except TypeError: # callback did not have the right signature
                pass

        del self.hash_map[node.key] # remove reference from the hash map, the node is not added back to the DLL so remove its indexed reference from the hash map
        raise KeyError(key) # only if the key passed to the get method call does not correspond to any Node currently in the cache, and there was no callback function supplied to handle cache misses

    def put(self, key : Hashable, value : Any):
        if (key in self.hash_map): # if the requested key is in the Cache's hash map, then the Node with that key will be somewhere in the DLL
            self._remove(self.hash_map[key]) # to update the cache block by the given key, we need to delete the Node object representing the cache block and create a new Node object and put it in the DLL as MRU
        node = Node(key, value) # timestamps set to now
        self._add(node) # add to DLL tail (MRU)
        self.hash_map[key] = node # update the references indexed by the key in the hash map (only the value of the item in the hash map changes, the key remains) 

        if (len(self.hash_map) > self.max_size): # LRUCache has reached its maximum size
            self.evictions += 1
            node = self.head.next # LRU node is at the DLL head (adjacent to head dummy node)
            self._remove(node)
            del self.hash_map[node.key]

    def size(self):
        return len(self.hash_map)

    def cache_info(self):
        CacheInfo = namedtuple('Info', 'hits misses max_age expiries curr_size max_size evictions')
        return CacheInfo(self.hits, self.misses, self.max_age, self.expiries, self.size(), self.max_size, self.evictions)

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node # connect previous node to the node's next
        next_node.prev = prev_node # connect next node to the node's previous
        # the node is skipped over in the DLL, but not deleted as the object itself may be added back into the DLL (in the case of moving a node to the DLL tail)

    def _add(self, node):
        most_recent_node = self.tail.prev # the node at the tail of the DLL (i.e. right before the dummy tail node) is the one that has been most recently retrieved or updated

        most_recent_node.next = node # the previous most recent node is placed before the node
        self.tail.prev = node # the DLL tail dummy node is connected to the node, making the node the new most recent node (adjacent to the dummy tail node)
        node.prev = most_recent_node # the node is connected after the previous most recent node, completeing the double link
        node.next = self.tail # the node is connected before the dummy tail node