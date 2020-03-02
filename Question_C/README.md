# Actors
The Geo Distributed LRU Cache (or 'GeoLRUCache' hereafter) admin (or 'admin' hereafter) is the actor responsible for setting up the geodistributed cache, and maintaining it.

The GeoLRUCache client (or 'client' hereafter) is the actor who will exploit the cache by optionally putting data in the cache and expecting that getting data from the cache will satisfy the 7 Functional Requirements given in the instructions.

The GeoLRUCache database (or 'database' hereafter) is the actor who will persist the data that is shared by the proxies on the central origin machine (either local to the machine or virtual, either way there is only a single database that is accessed only by the origin server).

# Roles
Admin is expected to:
- initialize an instance of the Origin class on a central machine that will act as the origin server for all subsequently created proxy servers
- provide this origin instance with a database instance
- maintain the GeoLRUCache across machines
- know the coordinates of potential servers that may host new potential proxy instances
- deploy new proxy instances as needed on the potential servers that can communicate with Client and with origin server

Client is expected to:
- hold a reference to the origin server, even once Client is assigned a proxy server
- know its own coordinates (the request coordinates)
- request a reference to the nearest proxy server based on its own coordinates
- perform all interactions with the cache via the proxy that it was given (a.k.a. its assigned proxy) until the proxy suffers a network failure or crash
- report a network failure or crash of its assigned proxy to the origin server, and request a new nearest proxy server besides the failed proxy
- potentially share its assigned proxy server with other clients

Database is expected to:
- be exposed to the origin server, and only the origin server as a database instance (the Database class is an interface that may be implemented any number of ways)
- implement a method to get a value (where the value may be of Any type) from the persitence by key (where the key may be of any Hashable type)
- implement a method to put a value (where the value may be of Any type) in the persistence indexed by its key (where the key may be of any Hashable type), which may translate to either an insert or an update to the table depending on whether the key already existed in the table (the origin server should be agnostic to this distinction)
- ensure it can handle simultaneous queries and inserts (perhaps by using a concurrent db implementation like PostgreSQL, or by ensuring incoming queries and inserts are staggered as transactions)

# Scenarios

## Initialization of GeoLRUCache
### Actor
Admin
### Intention
The intention of admin is to initialize an instance of GeoLRUCache by selecting a machine hosting an Origin instance to act as origin server and providing it with parameters to configure the eventual Proxy instances hosted on proxy servers.
### Precondition
There exists a server upon which the Origin instance may be hosted, that also hosts a database (either locally or virtually).
### Main Scenario
Admin provides the parameters to configure the LRUCache instances of the eventual Proxy instances, and the database instance representing Database actor to initialize an Origin instance that will be hosted on the origin server.

Admin provides the Origin instances with a dictionary of potential servers where the keys are the coordinates of each server, and the values are the server instances themselves (left as an abstract concept since it is outside of the scope of this assignemnt).

Admin optionally adds proxies to the GeoLRUCache network, by specifying the coordinates of the server that will host the new Proxy instance amongst the keys in the dictionary of potential servers.

New Proxy instances are initialized (each with its personal LRUCache instance) and each is mapped to a distinct proxy server with distinct coordinates, and references to these proxies servers are kept in the Origin instance for future assignment of clients to proxy servers.

## Request a proxy server from the origin server 
### Actor
Client
### Intention
The intention of client is to receive a proxy instance nearest to its own coordinates with which it can interact.
### Precondition
An origin server exists with at least one references to a proxy server.

Client has access to its own coordinates.
### Main Scenario
Client calls the method to get the nearest proxy on its Origin instance to which it holds a reference and provides its own coordinates to the method call as an argument.

The method call iterates through all Proxy instances referenced by the Origin instance, and calculates the distance between the parameter coordinates and the coordinates of the proxy at the current iteration.

The method call determines the coordinates of the Proxy instance with the least distance to the coordinates of client, and returns this nearest Proxy instance to client.

Client begins interacting with this Proxy instance - it is said that the Proxy instance is assigned to the client and the client is assigned to this Proxy instance - until the Proxy instance suffers a network failure or crash.

## Get data from proxy server 
### Actor
Client
### Intention
The intention of client is to retrieve a data from the cache by providing the value's key
### Precondition
An origin server exists with at least one references to a proxy server.

Client has been assigned to an operational proxy server.

The assigned proxy server holds a reference to the origin server.

The LRUCache of the assigned proxy server has a miss callback provided that accepts a key parameter and returns a value (by retrieving the value directly from the origin server).
### Main Scenario
Client performs a get method call on its assigned proxy instance providing the key as a parameter.

The proxy instance transmits the get method call to a get method call on its  internal LRUCache instance with the same key.

The LRUCache instance contains a valid (not expired) copy of the value (cache hit), and it is retrieved by its key and returned to the Proxy instance caller, that returns the value to the requesting client.

As a side effect, the value retrieved from the LRUCache instance of the client's assigned proxy is placed back in the cache as the MRU item indexed by its key.

### Alternative Scenario
Client performs a get method call on its assigned proxy instance providing the key as a parameter.

The proxy instance transmits the get method call to a get method call on its internal LRUCache instance with the same key.

The LRUCache instance does not contain a valid (not expired) copy of the value (cache miss), and it transmits the get method to its miss callback.

The miss callback should be a get method on the origin instance, which is expected to accept a key parameter and return a value by retrieving from its database.

The miss callback produces the value indexed by the key as it appears in the central repository persistence, and returns it up the call stack until it is returned to client by the initial get method call performed on the client's assigned proxy.

As a side effect, the value retrieved from the origin server is placed in the LRUCache instance of the client's assigned proxy as the MRU item indexed by its key and its last refresh timestamps are reset to the current time.

## Put data in proxy server and reflect data change in central database and eventually in other proxy servers
### Actor
Client
### Intention
The intention of the client is to place data in the cache by providing a value and it's key, and to have the data change in the cache of its assigned proxy be propagated to the database of the origin server, and eventually to other proxy servers.
### Precondition
An origin server exists with at least one references to a proxy server.

Client is assigned to a proxy server.
### Main Scenario
Client performs a put method call on its assigned proxy instance providing the key and value as parameters.

The proxy instance transmits the put method call to a put method call on its internal LRUCache instance with the same key and value parameters.

The LRUCache instance creates a new cache block with the supplied value indexed by the supplied key if there was a valid copy if the value in the cache, or updates the value of the cache block indexed by the supplied key with the supplied value if there was a valid copy of the value in the cache.

As a side effect, the value put is placed in the LRUCache instance of the client's assigned proxy as the MRU item indexed by its key and its last refresh timestamps are reset to the current time.

The put method call on the LRUCache instance of client's assigned proxy resolves. 

The proxy instance transmits the put method call to a put method call on its Origin instance with the same key and value parameters.

The origin server puts the supplied value in its database as indexed by the supplied key (corresponding to either an insert or update depending on whether the supplied key was already in the database).

The data change in client's assigned proxy is now reflected in the central database.

Eventually, as other proxy servers handle cache misses by their respective clients on the same data, they will retrieve the data from the origin server database and return this data as it was put by the initial client in its assigned proxy.

The data change in client's assigned proxy is eventually reflected in other proxy servers as they handle get requests by their respective clients on that same data, if that data is not contained as a valid copy in their personal LRUCache instances (i.e. a cache miss).
## Network failure or crash
### Actor
Client
### Intention
The intention of client is to continue exploiting the services of the GeoLRUCache after the proxy server assigned to the client suffers a network failure or crash.
### Precondition
An origin server exists with at least two references to proxy servers.

Client holds a reference to the origin server (that they have used to initially gain access to the proxy server that has now failed).

Client is assigned to a proxy server.

Client has access to its own coordinates.

The origin server is connected to at least one other proxy servers that is operational.
### Main Scenario
Client interacts with its assigned proxy server.

The assigned proxy server times out, or otherwise fails to satisfy the client request and indicates to the client a network failure or crash.

Client reports the failed proxy server to the origin server.

The origin server removes the reported proxy from its references to proxies servers and added to its references to failed proxy servers for logging and maintenance.

Client request the origin server to assign it to another operational proxy server that it is nearest to (after the failed proxy server)

Client continues interacting with its newly assigned proxy server
The failed proxy instance that is running on the proxy server that suffered the network failure or crash is removed from the origin server's references to proxy servers to ensure it is not assigned to future clients until it is manually reviewed by Admin.

Client again requests from the origin server a reference to the nearest proxy by providing its coordinates (the returned proxy instance is not the reported failed proxy).

Client continues interacting with the new proxy server it was assigned.

## Load balancing
### Actor
Admin
### Intention
The intention of admin is to load balance the network of proxy servers by adding a single proxy to alleviate the load on the proxy server that is the most stressed.
### Precondition
An origin server exists with at least two references to proxy servers.

The proxy servers experience a different amount of stress as measured by their stress score.
### Main Scenario
Admin accesses the runtime environment of the origin server.

Admin calls the load balancing method on the Origin instance.

The method call iterates through all proxies referenced by the origin server, and calculates the stress score for each one, and thus determines the most stressed proxy server that has the highest stress score.
The stress score of a proxy server is determined based on the cache info metrics of its personal LRUCache instance based on this formula:

`((cache_info.hits + cache_info.evictions) - (cache_info.expiries + cache_info.misses)) / (cache_info.hits + cache_info.evictions + cache_info.expiries + cache_info.misses)`

The method adds a Proxy instance on the potential server closest to the most sressed server, effectively creating a new proxy server near the most stressed proxy server to handle some of the load of the most stressed proxy server, thus alleviating some of its stress over time.


## Maintenance
### Actor
Admin
### Intention
The intention of admin is to maintain the GeoLRUCache by reviewing proxy servers that may have experienced network failures or crashes, or to load balance the network of proxy servers by adding another proxy server to alleviate the load of the most stressed proxy server.
### Precondition
An origin server exists with at least one reference to a proxy server.
### Main Scenario
Admin accesses the runtime environment of the origin server.

Admin reviews the dictionary of failed proxies (as reported by those proxies clients).

Admin reviews the proxies in the dictionary, and restores them to be operational, and then adds them to the origin server's references to proxies such that the now restarted proxy server may begin to serve nearby clients, if it happens to be the nearest proxy server to a client requesting a proxy server from the origin server.

Admin optionally calls the load balancing method on the Origin instance, to load balance the most stressed proxy server by adding another proxy server hosted on one of the remaining potential servers nearest to that most stressed proxy.

Admin adds potential servers (a key-value where the key is the server's coordinates and the value is the server, an abstract concept) to the Origin instance's dictionary of potential servers, which will be made as a possible host for future Proxy instances that will be added.

Admin optionally manually adds proxy servers by manually providing the coordinates of a potential server that will host the new Proxy instance.
