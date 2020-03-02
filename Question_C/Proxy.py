from typing import Tuple, Hashable, List
from Question_C.utils import distance, MAX_DISTANCE
from Question_C.LRUCache import LRUCache

class ProxyFactory:
    '''
    At initialization, ProxyFactory instances are provided with the parameters to configure the LRUCache instances that will be given to each proxy and the origin instance that will be given to each proxy.
    '''
    def __init__(self, max_size_of_LRUCache : int, max_age_of_LRUCache: int, origin):
        self.max_size_of_LRUCache = max_size_of_LRUCache
        self.max_age_of_LRUCache = max_age_of_LRUCache
        self.origin = origin

    def produce(self, new_coordinates : Tuple[float, float]):
        '''
        Yield a Proxy instance configured to have an LRUCache instance with the parameters given to the factory at initialization and origin instance that was provided to the factory at initialization.
        The returned Proxy instance will be initialized with the coordinated given to this method as arguments, provided a Proxy instance with the same coordinates is not already owned by the origin instance associated with this factory (and its products).
        '''
        for coordinates, proxy in self.origin.proxies.items():
            if (new_coordinates == coordinates):
                raise ValueError(new_coordinates)

        proxy = Proxy(new_coordinates, LRUCache(max_size=self.max_size_of_LRUCache, max_age=self.max_age_of_LRUCache), self.origin)
        proxy.LRUCache.set_miss_callback(self.origin.get)
        self.origin.proxies[new_coordinates] = proxy
        self.origin._deploy_proxy(proxy)
        return proxy

class Proxy:
    '''
    A Proxy instance acts as an intermediary between clients getting and putting data and the central origin server that hosts the central database that provides this data.
    It uses a personal LRUCache instance (provided and set at initialization) to cache data in get and put requests from the clients locally on the proxy server on which the Proxy instance is hosted.
    It holds an origin instance (provided and set at initialization) representing the origin server that hosts the central databse.
    It has a coordinates attribute representing the coordinates of the server on which the Proxy instance is hosted.
    A Proxy instance holds a reference to its own LRUCache instance and to its origin server (both provided and set at initialization)
    '''
    def __init__(self, coordinates : Tuple[float, float], LRUCache, origin):
        self.coordinates = coordinates

        self.origin = origin

        self.LRUCache = LRUCache
    
    def get(self, key : Hashable):
        return self.LRUCache.get(key) # get the value from the cache if it is in the cache, otherwise use the miss_callback function provided to the LRUCache instance of this proxy to retrieve the data from the origin repository

    def put(self, key : Hashable, value : Any):
        self.LRUCache.set(key, value)
        self.origin.set(key, value) # propagate the update to this value to the shared repository so that the updated value may be later propagated to other proxies when they handle a cache miss on this value