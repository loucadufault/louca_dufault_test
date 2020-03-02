from Proxy import ProxyFactory, Proxy
from LRUCache import LRUCache
from utils import distance, stress, MAX_DISTANCE, LOWEST_STRESS

from typing import Hashable, List, Tuple, Dict, Any

class Origin:
    def __init__(self, database, max_size_of_LRUCache : int, max_age_of_LRUCache: int, load_balancing_interval : int):
        self.database = database # the repository storing the centralized version of the data that is used by the proxy servers
        self.proxyFactory = ProxyFactory(max_size_of_LRUCache, max_age_of_LRUCache)

        # The following two instance variables are dicts of the form {coordinates: proxy, ...}, where coordinates is a tuple of type Tuple[float, float], and proxy is a Proxy instance
        self.proxies = dict() # a one-to-many association between Origin and Proxy. The association is stored as a dictionary of proxies indexed by their coordinates for O(1) lookup time in some scenarios
        self.failed_proxies = dict() # keep track of reported proxies (presumably having suffered a network failure or crash as detected by one of the proxy's assigned client(s)) for logging and maintenance purposes
        
        self.potential_servers = dict() # an abstract dictionary of potential Server instances (kept abstract for simplicity, outside assignment scope) indexed by the physical coordinates of the server
        # used to deploy a Proxy instance onto a physical server on which it will be hosted, either in the context of Admin simply creating a new proxy, or Admin calling the load balance method to automatically add a proxy server to alleviate the load of the most stressed proxy server.

    def _set_potential_servers(self, potential_servers : Dict[Tuple[float, float], Any]):
        self.potential_servers = potential_servers

    def get(self, key : Hashable):
        '''
        Called by a LRUCache instance when a cache miss occurs while its owner Proxy instance is handling a get request it received from a client, in order to retrieve the value by key as argument from the origin server's central database.
        The returned value is forwarded to the requesting client via the Proxy instance assigned to that client (the Proxy instance that owns the LRUCache instance that called this method), and it is put in the calling LRUCache instance as the MRU item.
        '''
        return self.database.get(key)

    def put(self, key : Hashable, value : Any):
        '''
        Called by a Proxy instance upon handling every put request it receives from clients, in order to ensure that data updated (i.e. put) in the cache of a client's assigned proxy is progressively reflected in the other proxy instances.
        Each request to put data in a proxy server's cache triggers a request to put that same data in the central database, to ensure that the data changes are reflected in other proxies.
        The data changes are not immediately reflected in other proxies, since other proxies may still hold a cached version of the value that is yet to expire that they might continue serving to their client (this is the behavior intended by having cache expiry).
        However, since all Proxy instances have an LRUCache instance with the same max age, it is guaranteed that after max age time has elapsed after an arbitrary proxy handled a put request updating some value, 
            at least that updated version of that value (if not an even newer version by a more recent put request by some other arbitrary proxy) will be served to every client requesting that value.
        That is, it is impossible for one proxy to receive a put request to update or create some value (thus updating or creating a value in the central database), then max age time later,
            for any proxy to serve a client a version of that data that is older (i.e. an older version of the data that does not reflect the update made by the first proxy, or a missing value if the first proxy was creating a value) than the version of the value put by the first proxy.
        '''
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
        '''
        Called by Client to receive a Proxy instance with which it will interact with until the Proxy instance suffers a network failure or crash.
        '''
        return self.proxies[self._get_coordinates_of_nearest_proxy(request_coordinates)]

    def _get_coordinates_of_stressed_proxy(self):
        highest_stress = LOWEST_STRESS

        if (len(self.proxies.keys() == 0)):
            raise ValueError(self.proxies)

        for coordinates, proxy in self.proxies.items():
            stress_of_proxy = stress(proxy.LRUCache.cache_info())
            if (stress_of_proxy > highest_stress):
                highest_stress = stress_of_proxy
                coordinates_of_stressed_proxy = coordinates
        
        return coordinates_of_stressed_proxy

    def _get_stressed_proxy(self):
        return self.proxies[self._get_coordinates_of_stressed_proxy()]

    def _deploy_proxy(self, proxy):
        server_hosting_proxy = self.potential_servers.pop(proxy.coordinates)
        # deploy ...

    def _add_proxy(self, coordinates : Tuple[float, float]):
        return self.proxyFactory.produce(coordinates)

    def balance_load(self):
        '''
        Called by Admin to add a proxy to the network to balance the load of the most stressed proxy server.
        This is acheived by adding a single proxy at the coordinates of the potential server (from the list of coordinates supplied as argument) that is nearest to the most stressed proxy server, so that the added proxy server may take on some of the most stressed proxy server's load.
        '''
        coordinates_of_stressed_proxy = self._get_coordinates_of_stressed_proxy()
        least_distance = MAX_DISTANCE

        potential_servers_coordinates = self.potential_servers.keys()

        if (len(potential_servers_coordinates) == 0):
            raise ValueError(potential_servers_coordinates)

        for potential_server_coordinates in potential_servers_coordinates:
            distance_stressed_to_potential = distance(coordinates_of_stressed_proxy, potential_server_coordinates)
            if (distance_stressed_to_potential < least_distance):
                least_distance = distance_stressed_to_potential # update
                coordinates_of_nearest_potential = potential_server_coordinates # keep track of

        self._add_proxy(coordinates_of_nearest_potential)

    def report_failure(self, failed_coordinates : Tuple[float, float]):
        '''
        Called by client to report a failed proxy server.
        Ensures that the proxy instance reported by its coordinates is no longer assigned to other clients until it is manually added back to the origin's proxies references.
        Reported proxies (presumably having suffered a network failure or crash as detected by one of the proxy's assigned client(s)) are kept in the failed proxies for logging and maintenance purposes.
        '''
        failed_proxy = self.proxies.pop(failed_coordinates)
        self.failed_proxies[failed_coordinates] = failed_proxy