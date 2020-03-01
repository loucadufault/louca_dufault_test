from Question_C.Proxy import ProxyFactory, Proxy
from Question_C.LRUCache import LRUCache
from typing import Hashable, List, Any

class Origin:
    def __init__(self, database, max_size_of_LRUCache : int, max_age_of_LRUCache: int, initial_coordinates : Tuple[float, float]):
        self.database = database
        self.proxyFactory = ProxyFactory(max_size_of_LRUCache, max_age_of_LRUCache, origin=self)
        self.proxyFactory.produce(initial_coordinates)

    def get(self, key : Hashable):
        return self.database.get(key)

    def put(self, key : Hashable, value : Any):
        self.database.put(key, value)


# class ProxyFactory:
#     def __init__(self, network_coordinates : List[Tuple[float, float]], max_size_of_LRUCache : int, max_age_of_LRUCache : int):
#         # if (len(coordinates_of_proxies) == 0):
#         #     raise ValueError(number_of_proxies)
#         self.coordinates_of_proxies = network_coordinates
#         self.max_size_of_LRUCache = max_size_of_LRUCache
#         self.max_age_of_LRUCache = max_age_of_LRUCache

#     def produce(self):
#         proxies = []
#         for coordinates in self.coordinates_of_proxies:
#             proxies.append(Proxy(coordinates, LRUCache(self.max_size_of_LRUCache, self.max_age_of_LRUCache)))
        
#         return proxies
