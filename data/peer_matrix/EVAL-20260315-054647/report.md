# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260315-054647
**Timestamp:** 2026-03-15T05:46:47.476588
**Category:** Small Language Models (<48B)
**Model Pool:** 10 slm-optimized models

## Question

Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Qwen 3 8B | 9.23 | 8.25 | 10.00 | 0.66 |
| 2 | Gemma 3 27B | 9.12 | 8.35 | 9.60 | 0.48 |
| 3 | Llama 4 Scout | 8.57 | 8.20 | 9.60 | 0.47 |
| 4 | Granite 4.0 Micro | 8.40 | 6.80 | 9.60 | 0.98 |
| 5 | Devstral Small | 8.29 | 7.65 | 8.80 | 0.35 |
| 6 | Qwen 3 32B | 8.15 | 8.15 | 8.15 | 0.00 |
| 7 | Kimi K2.5 | 8.15 | 8.15 | 8.15 | 0.00 |
| 8 | Phi-4 14B | 8.14 | 5.40 | 9.60 | 1.21 |
| 9 | Llama 3.1 8B | 7.45 | 4.80 | 8.80 | 1.59 |
| 10 | Mistral Nemo 12B | 6.17 | 3.60 | 8.80 | 1.92 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Kimi K2.5 | 5.40 |
| 2 | Qwen 3 8B | 6.95 |
| 3 | Qwen 3 32B | 7.13 |
| 4 | Mistral Nemo 12B | 8.29 |
| 5 | Devstral Small | 8.31 |
| 6 | Gemma 3 27B | 8.35 |
| 7 | Llama 4 Scout | 8.49 |
| 8 | Phi-4 14B | 8.53 |
| 9 | Granite 4.0 Micro | 8.64 |
| 10 | Llama 3.1 8B | 9.26 |

**Strictest Judge:** kimi_k25
**Most Lenient Judge:** llama31_8b
**Total Judgments:** 100
**Valid Judgments:** 66

---

## Model Pool

Models selected for **Small Language Models (<48B)** evaluation:

1. **Qwen 3 32B** (openrouter)
2. **Kimi K2.5** (openrouter)
3. **Devstral Small** (openrouter)
4. **Gemma 3 27B** (openrouter)
5. **Llama 4 Scout** (openrouter)
6. **Phi-4 14B** (openrouter)
7. **Granite 4.0 Micro** (openrouter)
8. **Qwen 3 8B** (openrouter)
9. **Mistral Nemo 12B** (openrouter)
10. **Llama 3.1 8B** (openrouter)

---

## Model Responses

### Qwen 3 32B

**Generation Time:** 91415ms
**Tokens:** 2113

```

```

### Kimi K2.5

**Generation Time:** 26117ms
**Tokens:** 2110

```

```

### Devstral Small

**Generation Time:** 3381ms
**Tokens:** 1034

```
To implement an LRU cache with per-key TTL (time-to-live) support, we need to ensure that the cache operations (get and put) are O(1), the cache is thread-safe, and it supports lazy expiration. We'll also include an eviction callback and cache hit/miss statistics.

Here's a Python implementation using the `collections.OrderedDict` for the LRU part and `threading.Lock` for thread safety. We will also use `time` to handle the TTL.

```python
import time
from collections import OrderedDict
import threading

class LRUCacheWithTTL:
    def __init__(self, max_size, eviction_callback=None):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        self.eviction_callback = eviction_callback
        self.hits = 0
        self.misses = 0

    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, ttl, timestamp = self.cache[key]
                if time.time() - timestamp > ttl:
                    # Key has expired
                    del self.cache[key]
                    self.misses += 1
                    if self.eviction_callback:
                        self.eviction_callback(key)
                    return None
                else:
                    # Key is valid
                    self.cache.move_to_end(key)
                    self.hits += 1
                    return value
            else:
                self.misses += 1
                return None

    def put(self, key, value, ttl):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            self.cache[key] = (value, ttl, time.time())
            if len(self.cache) > self.max_size:
                # Evict the least recently used item
                oldest_key, _ = self.cache.popitem(last=False)
                if self.eviction_callback:
                    self.eviction_callback(oldest_key)

    def get_stats(self):
        with self.lock:
            return {
...
```

### Gemma 3 27B

**Generation Time:** 60318ms
**Tokens:** 2118

```
```python
import threading
import time
from collections import OrderedDict

class LRUCacheWithTTL:
    """
    LRU Cache with per-key TTL support.
    """

    def __init__(self, max_size: int, eviction_callback=None):
        """
        Initializes the LRUCacheWithTTL.

        Args:
            max_size: The maximum number of items the cache can hold.
            eviction_callback: A function to be called when an item is evicted.
                               It should accept the key as an argument.
        """
        self.max_size = max_size
        self.cache = OrderedDict()
        self.ttl_map = {}  # Key: key, Value: expiration timestamp
        self.lock = threading.Lock()
        self.hit_count = 0
        self.miss_count = 0
        self.eviction_callback = eviction_callback

    def get(self, key):
        """
        Retrieves a value from the cache.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or None if the key is not found or expired.
        """
        with self.lock:
            if key in self.cache:
                if self.ttl_map[key] <= time.time():
                    # Expired, remove from cache
                    del self.cache[key]
                    del self.ttl_map[key]
                    self.miss_count += 1
                    return None
                else:
                    # Move to end to indicate recent use
                    self.cache.move_to_end(key)
                    self.hit_count += 1
                    return self.cache[key]
            else:
                self.miss_count += 1
                return None

    def put(self, key, value, ttl: int = None):
        """
        Adds a value to the cache.

        Args:
            key: The key to add.
            value: The value to add.
            ttl: The time-to-live in seconds. If None, the key will not expire.
        """
        with self.lock:
            if key in self.cache:
         ...
```

### Llama 4 Scout

**Generation Time:** 49257ms
**Tokens:** 1341

```
**LRU Cache with Per-Key TTL Support**
=====================================

### Overview

This implementation provides a thread-safe LRU cache with per-key TTL support, achieving O(1) get/put operations. It features lazy expiration, configurable max size, eviction callback, and cache hit/miss statistics.

### Code

```python
import collections
import threading
import time
from typing import Callable, Any

class LRUCache:
    def __init__(self, max_size: int, eviction_callback: Callable[[str, Any], None] = None):
        """
        Initialize the LRU cache.

        Args:
        - max_size (int): The maximum size of the cache.
        - eviction_callback (Callable[[str, Any], None]): An optional callback function called when a key is evicted.
        """
        self.max_size = max_size
        self.cache = collections.OrderedDict()
        self.lock = threading.Lock()
        self.eviction_callback = eviction_callback
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any:
        """
        Get the value associated with the given key.

        Args:
        - key (str): The key to retrieve.

        Returns:
        - Any: The value associated with the key, or None if not found.
        """
        with self.lock:
            if key in self.cache:
                value, expiry = self.cache[key]
                if time.time() < expiry:
                    self.cache.move_to_end(key)
                    self.hits += 1
                    return value
                else:
                    del self.cache[key]
                    if self.eviction_callback:
                        self.eviction_callback(key, value)
            self.misses += 1
            return None

    def put(self, key: str, value: Any, ttl: int):
        """
        Put a key-value pair into the cache with a TTL.

        Args:
        - key (str): The key to store.
        - value (Any): The value to store.
        - ttl (int): The time-to-live in seconds.
      ...
```

### Phi-4 14B

**Generation Time:** 15318ms
**Tokens:** 968

```
Implementing an LRU cache with per-key TTL support, thread safety, lazy expiration, and additional features such as eviction callbacks and statistics tracking requires careful design. Below is a Python implementation that meets these requirements using a combination of data structures and synchronization primitives.

```python
import time
from collections import OrderedDict
from threading import Lock

class LRUCache:
    def __init__(self, max_size, eviction_callback=None):
        self.max_size = max_size
        self.eviction_callback = eviction_callback
        self.cache = OrderedDict()
        self.lock = Lock()
        self.hit_count = 0
        self.miss_count = 0

    def _is_expired(self, key):
        if key in self.cache:
            value, expiry_time = self.cache[key]
            return expiry_time < time.time()
        return True

    def get(self, key):
        with self.lock:
            if key in self.cache and not self._is_expired(key):
                self.hit_count += 1
                value, expiry_time = self.cache.pop(key)
                # Re-insert to update order
                self.cache[key] = (value, expiry_time)
                return value
            else:
                self.miss_count += 1
                return None

    def put(self, key, value, ttl):
        with self.lock:
            expiry_time = time.time() + ttl
            if key in self.cache:
                self.cache.pop(key)
            elif len(self.cache) >= self.max_size:
                evicted_key, evicted_value = self.cache.popitem(last=False)
                if self.eviction_callback:
                    self.eviction_callback(evicted_key, evicted_value[0])
                self.miss_count += 1
            self.cache[key] = (value, expiry_time)

    def cache_info(self):
        with self.lock:
            return {
                'hit_count': self.hit_count,
                'miss_count': self.miss_count,
                'current_size': len(self.cache)
       ...
```

### Granite 4.0 Micro

**Generation Time:** 49843ms
**Tokens:** 1674

```
Implementing an LRU cache with per-key TTL support involves several components: maintaining the order of elements for LRU eviction, handling TTL expiration without background threads, ensuring thread safety, and providing statistics on cache hits and misses. Below is a Python implementation that meets these requirements, along with comprehensive tests.

### Implementation

```python
import threading
from collections import OrderedDict
from typing import Callable, Any, Dict, Tuple

class LruCacheWithTTL:
    def __init__(self, max_size: int, eviction_callback: Callable[[Any], None] = None):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.ttl_cache = {}  # Dictionary to store TTL expiration times
        self.eviction_callback = eviction_callback
        self.lock = threading.Lock()
        self.hit_count = 0
        self.miss_count = 0

    def get(self, key: Any, default=None) -> Any:
        with self.lock:
            if key not in self.cache:
                self.miss_count += 1
                return default
            value = self.cache[key]
            self.cache.move_to_end(key)  # Mark as recently used
            self.hit_count += 1
            return value

    def put(self, key: Any, value: Any, ttl: int = None) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if ttl:
                self.ttl_cache[key] = time.time() + ttl
            else:
                self.ttl_cache[key] = float('inf')  # No expiration

            # Eviction check
            self._evict_if_needed()

    def _evict_if_needed(self) -> None:
        with self.lock:
            while len(self.cache) > self.max_size:
                oldest_key, _ = self.cache.popitem(last=False)  # Pop the least recently used item
                if oldest_key in self.ttl_cache and self.ttl_cache[oldest_key] < time.time():
                    # TTL expired, remo...
```

### Qwen 3 8B

**Generation Time:** 473393ms
**Tokens:** 14622

```
# LRU Cache with Per-Key TTL Support

Here's a well-structured implementation of an LRU cache with per-key TTL (time-to-live) support. This implementation ensures O(1) performance for both `get` and `put` operations, supports thread safety, and includes lazy expiration (no background threads), configurable max size, eviction callbacks, and cache hit/miss statistics.

---

## ✅ Implementation Details

- **Data Structures**:
  - `OrderedDict` to maintain the order of access (LRU policy).
  - Dictionary (`_entries`) to store key-value pairs and their expiration times.
  - Thread-safe `RLock` for synchronization.

- **Key Features**:
  - **Per-key TTL**: Each entry has an individual expiration time.
  - **Lazy Expiration**: Only checks for expiration during `get` and `put` operations.
  - **Eviction Policy**: Evicts the least recently used entry when the cache is full, and handles expiration during eviction.
  - **Eviction Callback**: A user-defined callback is triggered when an entry is evicted.
  - **Hit/Miss Statistics**: Tracks the number of cache hits and misses.

- **Thread Safety**: All operations are guarded by a `RLock` to ensure thread-safe access.

---

## 📦 Code Implementation

```python
import threading
from collections import OrderedDict
import time

class LRUCache:
    def __init__(self, max_size: int, eviction_callback=None):
        """
        Initialize the LRU Cache with a maximum size and optional eviction callback.

        :param max_size: Maximum number of entries the cache can hold.
        :param eviction_callback: Optional function to call when an entry is evicted.
        """
        self.max_size = max_size
        self.eviction_callback = eviction_callback
        self._lock = threading.RLock()
        self._entries = dict()  # Maps keys to (value, expiration_time)
        self._order = OrderedDict()  # Tracks the order of keys
        self.hit_count = 0
        self.miss_count = 0

    def get(self, key):
        """
        Retrieve a val...
```

### Mistral Nemo 12B

**Generation Time:** 14238ms
**Tokens:** 801

```
To implement an LRU cache with per-key TTL support, we'll use a combination of a doubly-linked list and a dictionary to keep track of items, as well as a separate dictionary to store the TTL for each key. We'll make use of Python's `threading` module to ensure thread safety.

Here's the implementation:

```python
from collections import OrderedDict
import threading

class Node:
    def __init__(self, key, value, ttl):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.ttl_cache = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            else:
                return None

    def put(self, key, value, ttl):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            self.ttl_cache[key] = ttl

            if len(self.cache) > self.max_size:
                self.evict()

    def evict(self):
        first_key = next(iter(self.cache))
        del self.cache[first_key]
        del self.ttl_cache[first_key]

    def is_expired(self, key):
        return time.time() - self.ttl_cache[key] > self.ttl_cache[key]
```

Here are some tests to verify the implementation:

```python
import time
import unittest

class TestLRUCache(unittest.TestCase):

    def setUp(self):
        self.cache = LRUCache(3)

    def test_put_and_get(self):
        self.cache.put('key1', 'value1', 10)
        self.cache.put('key2', 'value2', 10)
        self.cache.put('key3', 'value3', 10)

        self.assertEqual(self.cache.get('key1'), 'value1')
        self.assertEqual(self.cache.get('key2'), 'value2')
        self.assertEqual(self.cache.get('key3'), 'va...
```

### Llama 3.1 8B

**Generation Time:** 14173ms
**Tokens:** 1315

```
Here's an implementation of an LRU cache with per-key TTL support in Python, meeting the specified requirements:

```python
import threading
from collections import OrderedDict

class LRUCache:
    def __init__(self, max_size, evict_callback=None):
        """
        Initialize the LRU cache.

        :param max_size: Maximum size of the cache.
        :param evict_callback: Optional callback function to be called when evicting a cache entry.
        """
        self.max_size = max_size
        self.evict_callback = evict_callback
        self.cache = OrderedDict()
        self.hit_count = 0
        self.miss_count = 0
        self._lock = threading.Lock()

    def _evict_entry(self):
        """
        Evict the least recently used entry from the cache.

        :return: The key of the evicted entry.
        """
        with self._lock:
            if self.evict_callback:
                return self.cache.popitem(last=False)
            else:
                return self.cache.popitem(last=False)

    def get(self, key, ttl=None):
        """
        Get a value from the cache.

        :param key: Cache key.
        :param ttl: Optional TTL (time-to-live) for the key. If provided, the value will be expired after the TTL.
        :return: The cached value or None if not found.
        """
        with self._lock:
            if key in self.cache:
                value = self.cache.pop(key)
                if ttl:
                    if self.cache.get(key, None):
                        self.cache.move_to_end(key)
                    else:
                        self.cache[key] = value
                else:
                    self.cache[key] = value
                self.hit_count += 1
                return value
            else:
                self.miss_count += 1
                return None

    def put(self, key, value, ttl=None):
        """
        Put a value into the cache.

        :param key: Cache key.
        :param value: Value to be cached.
       ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*