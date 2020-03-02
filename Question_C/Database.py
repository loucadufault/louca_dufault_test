class Database:
    '''
    A generic database that must implement at least the two methods declared below.
    The specific implementation of the database is left to Admin, but it can be any typical SQL or other database so long as it can implement a table where the key is a Hashable type and the value is Any type.
    A database instance is exposed to the origin server (and is only exposed to the origin server) by passing the instance to the Origin constructor.
    '''
    
    def get(self, key):
        pass

    def put(self, key, value):
        pass