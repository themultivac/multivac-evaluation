# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-144035
**Timestamp:** 2026-04-02T14:40:35.802416
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Gemini 3 Flash Preview | 8.34 | 6.75 | 9.60 | 0.89 |
| 2 | GPT-5.4 | 7.90 | 5.50 | 9.60 | 1.40 |
| 3 | MiMo-V2-Flash | 6.92 | 4.35 | 9.60 | 1.56 |
| 4 | Grok 4.20 | 6.86 | 4.40 | 9.20 | 1.71 |
| 5 | DeepSeek V3 | 6.56 | 4.35 | 7.95 | 1.20 |
| 6 | Claude Opus 4.6 | 6.42 | 3.50 | 9.00 | 2.01 |
| 7 | Claude Sonnet 4.6 | 6.13 | 3.05 | 8.80 | 2.05 |
| 8 | GPT-OSS-120B | 6.04 | 2.05 | 9.20 | 2.23 |
| 9 | Gemini 3.1 Pro | 2.72 | 1.20 | 4.30 | 1.17 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.76 |
| 2 | Claude Opus 4.6 | 5.50 |
| 3 | MiniMax M2.5 | 6.04 |
| 4 | GPT-OSS-120B | 6.06 |
| 5 | Gemini 3.1 Pro | 6.10 |
| 6 | Grok 4.20 | 6.34 |
| 7 | Claude Sonnet 4.6 | 6.35 |
| 8 | Gemini 3 Flash Preview | 8.09 |
| 9 | MiMo-V2-Flash | 8.33 |
| 10 | DeepSeek V3 | 9.26 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 78

---

## Model Pool

Models selected for **Code Generation** evaluation:

1. **GPT-5.4** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **Gemini 3.1 Pro** (openrouter)
4. **Claude Sonnet 4.6** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **Gemini 3 Flash Preview** (openrouter)
9. **MiniMax M2.5** (openrouter)
10. **MiMo-V2-Flash** (openrouter)

---

## Model Responses

### GPT-5.4

**Generation Time:** 23625ms
**Tokens:** 2109

```
Below is a complete Java implementation of a thread-safe LRU cache with:

- O(1) get/put
- Per-key TTL
- Lazy expiration
- Configurable max size
- Eviction callback
- Hit/miss statistics
- Comprehensive JUnit 5 tests

The implementation uses:

- `HashMap<K, Node<K,V>>` for O(1) lookup
- A custom doubly linked list for O(1) LRU maintenance
- A single lock (`ReentrantLock`) for thread safety

---

## Production code

### `LruTtlCache.java`

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

public class LruTtlCache<K, V> {

    public enum EvictionReason {
        EXPIRED,
        SIZE,
        REPLACED,
        MANUAL
    }

    @FunctionalInterface
    public interface EvictionListener<K, V> {
        void onEvict(K key, V value, EvictionReason reason);
    }

    public static final class Stats {
        private final long hits;
        private final long misses;
        private final long evictions;

        public Stats(long hits, long misses, long evictions) {
            this.hits = hits;
            this.misses = misses;
            this.evictions = evictions;
        }

        public long getHits() {
            return hits;
        }

        public long getMisses() {
            return misses;
        }

        public long getEvictions() {
            return evictions;
        }

        @Override
        public String toString() {
            return "Stats{" +
                    "hits=" + hits +
                    ", misses=" + misses +
                    ", evictions=" + evictions +
                    '}';
        }
    }

    public interface Clock {
        long nowMillis();
    }

    public static final Clock SYSTEM_CLOCK = System::currentTimeMillis;

    private static final class Node<K, V> {
        K key;
        V value;
        long expireAtMillis;
        Node<K, V> prev;
        Node<K, V> next;

        Node(K ...
```

### Claude Opus 4.6

**Generation Time:** 26832ms
**Tokens:** 2121

```


# LRU Cache with Per-Key TTL Support

## Implementation

```python
"""
LRU Cache with per-key TTL support, thread-safety, and comprehensive features.
"""

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Hashable, Optional, TypeVar

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


@dataclass
class CacheEntry(Generic[V]):
    """Represents a single cache entry with value and expiration metadata."""
    value: V
    expire_at: Optional[float] = None  # None means no expiration
    created_at: float = field(default_factory=time.monotonic)

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.expire_at is None:
            return False
        if now is None:
            now = time.monotonic()
        return now >= self.expire_at


@dataclass
class CacheStats:
    """Thread-safe cache hit/miss statistics."""
    _hits: int = 0
    _misses: int = 0
    _evictions: int = 0
    _expirations: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def hits(self) -> int:
        with self._lock:
            return self._hits

    @property
    def misses(self) -> int:
        with self._lock:
            return self._misses

    @property
    def evictions(self) -> int:
        with self._lock:
            return self._evictions

    @property
    def expirations(self) -> int:
        with self._lock:
            return self._expirations

    @property
    def total_requests(self) -> int:
        with self._lock:
            return self._hits + self._misses

    @property
    def hit_rate(self) -> float:
        with self._lock:
            total = self._hits + self._misses
            if total == 0:
                return 0.0
            return self._hits / total

    def record_hit(self) -> None:
        with self._lock:
            self._hits += 1

    def record_miss(self) -> None:
        with...
```

### Gemini 3.1 Pro

**Generation Time:** 21930ms
**Tokens:** 2105

```
This is a complete, production-ready implementation in Python. 

To achieve **O(1) time complexity** for both `get` and `put`, the implementation uses a combination of a **Hash Map** (Python dictionary) and a **Doubly Linked List**. 

To ensure **Thread Safety**, it uses `threading.Lock`. To prevent deadlocks, eviction callbacks are executed *outside
```

### Claude Sonnet 4.6

**Generation Time:** 27427ms
**Tokens:** 2121

```
# LRU Cache with Per-Key TTL Support

## Implementation

```python
"""
LRU Cache with per-key TTL, thread safety, eviction callbacks, and statistics.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Hashable, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


# ---------------------------------------------------------------------------
# Internal node / statistics helpers
# ---------------------------------------------------------------------------

@dataclass
class _CacheEntry(Generic[V]):
    """Holds a cached value together with its expiry timestamp."""
    value: V
    expires_at: Optional[float]  # None means no expiration

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.monotonic() >= self.expires_at


@dataclass
class CacheStats:
    """Snapshot of cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0          # evicted due to capacity
    expirations: int = 0        # removed due to TTL

    @property
    def total_requests(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests

    def __repr__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.misses}, "
            f"evictions={self.evictions}, expirations={self.expirations}, "
            f"hit_rate={self.hit_rate:.2%})"
        )


EvictionCallback = Callable[[Any, Any, str], None]
"""Signature: callback(key, value, reason) where reason is 'evicted' | 'expired' | 'deleted'."""


# ---------------------------------------------------------------------------
# LRU Cache
# ---------------------------------------------------------------------------

class LRUCache(Generic...
```

### Grok 4.20

**Generation Time:** 7576ms
**Tokens:** 2225

```
**Here's a complete implementation of an LRU Cache with per-key TTL in Java:**

```java
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.function.Consumer;

/**
 * Thread-safe LRU Cache with per-key TTL support.
 * Uses lazy expiration (checks on access).
 */
public class LRUCacheWithTTL<K, V> {

    private final int maxSize;
    private final Consumer<EvictionEvent<K, V>> evictionCallback;
    
    // Main data structures
    private final ConcurrentHashMap<K, CacheEntry<K, V>> cache;
    private final LinkedHashSet<K> accessOrder; // For O(1) LRU ordering
    
    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock(true);
    
    // Statistics
    private final AtomicLong hits = new AtomicLong(0);
    private final AtomicLong misses = new AtomicLong(0);
    private final AtomicLong evictions = new AtomicLong(0);

    public static class Builder<K, V> {
        private int maxSize = 1000;
        private Consumer<EvictionEvent<K, V>> evictionCallback = e -> {};
        
        public Builder<K, V> maxSize(int maxSize) {
            this.maxSize = maxSize;
            return this;
        }
        
        public Builder<K, V> evictionCallback(Consumer<EvictionEvent<K, V>> callback) {
            this.evictionCallback = callback;
            return this;
        }
        
        public LRUCacheWithTTL<K, V> build() {
            return new LRUCacheWithTTL<>(maxSize, evictionCallback);
        }
    }

    public static <K, V> Builder<K, V> builder() {
        return new Builder<>();
    }

    public LRUCacheWithTTL(int maxSize) {
        this(maxSize, e -> {});
    }

    public LRUCacheWithTTL(int maxSize, Consumer<EvictionEvent<K, V>> evictionCallback) {
        if (maxSize <= 0) {
            throw new IllegalArgumentException("Max size must be pos...
```

### DeepSeek V3

**Generation Time:** 144773ms
**Tokens:** 2111

```
# LRU Cache with Per-Key TTL

Here's a Python implementation of an LRU cache with per-key TTL that meets all your requirements:

```python
import time
from collections import OrderedDict, defaultdict
from threading import Lock
from typing import Any, Callable, Dict, Optional, Tuple

class LRUCacheWithTTL:
    def __init__(
        self,
        max_size: int,
        eviction_callback: Optional[Callable[[Any, Any], None]] = None,
        default_ttl: Optional[float] = None,
    ):
        """
        Initialize the LRU cache with TTL support.

        Args:
            max_size: Maximum number of items the cache can hold.
            eviction_callback: Optional function called when an item is evicted.
            default_ttl: Default TTL in seconds for items without explicit TTL.
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.eviction_callback = eviction_callback
        
        self.cache: OrderedDict[Any, Tuple[Any, float]] = OrderedDict()
        self.expiry_times: Dict[Any, float] = {}
        self.lock = Lock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expired = 0

    def get(self, key: Any) -> Optional[Any]:
        """Get an item from the cache if it exists and hasn't expired."""
        with self.lock:
            self._cleanup()
            
            if key in self.cache:
                value, _ = self.cache[key]
                if key in self.expiry_times and time.time() > self.expiry_times[key]:
                    del self.cache[key]
                    del self.expiry_times[key]
                    self.expired += 1
                    self.misses += 1
                    return None
                
                # Move to end to mark as recently used
                self.cache.move_to_end(key)
                self.hits += 1
      ...
```

### GPT-OSS-120B

**Generation Time:** 33208ms
**Tokens:** 2157

```
Below is a **complete, self‑contained implementation** of an **LRU cache with per‑key TTL** in Python 3, together with a **full test‑suite** that exercises every requirement.

---

## 1. Design Overview  

| Requirement | How it is satisfied |
|-------------|--------------------|
| **O(1) get / put** | A hash‑map (`dict`) gives O(1) key lookup. A doubly‑linked list (head = most‑recent, tail = least‑recent) gives O(1) re‑ordering and eviction. |
| **Thread‑safe** | All public operations acquire a single `threading.RLock`.  The lock is re‑entrant so that callbacks that call back into the cache do not dead‑lock. |
| **Lazy expiration** | Each entry stores an absolute `expire_at` timestamp (or `None`). It is only checked when the entry is accessed (`get`/`put`/`delete`). Expired entries are removed on‑the‑fly. |
| **Configurable max size** | Constructor argument `maxsize`. When the number of *non‑expired* entries exceeds `maxsize`, the LRU entry (or entries) are evicted. |
| **Eviction callback** | Optional `on_evict(key, value)` is invoked for every entry removed because of capacity overflow *or* because it is discovered to be expired. |
| **Cache hit/miss statistics** | Counters `hits`, `misses`, `evictions`, `expired` are kept under the same lock and exposed via `stats()` (a copy of the counters). |
| **No background thread** | The cache never spawns a daemon; expiration is only evaluated on accesses. |

---

## 2. Implementation  

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LRU Cache with per‑key TTL.

Features
--------
* O(1) get / put / delete
* Thread‑safe (single re‑entrant lock)
* Lazy expiration – no background cleaning thread
* Configurable max size
* Optional eviction callback (called for evicted *and* expired items)
* Hit / miss / eviction statistics
"""

from __future__ import annotations

import time
import threading
from typing import Any, Callable, Optional, Dict, Tuple


# -------------------------------------------------------------...
```

### Gemini 3 Flash Preview

**Generation Time:** 11016ms
**Tokens:** 1825

```
To implement an LRU (Least Recently Used) cache with per-key TTL in Python, we combine a **Doubly Linked List** (for LRU ordering) and a **Hash Map** (for $O(1)$ access). 

To handle TTL efficiently without background threads, we use **Lazy Expiration**: we check if a key has expired only when it is accessed.

### Implementation

```python
import threading
import time
from typing import Any, Optional, Callable, Dict

class Node:
    def __init__(self, key, value, ttl_expiry):
        self.key = key
        self.value = value
        self.expiry = ttl_expiry  # Absolute timestamp
        self.prev = None
        self.next = None

class LRUTTLCache:
    def __init__(self, capacity: int, on_evict: Optional[Callable[[Any, Any], None]] = None):
        self.capacity = capacity
        self.on_evict = on_evict
        self.cache: Dict[Any, Node] = {}
        self.lock = threading.RLock()
        
        # Stats
        self.hits = 0
        self.misses = 0

        # Sentinel nodes for Doubly Linked List
        self.head = Node(None, None, None)
        self.tail = Node(None, None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _is_expired(self, node: Node) -> bool:
        if node.expiry is None:
            return False
        return time.time() > node.expiry

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None

            node = self.cache[key]

            # Check for lazy expiration
            if self._is_expired(node):
                self._evict_node(node)
                self.misses += 1
                return None

            # Move...
```

### MiniMax M2.5

**Generation Time:** 28923ms
**Tokens:** 2141

```

```

### MiMo-V2-Flash

**Generation Time:** 14806ms
**Tokens:** 2141

```
Here is a complete implementation of an LRU cache with per-key TTL support in Python.

### Design Decisions

1.  **Data Structures**:
    *   **Doubly Linked List**: Used to maintain the LRU order. The head represents the most recently used item, and the tail represents the least recently used.
    *   **Hash Map (Dictionary)**: Maps keys to `Node` objects in the linked list for $O(1)$ access.
    *   **Sorted List (Heapq)**: Used to manage expiration times. We maintain a min-heap of `(expiry_time, key)` tuples to efficiently find the next expired item.

2.  **Thread Safety**:
    *   Uses a single `threading.RLock` (Reentrant Lock) to protect all internal state (list, map, and heap). This ensures that operations like `get` and `put` are atomic.

3.  **Lazy Expiration**:
    *   No background threads are used. Expiration is checked during `get`, `put`, and explicit eviction calls.
    *   To handle the complexity of arbitrary key removal (which is hard with a standard heap), we use a **lazy invalidation strategy** for the heap: when popping from the heap for eviction, we check if the key is still valid and not already expired.

4.  **Eviction Strategy**:
    *   **TTL Priority**: If an item is expired, it is evicted immediately, regardless of LRU status.
    *   **LRU Priority**: If the cache is full and no items are expired, the least recently used item is evicted.

### Implementation

```python
import threading
import time
import heapq
from collections import OrderedDict
from typing import Any, Optional, Tuple, Callable, Dict

class Node:
    """Doubly Linked List Node"""
    __slots__ = ('key', 'value', 'prev', 'next', 'expiry')
    
    def __init__(self, key: Any, value: Any, expiry: float):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.prev = None
        self.next = None

class LRUCacheTTL:
    def __init__(self, max_size: int, eviction_callback: Optional[Callable[[Any, Any], None]] = None):
        if max_size <=...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*