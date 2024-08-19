#!/usr/bin/env python3
'''
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str,
bytes, int or float.
===============================================================================
In this exercise, we will create a get method that takes
a key string argument and an optional Callable argument named fn.
This callable will be used to convert the data back to the desired format.
Remember to conserve the original Redis.get behavior
if the key does not exist.
Also, implement 2 new methods: get_str and get_int
that will automatically parametrize Cache.get with
the correct conversion function.
===================================================================================
define a call_history decorator to store the history of inputs and outputs
for a particular function.Everytime the original function will be called,
we will add its input parameters to one list in redis,and store its output
into another list.In call_history, use the decorated function’s qualified
name and append ":inputs" and ":outputs" to create input and output list keys,
respectively.call_history has a single parameter named method that is a
Callable and returns a Callable. In the new function that the decorator will
return, use rpush to append the input arguments.
Remember that Redis can only store strings, bytes and numbers.
Therefore, we can simply use str(args) to normalize.
We can ignore potential kwargs for now.
Execute the wrapped function to retrieve the output.
Store the output using rpush in the "...:outputs" list, then return the output.
Decorate Cache.store with call_history.
======================================================================================
replay function to display the history of calls of a particular function
'''

import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps

# Define a type alias for the return type
CacheDataType = Union[str, bytes, int, float, None]


def call_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of function calls
    (inputs and outputs) in Redis.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with call history logging.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        Wrapper function that logs input arguments and
        outputs to Redis, then calls the original method.
        '''
        # Create keys for inputs and outputs
        # based on the qualified name of the function
        func_name = f"{method.__module__}.{method.__qualname__}"
        inputs_key = f"{func_name}:inputs"
        outputs_key = f"{func_name}:outputs"

        # Store the input arguments in Redis
        self._redis.rpush(inputs_key, str(args))

        # Call the original method
        result = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(outputs_key, str(result))

        # Return the result
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    '''
    Decorator to count the number of times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with a call count feature.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        Wrapper function that increments the call count
        and calls the original method.
        '''
        # Generate the key using the method's qualified name
        key = method.__qualname__

        # Increment the count for this method call in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    '''A class for caching data using Redis.
        Creates a Redis client and flushes the current database
        to ensure a clean start.
    '''

    def __init__(self):
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store data in the Redis cache with a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]):
        Returns:
            str: The key under which the data is stored in Redis.
        '''
        # Generate a random key using uuid4
        key = str(uuid.uuid4())

        # Store the data in Redis using the generated key
        self._redis.set(key, data)

        # Return the generated key
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> CacheDataType:
        '''
        Retrieve data from the Redis cache using a key
        and an optional conversion function.
        Args:
            key (str): The key to retrieve data for.
            fn (Optional[Callable]):
            A callable function that converts the retrieved
            data to the desired format.
        Returns:
            CacheDataType: The retrieved data,
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


def replay(method: Callable):
    '''
    Display the history of calls for a particular function.
    Args:
        method (Callable): The function whose call history is to be displayed.
    '''
    # Create keys for inputs and outputs
    # based on the qualified name of the function
    func_name = f"{method.__module__}.{method.__qualname__}"
    inputs_key = f"{func_name}:inputs"
    outputs_key = f"{func_name}:outputs"

    # Retrieve all inputs and outputs from Redis
    inputs = method.__self__._redis.lrange(inputs_key, 0, -1)
    outputs = method.__self__._redis.lrange(outputs_key, 0, -1)

    # Format and print the history
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, outp in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{eval(inp)}) -> {outp.decode('utf-8')}")
