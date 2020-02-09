import time

class Node:
    def __init__(self, key, value, expires : bool = True):
        self.key = key
        self.val = value
        self.prev = None
        self.next = None
        self.expires = expires # whether this node expires, should be true for all nodes except the dummy head and tail nodes
        self._refresh()

    def set_value(self, value):
        self.val = value
        self._refresh()

    def _refresh(self):
        self.last_refresh = time.monotonic() # now

    def _get_last_refresh(self):
        return self.last_refresh if expires else time.monotonic()

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
        and we get O(1) insert time when adding a Node to the DLL's tail
    """

    def __init__(self, max_size, max_age):
        self.max_size = max_size # cache capacity
        self.max_age = max_age # cache expiration
        self.hash_map = {} # lookup table for the cache nodes
        self.head = Node(0, 0, expires=False) # dummy nodes to eliminate edge cases and dealing with None pointers
        self.tail = Node(0, 0, expires=False)
        self.head.next = self.tail # connect the head and tail at the start since the DLL is empty
        self.tail.prev = self.head # as the DLL grows, Nodes are added between the head and tail, that remain as dummy nodes
        self.curr_size = 0 # cache sixe, number of nodes in DLL (excluding head and tail dummy nodes) = number of items in hash map

        self.hits, self.misses, self.evictions, self.expiries = 0, 0, 0, 0 # cache performance info

    def get(self, key):
        if key in self.hash_map: # .keys()
            node = self.hash_map[key]
            self._remove(node)
            self._add(node)
            if (node.age < self.max_age):
                return node.val
        raise KeyError(key)

    def get(self, key):
        if key in self.hash_map: # .keys()
            node = self.hash_map[key]
            self._remove(node)

            if (node.get_time_since_last_refresh() < self.max_age):
                self._add(node)
                return node.val
        raise KeyError(key)

    def put(self, key, value):
        if (key in self.hash_map):
            self._remove(self.hash_map[key])
        node = Node(key, value) # updates timestamps
        self._add(node)
        self.hash_map[key] = node
        if (len(self.hash_map) > self.max_size):
            node = self.head.next
            self._remove(node)
            del self.hash_map[n.key]

    def size(self):
        return self.curr_size

    def cache_info(self):
        pass

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node # connect previous node to the node's next
        next_node.prev = prev_node # connect next node to the node's previous
        # the node is skipped over in the DLL, no more references to the node so it will be GC'd

    def _add(self, node):
        most_recent_node = self.tail.prev # the node at the tail of the DLL (i.e. right before the dummy tail node) is the one that has been most recently retrieved or updated

        most_recent_node.next = node # the previous most recent node is placed before the node
        self.tail.prev = node # the DLL tail dummy node is connected to the node, making the node the new most recent node (adjacent to the dummy tail node)
        node.prev = most_recent_node # the node is connected after the previous most recent node, completeing the double link
        node.next = self.tail # the node is connected before the dummy tail node