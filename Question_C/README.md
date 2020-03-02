### Actors
The Geodistributed LRU Cache (or 'GeoLRUCache' hereafter) admin (or 'admin' hereafter) is the actor responsible for setting up the geodistributed cache, and maintaining (Maintenance) it.

The GeoLRUCache client (or 'client' hereafter) is the actor who will exploit the cache by optionally putting data in the cache and expecting that getting data from the cache will satisfy the 7 Functional Requirements given in the instructions

### Roles
Admin is expected to:
- initialize an instance of the Origin class on a central machine that will act as the origin server for all subsequently created proxy servers
- provide this origin instance with a database instance, that will act as the central repository persistence that will
- ensure the database instance can handle simultaneous queries and inserts (perhaps by using a concurrent db implementation like PostgreSQL, or by ensuring incoming queries and inserts are staggered as transactions)

Client is expected to:
- have an initial access to the origin server as a given
- have access to its own coordinates (the request coordinates)
- request from the origin server a reference to the nearest proxy by providing its coordinates
- perform all subsequent interactions with the cache via this proxy (note that multiple clients may share the same proxy) until either until the proxy suffers a network failure or crash (Scenario 1)

# Scenarios
## Get data from proxy server 
### Actor
Client

### Intention
The intention of client is to retrieve a data from the cache by providing the value's key

### Precondition
Client has been assigned to an operational proxy server
The assigned proxy server holds a reference to the origin server
The LRUCache of the assigned proxy server has a miss callback provided that accepts a key parameter and returns a value (by retrieving the value directly from the origin server)

### Main scenario
Client performs a get method call on its assigned proxy instance providing the key as a parameter
The proxy instance transmits the get method call to a get method call on its  internal LRUCache instance with the same key
The LRUCache instance contains a valid (not expired) copy of the value (cache hit), and it is retrieved by its key and returned to the Proxy instance caller, that returns the value to the requesting client
 As a side effect, the value retrieved from the LRUCache instance of the client's assigned proxy is placed back in the cache as the MRU item indexed by its key

### Alternative scenario
Client performs a get method call on its assigned proxy instance providing the key as a parameter
The proxy instance transmits the get method call to a get method call on its  internal LRUCache instance with the same key
The LRUCache instance does not contain a valid (not expired) copy of the value (cache miss), and it transmits the get method to its miss callback
The miss callback should be a get method on the origin instance, which is expected to accept a key parameter and return a value by retrieving from its database
The miss callback produces the value indexed by the key as it appears in the central repository persistence, and returns it up the call stack until it is returned to client by the initial get method call performed on the client's assigned proxy
As a side effect, the value retrieved from the origin server is placed in the LRUCache instance of the client's assigned proxy as the MRU item indexed by its key and its last refresh timestamps are reset to the current time

## Put data in proxy server and reflect change in repository persistence
### Actor
Client

### Intention
The intention of the client is to place data in the cache by providing a value and it's key

### Precondition


## Network failure or crash
### Actor
Client

### Intention
The intention of client is to continue exploiting the services of the GeoLRUCache after the proxy server assigned to the client suffers a network failure or crash 

### Precondition
Client holds a reference to the origin server (that they have used to initially gain access to the proxy server that has now failed)
Client has access to its own coordinates
The origin server is connected to at least one other proxy servers that is operational

### Main Scenario
Client interacts with its assigned proxy server
The assigned proxy server times out, or otherwise fails to satisfy the client request and indicates to the client a network failure or crash
Client requests the origin server remove the proxy server from its associated proxies
Client request the origin server to assign it to another operational proxy server that it is nearest to (after the failed proxy server)
Client continues interacting with its newly assigned proxy server

### Success
The proxy instance that is running on the proxy server that suffered the network failure or crash is deleted and its internal cache is wiped, the next nearest operational proxy server is assigned to another client, the origin server is associated to one less proxy instance

### Failure


## Load balancing
Load balancing
Origin server occasionally polls the cache info of the LRUCache instances of its proxies, and uses the performance algorithm to determine a ranking of which cache needs load balancing, and creates a proxy near the coordinates of the stressed cache

### Scenario 3