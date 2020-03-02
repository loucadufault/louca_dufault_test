from Question_C.Proxy import ProxyFactory, Proxy
from Question_C.LRUCache import LRUCache
from Question_C.utils import distance, MAX_DISTANCE

from typing import Hashable, List, Any

class Origin:
    def __init__(self, database, max_size_of_LRUCache : int, max_age_of_LRUCache: int, initial_coordinates : Tuple[float, float], load_balancing_interval : int):
        self.database = database # the repository storing the centralized version of the data that is used by the proxy servers
        self.proxyFactory = ProxyFactory(max_size_of_LRUCache, max_age_of_LRUCache)
        self.proxies = dict()
        self.proxies[coordinates] = self.proxyFactory.produce(initial_coordinates)
        self.failed_proxies = list()

    def get(self, key : Hashable):
        '''Called by a proxy instance when a cache miss occurs.
        '''
        return self.database.get(key)

    def put(self, key : Hashable, value : Any):
        '''Called by a proxy instance upon every put request that proxy instance receives'''
        self.database.put(key, value)

    def _get_coordinates_of_nearest_proxy(self, request_coordinates : Tuple[float, float]):
        least_distance = MAX_DISTANCE

        for coordinates, proxy in self.proxies.items():
            distance_request_to_proxy = distance(request_coordinates, coordinates)
            if (distance_request_to_proxy < least_distance):
                least_distance = distance_request_to_proxy # update
                coordinates_of_nearest_proxy = coordinates # keep track of

        return coordinates_of_nearest_proxy
    
    def get_nearest_proxy(self, request_coordinates : Tuple[float, float]):
        return self.proxies[self._get_coordinates_of_nearest_proxy(request_coordinates)]

    def _add_proxy(self, new_coordinates : Tuple[float, float]):
        for coordinates, proxy in self.proxies.items():
            if (new_coordinates == coordinates):
                raise ValueError(new_coordinates)

        proxy = self.proxyFactory.produce(coordinates)
        self.proxies[coordinates] = proxy
        return proxy

    def report_failure(self, failed_coordinates : Tuple[float, float]):
        failed_proxy = self.proxies.pop(failed_coordinates)
        self.failed_proxies.append(failed_proxy)