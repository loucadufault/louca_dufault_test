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
        return self.LRUCache.get(key)

    def put(self, key : Hashable, value : Any):
        return self.LRUCache.set(key, value)

    def _set_network(self, network : Dict[Tuple[float, float], Any]):
        self.network = network
        self.network[self.coordinates] = self

    def create_and_add_proxy_to_network(self, coordinates : Tuple[float, float]):
        proxy = self.origin.proxyFactory.produce(coordinates)
        self.network[coordinates] = proxy
        proxy._set_network(self.network)

    def _get_coordinates_of_nearest_proxy(self, client_coordinates : Tuple[float, float]):
        least_distance = MAX_DISTANCE
        coordinates_of_nearest_proxy = self.coordinates # default

        for coordinates, proxy in self.network.items():
            distance_from_client_to_proxy = distance(client_coordinates, coordinates)
            if (distance_from_client_to_proxy < least_distance):
                least_distance = distance_from_client_to_proxy # update
                coordinates_of_nearest_proxy = coordinates # keep track of

        return coordinates_of_nearest_proxy
    
    def get_nearest_proxy(self, client_coordinates: Tuple[float, float]):
        return self.network[self._get_coordinates_of_nearest_proxy(client_coordinates)]








    