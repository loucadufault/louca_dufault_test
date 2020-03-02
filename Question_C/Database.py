class Database:
    '''
    A generic database that must implement at least the two methods declared below.
    The specific implementation of the database is left to Admin, but it can be any typical SQL or other database so long as it can implement a table where the key is a Hashable type and the value is Any type.
    A database instance is exposed to the origin server (and is only exposed to the origin server) by passing the instance to the Origin constructor.
    '''

    def get(self, key):
        '''
        Translates to a query where the key is the given parameter key.
        '''
        pass

    def put(self, key, value):
        '''
        Translates to a database insert if the key is not already in the database, or a database update if the key is already in the database.
        '''
        pass