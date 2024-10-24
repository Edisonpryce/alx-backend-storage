#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage.
"""
from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


class Cache:
    """Represents an object for storing data in a Redis data storage.
    """

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda x: int(x))
