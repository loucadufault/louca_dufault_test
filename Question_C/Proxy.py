# TODO discuss load balancing
from typing import Tuple, Hashable, List
from Question_C.utils import distance, MAX_DISTANCE
from Question_C.LRUCache import LRUCache

class ProxyFactory:
    def __init__(self, max_size_of_LRUCache : int, max_age_of_LRUCache: int, origin):
        self.max_size_of_LRUCache = max_size_of_LRUCache
        self.max_age_of_LRUCache = max_age_of_LRUCache
        self.origin = origin

    def produce(self, coordinates : Tuple[float, float]):
        proxy = Proxy(coordinates, LRUCache(max_size=self.max_size_of_LRUCache, max_age=self.max_age_of_LRUCache), self.origin)

class Proxy:
    def __init__(self, coordinates : Tuple[float, float], LRUCache, origin):
        self.coordinates = coordinates

        self.origin = origin

        self.LRUCache = LRUCache
        self.LRUCache.set_miss_callback(self.origin.get)
    
    def get(self, key : Hashable):
        return self.LRUCache.get(key) # get the value from the cache if it is in the cache, otherwise use the miss_callback function provided to the LRUCache instance of this proxy to retrieve the data from the origin repository

    def put(self, key : Hashable, value : Any):
        self.LRUCache.set(key, value)
        self.origin.set(key, value) # propagate the update to this value to the shared repository