#!/usr/bin/env python3
'''Create a Cache class. In the __init__ method,
    store an instance of the Redis client as a private variable named _redis
    (using redis.Redis()) and flush the instance using flushdb.

    Create a store method that takes a data argument and returns a string.
    The method should generate a random key (e.g. using uuid),
    store the input data in Redis using the random key and return the key.

    Type-annotate store correctly. Remember that data can be a str,
    bytes, int or float
    ===============================================================================
'''


import redis
import uuid
from typing import Union


class Cache:
    '''A class for caching data using Redis.
        Creates a Redis client and flushes the current database
        to ensure a clean start
    '''
    def __init__(self):
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data in the Redis cache with a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]):
        Returns:
            str: The key under which the data is stored in Redis.'''
        # Generate a random key using uuid4
        key = str(uuid.uuid4())

        # Store the data in Redis using the generated key
        self._redis.set(key, data)

        # Return the generated key
        return key
