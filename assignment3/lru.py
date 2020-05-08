import collections
import functools

import collections
import functools
import hashlib
import pickle

from dill.source import getsource

def lru_cache(maxsize=100):

    def decorating_function(user_function):
        cache = collections.OrderedDict()

        @functools.wraps(user_function)
        def wrapper(*args, **kwds):
            key = args[0]

            if isinstance(key, dict):
                hashcode = hashlib.md5(pickle.dumps(key))
                key = hashcode.hexdigest()
            try:
                result = cache.pop(key)
                print("acquired item from cache")
            except KeyError:
                print("cache miss")
                result = user_function(*args, **kwds)
                if len(cache) >= maxsize:
                    cache.popitem(0)
            cache[key] = result
            return result
        return wrapper
    return decorating_function