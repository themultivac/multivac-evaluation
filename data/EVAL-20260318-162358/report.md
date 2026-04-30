# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-162358
**Timestamp:** 2026-03-18T16:23:58.804940
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | MiniMax-01 | 6.97 | 4.40 | 7.75 | 1.19 |
| 2 | GPT-5.4 | 6.63 | 5.60 | 8.60 | 1.01 |
| 3 | MiniMax M1 | 5.80 | 2.25 | 8.60 | 1.86 |
| 4 | Claude Sonnet 4.6 | 4.90 | 2.05 | 8.60 | 2.00 |
| 5 | MiniMax M2.5 | 2.46 | 0.60 | 8.20 | 3.24 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 2.34 |
| 2 | MiniMax M1 | 4.56 |
| 3 | Claude Sonnet 4.6 | 5.12 |
| 4 | MiniMax M2.1 | 5.26 |
| 5 | MiniMax M2 | 5.94 |
| 6 | MiniMax M2.5 | 5.97 |
| 7 | MiniMax M2.7 | 6.59 |
| 8 | MiniMax-01 | 8.50 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_01
**Total Judgments:** 72
**Valid Judgments:** 33

---

## Model Pool

Models selected for **Project MiniMax** evaluation:

1. **MiniMax M2.7** (openrouter)
2. **MiniMax M2.5** (openrouter)
3. **MiniMax M2.1** (openrouter)
4. **MiniMax M2** (openrouter)
5. **MiniMax M1** (openrouter)
6. **MiniMax-01** (openrouter)
7. **Claude Sonnet 4.6** (openrouter)
8. **GPT-5.4** (openrouter)
9. **Gemini 3.1 Pro** (openrouter)

---

## Model Responses

### MiniMax M2.7

**Generation Time:** 48593ms
**Tokens:** 2144

```

```

### MiniMax M2.5

**Generation Time:** 59154ms
**Tokens:** 2141

```
Here is a complete implementation in Python. It uses a **Hash Map** for $O(1)$ lookups and a **Doubly Linked List** for $O(1)$ insertions and deletions to maintain LRU order.

### Implementation

```python
import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable, Dict, Tuple
from dataclasses import dataclass, field
import
```

### MiniMax M2.1

**Generation Time:** 18773ms
**Tokens:** 2146

```

```

### MiniMax M2

**Generation Time:** 60091ms
**Tokens:** 2142

```

```

### MiniMax M1

**Generation Time:** 34505ms
**Tokens:** 2549

```
# LRU Cache with Per-Key TTL Support

I'll implement a comprehensive, production-ready LRU cache with all the requested features. Let me create a well-structured C++ solution with extensive tests.

```cpp
/**
 * LRUCache - A thread-safe LRU cache with per-key TTL support
 * 
 * Features:
 * - O(1) get/put operations
 * - Thread-safe with fine-grained locking
 * - Lazy expiration (no background threads)
 * - Configurable max size
 * - Eviction callback
 * - Hit/miss statistics
 */

#ifndef LRU_CACHE_H
#define LRU_CACHE_H

#include <chrono>
#include <cstddef>
#include <functional>
#include <list>
#include <mutex>
#include <optional>
#include <shared_mutex>
#include <unordered_map>
#include <utility>

/**
 * @brief Cache statistics structure
 */
struct CacheStats {
    size_t hits = 0;
    size_t misses = 0;
    size_t evictions = 0;
    size_t expirations = 0;
    
    double hit_rate() const {
        size_t total = hits + misses;
        return total > 0 ? static_cast<double>(hits) / total : 0.0;
    }
    
    void reset() {
        hits = 0;
        misses = 0;
        evictions = 0;
        expirations = 0;
    }
};

/**
 * @brief Cache configuration
 */
struct CacheConfig {
    size_t max_size;
    size_t default_ttl_ms = 0;  // 0 means no expiration by default
};

/**
 * @brief LRU Cache with per-key TTL support
 * 
 * @tparam K Key type (must be hashable)
 * @tparam V Value type
 */
template<typename K, typename V>
class LRUCache {
public:
    using KeyType = K;
    using ValueType = V;
    using Duration = std::chrono::milliseconds;
    using TimePoint = std::chrono::steady_clock::time_point;
    using EvictionCallback = std::function<void(const K&, const V&)>;

private:
    /**
     * @brief Node storing cache entry
     */
    struct Node {
        K key;
        V value;
        TimePoint timestamp;
        Duration ttl;
        bool expired() const {
            if (ttl.count() <= 0) return false;
            auto now = std::chrono::steady_clock::now();
 ...
```

### MiniMax-01

**Generation Time:** 44191ms
**Tokens:** 2814

```
Below is a comprehensive implementation of an LRU (Least Recently Used) cache with per-key TTL (Time-To-Live) support in Python. This implementation meets all the specified requirements:

1. **O(1) `get` and `put` operations**: Achieved using a combination of a hash map (`dict`) and a doubly linked list.
2. **Thread-safe**: Utilizes threading locks to ensure safe access in multi-threaded environments.
3. **Lazy expiration**: Expiration checks are performed during `get` and `put` operations without the need for background threads.
4. **Configurable max size**: The cache has a maximum size that can be set during initialization.
5. **Eviction callback**: A user-defined callback function is invoked when an item is evicted from the cache.
6. **Cache hit/miss statistics**: Maintains statistics on the number of cache hits and misses.
7. **Comprehensive tests**: Includes unit tests using Python’s `unittest` framework to verify functionality.

### Implementation

```python
import threading
from collections import OrderedDict
from time import time, sleep
import unittest

class LRUCacheEntry:
    def __init__(self, key, value, ttl):
        self.key = key
        self.value = value
        self.ttl = ttl  # Time-to-live in seconds
        self.timestamp = time()

class LRUCache:
    def __init__(self, max_size=128, eviction_callback=None):
        """
        Initializes the LRU cache.

        :param max_size: Maximum number of items the cache can hold.
        :param eviction_callback: Function to call when an item is evicted.
        """
        self.max_size = max_size
        self.cache = OrderedDict()  # Maintains the order of items for LRU eviction
        self.hits = 0
        self.misses = 0
        self.eviction_callback = eviction_callback
        self.lock = threading.Lock()

    def _evict_lru(self):
        """
        Evicts the least recently used item from the cache if it exceeds max_size.
        """
        if len(self.cache) > self.max_size:
            # P...
```

### Claude Sonnet 4.6

**Generation Time:** 23631ms
**Tokens:** 2121

```
# LRU Cache with Per-Key TTL Support

## Implementation

```python
"""
LRU Cache with per-key TTL support.

Features:
- O(1) get/put operations via doubly-linked list + hash map
- Thread-safe via RWLock (readers-writer lock)
- Lazy expiration (expired entries cleaned on access)
- Configurable max size with LRU eviction
- Eviction callbacks (TTL expiry, LRU eviction, explicit delete)
- Cache hit/miss statistics
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


# ---------------------------------------------------------------------------
# Eviction reason
# ---------------------------------------------------------------------------

class EvictionReason(Enum):
    TTL_EXPIRED = auto()
    LRU_EVICTION = auto()
    EXPLICIT_DELETE = auto()
    CACHE_CLEAR = auto()


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    current_size: int = 0

    @property
    def total_requests(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        total = self.total_requests
        return self.hits / total if total > 0 else 0.0

    @property
    def miss_rate(self) -> float:
        return 1.0 - self.hit_rate

    def snapshot(self) -> "CacheStats":
        return CacheStats(
            hits=self.hits,
            misses=self.misses,
            evictions=self.evictions,
            expirations=self.expirations,
            current_size=self.current_size,
        )

    def __repr__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.m...
```

### GPT-5.4

**Generation Time:** 25108ms
**Tokens:** 2109

```
Below is a complete Python implementation of a thread-safe **LRU cache with per-key TTL**, supporting:

- **O(1)** `get` / `put` / `delete`
- **Per-key TTL**
- **Lazy expiration** only
- **Configurable max size**
- **Eviction callback**
- **Hit/miss/eviction/expiration statistics**
- **Comprehensive tests**

---

## Implementation

```python
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass(frozen=True)
class CacheStats:
    hits: int
    misses: int
    evictions: int
    expirations: int
    size: int


class _Node:
    __slots__ = ("key", "value", "expires_at", "prev", "next")

    def __init__(self, key: Any, value: Any, expires_at: Optional[float]):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCacheTTL:
    """
    Thread-safe LRU cache with per-key TTL and lazy expiration.

    Properties:
    - O(1) get/put/delete
    - max_size controls capacity
    - TTL checked lazily on access/mutation
    - optional eviction callback:
        callback(key, value, reason)
      where reason is one of: 'evicted', 'expired', 'deleted', 'replaced'
    """

    def __init__(
        self,
        max_size: int,
        on_evict: Optional[Callable[[Any, Any, str], None]] = None,
        time_func: Optional[Callable[[], float]] = None,
    ):
        if max_size <= 0:
            raise ValueError("max_size must be > 0")

        self._max_size = max_size
        self._on_evict = on_evict
        self._time = time_func or time.monotonic

        self._lock = threading.RLock()
        self._map: Dict[Any, _Node] = {}

        # Dummy head/tail for doubly linked list
        # head.next = most recently used
        # tail.prev = least recently used
        self._head = _Node(None, None, None)
        self._tail = _Node(None, None, No...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*