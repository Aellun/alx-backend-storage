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
from typing import Callable, Optional, Union


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

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        '''
            Retrieve data from the Redis cache using a
            key and an optional conversion function.
        Args:
            key (str): The key to retrieve data for.
            fn (Optional[Callable]):
            A callable function that converts the retrieved
            data to the desired format.
        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted using the fn callable.
            If the key does not exist, returns None.
        '''
        data = self._redis.get(key)

        return fn(data) if fn else data if data is not None else None

    def get_str(self, key: str) -> Optional[str]:
        '''
        Retrieve data from Redis and convert it to a string.
        Args:
            key (str): The key to retrieve data for.
        Returns:
            Optional[str]: The retrieved data as a string,
            or None if the key does not exist.
        '''
        # Use the get method with a conversion function
        # that decodes bytes to a string
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        '''
        Retrieve data from Redis and convert it to an integer.
        Args:
            key (str): The key to retrieve data for.
        Returns:
            Optional[int]: The retrieved data as an integer,
            or None if the key does not exist.
        '''
        # Use the get method with a conversion function
        # that converts bytes to an integer
        return self.get(key, fn=int)
