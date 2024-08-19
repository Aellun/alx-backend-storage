#!/usr/bin/env python3
'''Fetches the HTML content of a given URL and caches the result.

    This function uses the `requests` library to obtain the
    HTML content of the specified URL.It then stores the content in Redis,
    setting an expiration time of 10 seconds for the cache.
    Additionally, it tracks how many times a particular
    URL was accessed by incrementing a count
    stored in Redis under the key "count:{url}".
        Args:
            url (str): The URL to fetch the HTML content from.
        Returns:
            str: The HTML content of the specified URL.
'''
import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_decorator(expiry_time: int) -> Callable:
    '''
    Decorator to cache function results in Redis.
    Args:
        expiry_time (int): Time in seconds for cache expiration.
    Returns:
        Callable: The wrapped function with caching.
    '''
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key based on function arguments
            key = f"cache:{args[0]}"
            # Check if result is in cache
            if redis_client.exists(key):
                print("Cache hit")
                return redis_client.get(key).decode('utf-8')

            print("Cache miss")
            # Call the original function
            result = func(*args, **kwargs)
            # Cache the result
            redis_client.setex(key, expiry_time, result)
            return result
        return wrapper
    return decorator


@cache_decorator(expiry_time=10)
def get_page(url: str) -> str:
    '''
    Fetch the HTML content of a URL.
        Args:
            url (str): The URL to fetch.
        Returns:
            str: The HTML content of the URL.
    '''
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    # Track the number of times this URL was accessed
    access_key = f"count:{url}"
    redis_client.incr(access_key)
    return response.text
