# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260315-043801
**Timestamp:** 2026-03-15T04:38:01.133610
**Category:** Small Language Models (<48B)
**Model Pool:** 10 slm-optimized models

## Question

Implement an LRU cache with per-key TTL...

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Gemma 3 27B | 9.06 | 8.20 | 9.60 | 0.45 |
| 2 | Qwen 3 8B | 9.05 | 8.25 | 9.60 | 0.44 |
| 3 | Qwen 3 32B | 8.99 | 8.25 | 9.60 | 0.42 |
| 4 | Phi-4 14B | 8.91 | 7.60 | 9.60 | 0.73 |
| 5 | Devstral Small | 8.66 | 8.25 | 9.05 | 0.27 |
| 6 | Granite 4.0 Micro | 8.65 | 8.00 | 9.05 | 0.37 |
| 7 | Llama 4 Scout | 8.59 | 8.25 | 9.05 | 0.31 |
| 8 | Mistral Nemo 12B | 8.16 | 7.20 | 8.85 | 0.51 |
| 9 | Llama 3.1 8B | 7.82 | 5.20 | 8.80 | 1.13 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Qwen 3 32B | 7.76 |
| 2 | Phi-4 14B | 8.48 |
| 3 | Mistral Nemo 12B | 8.65 |
| 4 | Granite 4.0 Micro | 8.75 |
| 5 | Llama 3.1 8B | 8.76 |
| 6 | Qwen 3 8B | 8.80 |
| 7 | Llama 4 Scout | 8.86 |
| 8 | Gemma 3 27B | 8.90 |
| 9 | Devstral Small | 8.96 |

**Strictest Judge:** qwen3_32b
**Most Lenient Judge:** devstral
**Total Judgments:** 100
**Valid Judgments:** 69

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

**Generation Time:** 33561ms
**Tokens:** 1106

```
Implementing an **LRU cache with per-key TTL** (Time To Live) combines two important features:

1. **LRU eviction policy**: When the cache is full, the least recently used item is evicted.
2. **Per-key TTL**: Each key has its own expiration time after which it should be considered stale and removed.

Below is a Python implementation of such a cache using `OrderedDict` for LRU tracking and a background cleanup mechanism to handle expired items.

---

## ✅ Features

- Add items with a custom TTL.
- Evict least recently used when capacity is exceeded.
- Automatically remove expired items during access or via periodic cleanup.
- Thread-safe optional (can add if required).

---

## 🧠 Design Overview

We use:

- An `OrderedDict` to maintain the LRU order.
- A separate dictionary to track key expiration times.
- On `get`, we check if the key exists and hasn't expired.
- Periodically, we clean up expired keys (optional based on your use-case).
- `move_to_end` in `OrderedDict` helps update usage order.

---

### ✅ Code Implementation

```python
from collections import OrderedDict
import threading
import time


class LRUTTLCache:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = OrderedDict()  # {key: value}
        self.expires_at = {}         # {key: timestamp}
        self.lock = threading.Lock()
        self.cleanup_interval = 10   # seconds
        self.running = True
        self.start_cleanup()

    def start_cleanup(self):
        """Start a background thread to periodically clean up expired items."""
        def cleanup_task():
            while self.running:
                try:
                    current_time = time.time()
                    expired_keys = [k for k in self.expires_at if self.expires_at[k] <= current_time]
                    with self.lock:
                        for key in expired_keys:
                            if key in self.cache:
                                self.cache.pop(key)
               ...
```

### Kimi K2.5

**Generation Time:** 38735ms
**Tokens:** 2064

```

```

### Devstral Small

**Generation Time:** 2763ms
**Tokens:** 809

```
Implementing an LRU (Least Recently Used) cache with per-key TTL (Time-to-Live) requires a combination of data structures to manage the cache entries and their expiration times. Here's a Python implementation using `collections.OrderedDict` for the LRU behavior and a dictionary to store the TTL for each key.

```python
import time
from collections import OrderedDict

class LRUCacheWithTTL:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.ttl = {}

    def get(self, key: str) -> (bool, any):
        if key in self.cache:
            # Move the key to the end to show that it was recently used
            self.cache.move_to_end(key)
            if self.ttl[key] > time.time():
                return True, self.cache[key]
            else:
                # Key has expired
                self.cache.pop(key)
                self.ttl.pop(key)
                return False, None
        else:
            return False, None

    def put(self, key: str, value: any, ttl: int):
        if key in self.cache:
            # Move the key to the end to show that it was recently used
            self.cache.move_to_end(key)
            self.ttl[key] = time.time() + ttl
        else:
            if len(self.cache) >= self.capacity:
                # Remove the least recently used item
                oldest_key = next(iter(self.cache))
                self.cache.pop(oldest_key)
                self.ttl.pop(oldest_key)

            # Add the new item
            self.cache[key] = value
            self.ttl[key] = time.time() + ttl

    def remove(self, key: str):
        if key in self.cache:
            self.cache.pop(key)
            self.ttl.pop(key)

    def clear(self):
        self.cache.clear()
        self.ttl.clear()

# Example usage
cache = LRUCacheWithTTL(2)
cache.put("key1", "value1", 5)
cache.put("key2", "value2", 5)

print(cache.get("key1"))  # (True, 'value1')
time.sleep(6)
print(cache.get("key1"))  # ...
```

### Gemma 3 27B

**Generation Time:** 102377ms
**Tokens:** 1642

```
```python
import time
import threading

class LRUCacheWithTTL:
    """
    An LRU cache with per-key TTL (Time To Live).

    Attributes:
        capacity: The maximum number of items the cache can hold.
        ttl: The default TTL in seconds for cache entries.
        cache: A dictionary to store the cache entries (key: (value, expiry_time)).
        lru_list: A list to maintain the order of access (least recently used to most recently used).
        lock: A lock to ensure thread safety.
    """

    def __init__(self, capacity, ttl=60):
        """
        Initializes the LRUCacheWithTTL.

        Args:
            capacity: The maximum number of items the cache can hold.
            ttl: The default TTL in seconds for cache entries.
        """
        self.capacity = capacity
        self.ttl = ttl
        self.cache = {}
        self.lru_list = []
        self.lock = threading.Lock()

    def get(self, key):
        """
        Retrieves a value from the cache based on the key.

        Args:
            key: The key of the value to retrieve.

        Returns:
            The value associated with the key if it exists and is not expired,
            otherwise None.
        """
        with self.lock:
            if key in self.cache:
                value, expiry_time = self.cache[key]
                if expiry_time > time.time():
                    # Move the key to the end of the LRU list (most recently used)
                    self.lru_list.remove(key)
                    self.lru_list.append(key)
                    return value
                else:
                    # Key has expired, remove it
                    del self.cache[key]
                    self.lru_list.remove(key)
                    return None
            else:
                return None

    def put(self, key, value, ttl=None):
        """
        Adds a key-value pair to the cache.

        Args:
            key: The key of the value.
            value: The value to store.
       ...
```

### Llama 4 Scout

**Generation Time:** 2510ms
**Tokens:** 938

```
**LRU Cache with Per-Key TTL Implementation**
=====================================================

### Overview

This implementation provides a Least Recently Used (LRU) cache with a time-to-live (TTL) feature for each key. The cache stores key-value pairs and automatically evicts the least recently used items when the cache reaches its capacity. Additionally, each key has a TTL, after which it will be automatically removed from the cache.

### Code

```python
import collections
import time
import threading

class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with a given capacity.

        :param capacity: The maximum number of items in the cache.
        """
        self.capacity = capacity
        self.cache = collections.OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: str) -> any:
        """
        Retrieve the value associated with a key from the cache.

        :param key: The key to look up.
        :return: The value associated with the key, or None if not found.
        """
        with self.lock:
            if key in self.cache:
                value, expiry = self.cache[key]
                if expiry == 0 or expiry > time.time():
                    self.cache.move_to_end(key)
                    return value
                else:
                    del self.cache[key]
            return None

    def put(self, key: str, value: any, ttl: int = 0):
        """
        Insert or update a key-value pair in the cache with a TTL.

        :param key: The key to store.
        :param value: The value to store.
        :param ttl: The time-to-live in seconds. 0 means no TTL.
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            expiry = time.time() + ttl if ttl > 0 else 0
            self.cache[key] = (value, expiry)

    d...
```

### Phi-4 14B

**Generation Time:** 13238ms
**Tokens:** 922

```
Implementing an LRU (Least Recently Used) cache with per-key TTL (Time-to-Live) involves combining the LRU eviction policy with time-based expiration for each key. To achieve this, we can use a combination of data structures, such as a dictionary for O(1) access and a doubly linked list for maintaining the order of usage, along with a mechanism to handle time-based expiration.

Below is a Python implementation of such a cache:

```python
import time
from collections import OrderedDict

class Node:
    def __init__(self, key, value, expiry):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.prev = None
        self.next = None

class LRUCacheWithTTL:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0, 0)
        self.tail = Node(0, 0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node):
        prev_node = self.head
        next_node = self.head.next
        prev_node.next = node
        node.prev = prev_node
        node.next = next_node
        next_node.prev = node

    def _evict_if_needed(self):
        while self.head.next != self.tail and (len(self.cache) > self.capacity or self.head.next.expiry < time.time()):
            node_to_evict = self.head.next
            self._remove(node_to_evict)
            del self.cache[node_to_evict.key]

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            if node.expiry < time.time():
                # Key has expired
                self._remove(node)
                del self.cache[key]
                return -1
            # Move the accessed node to the end
            self._remove(node)
            self._add(node)
            return...
```

### Granite 4.0 Micro

**Generation Time:** 33389ms
**Tokens:** 1114

```
Implementing an LRU (Least Recently Used) cache with per-key Time To Live (TTL) involves creating a data structure that can efficiently store and retrieve items based on their usage and expiration time. Below is a Python implementation of such a cache. This implementation uses the `OrderedDict` from the `collections` module to maintain the order of items based on their usage, and the `threading` module to handle the TTL expiration.

### Python Implementation

```python
from collections import OrderedDict
import threading
import time

class LRUCacheWithTTL:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        self.ttl = {}  # Dictionary to store TTL for each key

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return None
            value, ttl = self.cache[key]
            if time.time() > ttl:  # Check if the item has expired
                self.cache.pop(key)
                del self.ttl[key]
                return None
            self.cache.move_to_end(key)  # Mark the key as recently used
            return value

    def put(self, key, value, ttl_seconds):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)  # Move the key to the end to show it was recently used
            elif len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # Remove the least recently used item
            self.cache[key] = (value, time.time() + ttl_seconds)  # Store the value and its expiration time
            self.ttl[key] = time.time() + ttl_seconds  # Store the TTL expiration time for the key

    def delete(self, key):
        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
                del self.ttl[key]

    def clear_expired(self):
        with self.lock:
            current_time = time.time()
            keys...
```

### Qwen 3 8B

**Generation Time:** 455026ms
**Tokens:** 13493

```
To implement an **LRU cache with per-key TTL** in Python, we need to combine two core mechanisms:

1. **LRU eviction** — to remove the least recently used item when the cache is full.
2. **Time-to-live (TTL)** — to remove items from the cache when their expiration time is reached.

---

### ✅ Key Design Decisions

- **Data Structures**:
  - `OrderedDict`: Maintains the order of insertion and allows efficient `move_to_end` for LRU behavior.
  - `dict`: Stores the expiration time of each key.

- **TTL Handling**:
  - Each key is stored with its value and expiration time (`current_time + ttl`).
  - During `get` and `put`, we check for expiration and remove the key if it has expired.

- **LRU Behavior**:
  - When a key is accessed (`get` or `put`), it is moved to the end of the `OrderedDict` to mark it as recently used.
  - When the cache is full, the LRU item (first in the `OrderedDict`) is removed.

---

### 📦 Implementation

```python
from collections import OrderedDict
import time

class LRUCacheWithTTL:
    def __init__(self, max_size):
        """
        Initialize the LRU cache with a maximum size and per-key TTL support.

        Args:
            max_size: Maximum number of items in the cache.
        """
        self.max_size = max_size
        self.cache = OrderedDict()

    def get(self, key):
        """
        Retrieve a value from the cache if it exists and hasn't expired.

        Args:
            key: The key to look up.

        Returns:
            The value if it exists and hasn't expired, otherwise None.
        """
        current_time = time.time()
        if key in self.cache:
            value, expiration = self.cache[key]
            if expiration <= current_time:
                # The key has expired, remove it from the cache
                self.cache.pop(key)
                return None
            else:
                # Move the key to the end to mark as recently used
                self.cache.move_to_end(key)
                return va...
```

### Mistral Nemo 12B

**Generation Time:** 6228ms
**Tokens:** 488

```
Here's an implementation of an LRU (Least Recently Used) cache with per-key Time To Live (TTL) in Python using OrderedDict to keep track of the most recently used keys and their associated values and TTLs.

```python
import time
from collections import OrderedDict

class LRUTTLCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move the key to the end of the ordered dictionary (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]['value']

    def put(self, key: int, value: int, ttl: int) -> None:
        if key in self.cache:
            # If the key already exists, update its value and move it to the end
            self.cache[key]['value'] = value
            self.cache.move_to_end(key)
        else:
            # If the cache is full, remove the least recently used key (the first one in the ordered dictionary)
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            # Add the new key-value pair with its TTL
            self.cache[key] = {'value': value, 'ttl': time.time() + ttl}

    def evict_expired(self) -> None:
        now = time.time()
        # Remove keys that have expired (their TTL has passed)
        self.cache = {k: v for k, v in self.cache.items() if v['ttl'] > now}

# Example usage:
cache = LRUTTLCache(2)
cache.put(1, 10, 5)  # Key 1 with value 10 and TTL 5 seconds
cache.put(2, 20, 10)  # Key 2 with value 20 and TTL 10 seconds
print(cache.get(1))  # Output: 10
cache.evict_expired()
time.sleep(6)
print(cache.get(1))  # Output: -1 (Key 1 has expired and been removed)
```
```

### Llama 3.1 8B

**Generation Time:** 19292ms
**Tokens:** 1012

```
**LRU Cache with Per-Key TTL Implementation**
=====================================================

Below is a Python implementation of an LRU cache with per-key TTL. The cache will store key-value pairs with a limit on the maximum size of the cache. Additionally, each key will have a specific time-to-live (TTL) in seconds, after which the key will be automatically removed from the cache.

**Code**
```python
from collections import OrderedDict
import time

class LRUCache:
    def __init__(self, max_size, ttl):
        """
        Initialize the LRU cache.

        :param max_size: Maximum number of items in the cache
        :param ttl: Time-to-live (TTL) for each key in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()

    def get(self, key):
        """
        Retrieve the value associated with the given key.

        :param key: The key to retrieve
        :return: The associated value, or None if the key does not exist
        """
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value  # Move to end to mark as recently used
            return value
        return None

    def set(self, key, value):
        """
        Set the value associated with the given key.

        :param key: The key to set
        :param value: The value to associate with the key
        """
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # Remove the least recently used item (LRU) if cache is full
            lru_key = self.cache.popitem(last=False)[0]
            self._remove_lru(lru_key)
        self.cache[key] = (value, time.time())  # Store value and timestamp

    def _remove_lru(self, key):
        # Remove the least recently used item (LRU) from the cache
        self.cache.pop(key, None)

    def _remove_expired(self):
        # Remove expired items from the cache
        current_time = time.t...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*