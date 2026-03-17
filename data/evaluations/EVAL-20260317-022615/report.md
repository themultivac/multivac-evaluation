# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260317-022615
**Timestamp:** 2026-03-17T02:26:15.283017
**Category:** Project Qwen
**Model Pool:** 8 qwen-optimized models

## Question

Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Qwen 3.5 35B-A3B | 7.83 | 6.15 | 9.60 | 1.54 |
| 2 | Qwen 3 Coder Next | 7.44 | 7.00 | 8.60 | 0.61 |
| 3 | Qwen 3 8B | 7.22 | 4.80 | 8.80 | 1.55 |
| 4 | Qwen 3.5 397B-A17B | 6.47 | 4.20 | 9.00 | 2.02 |
| 5 | Qwen 3.5 122B-A10B | 6.18 | 4.40 | 7.80 | 1.29 |
| 6 | Qwen 3.5 9B | 4.62 | 2.45 | 6.85 | 1.74 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Qwen 3.5 397B-A17B | 4.45 |
| 2 | Qwen 3.5 27B | 5.22 |
| 3 | Qwen 3.5 35B-A3B | 5.41 |
| 4 | Qwen 3.5 122B-A10B | 6.47 |
| 5 | Qwen 3.5 9B | 6.71 |
| 6 | Qwen 3 32B | 7.43 |
| 7 | Qwen 3 8B | 7.94 |
| 8 | Qwen 3 Coder Next | 8.28 |

**Strictest Judge:** qwen35_397b_a17b
**Most Lenient Judge:** qwen3_coder_next
**Total Judgments:** 64
**Valid Judgments:** 37

---

## Model Pool

Models selected for **Project Qwen** evaluation:

1. **Qwen 3.5 9B** (openrouter)
2. **Qwen 3 8B** (openrouter)
3. **Qwen 3 32B** (openrouter)
4. **Qwen 3 Coder Next** (openrouter)
5. **Qwen 3.5 35B-A3B** (openrouter)
6. **Qwen 3.5 27B** (openrouter)
7. **Qwen 3.5 122B-A10B** (openrouter)
8. **Qwen 3.5 397B-A17B** (openrouter)

---

## Model Responses

### Qwen 3.5 9B

**Generation Time:** 47320ms
**Tokens:** 2114

```
# LRU Cache with Per-Key TTL

Below is a complete implementation of a thread-safe LRU cache with per-key TTL support, including eviction callbacks, lazy expiration, and cache statistics. It also includes comprehensive unit tests.

```python
import time
import threading
from typing import Any, Callable, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import OrderedDict

@dataclass
class CacheEntry:
    key: str
    value: Any
    timestamp: float
    ttl: Optional[float]
    node: 'CacheNode'

@dataclass
class CacheNode:
    key: str
    value: Any
    timestamp: float
    ttl: Optional[float]
    next_node: Optional['CacheNode'] = None
    prev_node: Optional['CacheNode'] = None

class LRUCache:
    def __init__(
        self,
        max_size: int = 100,
        eviction_callback: Optional[Callable[[str, Any], None]] = None
    ):
        self.max_size = max_size
        self.eviction_callback = eviction_callback
        self.lock = threading.RLock()
        self.cache: Dict[str, CacheEntry] = {}
        self.head: Optional[CacheNode] = None  # Most recently used
        self.tail: Optional[CacheNode] = None  # Least recently used
        self.hits = 0
        self.misses = 0

    def _is_expired(self, node: CacheNode) -> bool:
        return node.ttl is not None and time.time() > (node.timestamp + node.ttl)

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None

            entry = self.cache[key]
            node = entry.node

            if self._is_expired(node):
                del self.cache[key]
                self.misses += 1
                return None

            self._move_to_head(node)
            self.hits += 1
            return node.value

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        with self.lock:
            if key in self.cache:
                entry = self.cache[key...
```

### Qwen 3 8B

**Generation Time:** 205347ms
**Tokens:** 10611

```
# LRU Cache with Per-Key TTL and Thread Safety

Below is a comprehensive implementation of an LRU cache with per-key TTL (Time-to-Live) support, satisfying all the specified requirements:

---

## ✅ Features Implemented

- **O(1) get/put operations** using a doubly linked list + hash map.
- **Thread-safe** using `ReentrantLock`.
- **Lazy expiration** (checked at access time, no background threads).
- **Configurable max size**.
- **Eviction callback** with support for cleanup.
- **Hit/miss statistics** tracking.
- **Per-key TTL** support.
- **Comprehensive unit tests**.

---

## 📦 Code Implementation

```java
import java.util.*;
import java.util.concurrent.locks.ReentrantLock;

public class LRUCache<K, V> {
    private final int maxSize;
    private final Map<K, Node<K, V>> map;
    private final Node<K, V> head;
    private final Node<K, V> tail;
    private final ReentrantLock lock;
    private long hitCount;
    private long missCount;
    private Consumer<CacheEntry<K, V>> evictionCallback;

    public LRUCache(int maxSize) {
        if (maxSize <= 0) throw new IllegalArgumentException("Max size must be positive.");
        this.maxSize = maxSize;
        this.map = new HashMap<>();
        this.head = new Node<>();
        this.tail = new Node<>();
        head.next = tail;
        tail.prev = head;
        this.lock = new ReentrantLock();
        this.hitCount = 0;
        this.missCount = 0;
        this.evictionCallback = null;
    }

    public void put(K key, V value, long ttl) {
        lock.lock();
        try {
            Node<K, V> node = map.get(key);
            if (node != null) {
                if (node.expiration <= System.currentTimeMillis()) {
                    removeNode(node);
                    if (evictionCallback != null) {
                        evictionCallback.accept(new CacheEntry<>(key, value));
                    }
                } else {
                    node.value = value;
                    node.expiration = (ttl == 0) ?...
```

### Qwen 3 32B

**Generation Time:** 23782ms
**Tokens:** 2113

```

```

### Qwen 3 Coder Next

**Generation Time:** 18003ms
**Tokens:** 2112

```
Here's a comprehensive implementation of an LRU Cache with per-key TTL, thread-safety, and all requested features.

### Implementation (`lru_cache_ttl.py`)

```python
import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable, Tuple, Dict
import unittest


class LRUCacheWithTTL:
    """
    Thread-safe LRU Cache with per-key TTL support.
    
    Features:
    - O(1) average get/put operations
    - Per-key configurable TTL
    - Lazy expiration (no background threads)
    - Configurable max size with LRU eviction
    - Optional eviction callback
    - Cache hit/miss statistics
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: Optional[float] = None,
        eviction_callback: Optional[Callable[[Any, Any], None]] = None,
    ):
        """
        Initialize the LRU cache.
        
        Args:
            max_size: Maximum number of items in the cache
            default_ttl: Default TTL in seconds (None = no expiration)
            eviction_callback: Optional callback(evicted_key, evicted_value) called when items are evicted
        """
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        if default_ttl is not None and default_ttl < 0:
            raise ValueError("default_ttl must be non-negative")
            
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._eviction_callback = eviction_callback
        
        # OrderedDict maintains insertion order; we'll use move_to_end() for LRU
        self._cache: OrderedDict = OrderedDict()
        
        # Store expiration times: key -> expiration_timestamp (or None for no TTL)
        self._expiration: Dict[Any, float] = {}
        
        # Statistics
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
        
        # Thread safety
        self._lock = threading.RLock()
        
    def ...
```

### Qwen 3.5 35B-A3B

**Generation Time:** 31048ms
**Tokens:** 5379

```
Here's a complete, production-ready implementation of a thread-safe LRU cache with per-key TTL support, lazy expiration, eviction callbacks, configurable max size, and hit/miss statistics. It includes comprehensive unit tests to validate functionality and concurrency.

---

### ✅ Core Features

- **LRU Eviction**: Least Recently Used policy with O(1) get/put
- **Per-Key TTL**: Optional expiration time for each key
- **Lazy Expiration**: Checked on access, no background threads
- **Thread Safety**: Uses `threading.RLock`
- **Eviction Callback**: Invoked when entries are evicted
- **Statistics**: Tracks hits, misses, evictions, and hit rate
- **Mock Clock Support**: For deterministic testing of TTL behavior

---

### 🔧 Implementation

```python
import threading
import time
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass

class CacheStats:
    """Thread-safe cache statistics tracker"""
    def __init__(self):
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._lock = threading.Lock()

    def record_hit(self):
        with self._lock:
            self._hits += 1

    def record_miss(self):
        with self._lock:
            self._misses += 1

    def record_eviction(self):
        with self._lock:
            self._evictions += 1

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
    def hit_rate(self) -> float:
        with self._lock:
            total = self._hits + self._misses
            return self._hits / total if total > 0 else 0.0

    def reset(self):
        with self._lock:
            self._hits = 0
            self._misses = 0
            self._evictions = 0


@dataclass
class CacheNode:
    key: Any
    value: Any
 ...
```

### Qwen 3.5 27B

**Generation Time:** 25813ms
**Tokens:** 2114

```

```

### Qwen 3.5 122B-A10B

**Generation Time:** 25799ms
**Tokens:** 2114

```
Here's a complete, production-ready implementation of a thread-safe LRU cache with per-key TTL support, lazy expiration, eviction callbacks, and hit/miss statistics. It includes comprehensive unit tests to ensure correctness and robustness.

---

## 🧠 Implementation

```python
import time
import threading
from typing import Any, Callable, Dict, Optional, TypeVar
from dataclasses import dataclass

K = TypeVar('K')
V = TypeVar('V')


@dataclass
class CacheEntry:
    value: V
    expiry_time: float
    ttl: Optional[float] = None


class LRUCache:
    def __init__(
        self,
        max_size: int,
        default_ttl: Optional[float] = None,
        eviction_callback: Optional[Callable[[K, V], None]] = None,
    ):
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.eviction_callback = eviction_callback

        self._cache: Dict[K, CacheEntry] = {}
        self._access_order: list[K] = []
        self._lock = RLock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'expirations': 0,
            'size': 0,
        }

    def get(self, key: K, ttl: Optional[float] = None) -> Optional[V]:
        with self._lock:
            self._stats['size'] = len(self._cache)
            if key not in self._cache:
                self._stats['misses'] += 1
                return None

            entry = self._cache[key]
            if time.time() > entry.expiry_time:
                del self._cache[key]
                self._access_order.remove(key)
                if self.eviction_callback:
                    self.eviction_callback(key, entry.value)
                self._stats['expirations'] += 1
                self._stats['size'] = len(self._cache)
                self._stats['misses'] += 1
                return None

            self._access_order.remove(key)
            self._access_order.append...
```

### Qwen 3.5 397B-A17B

**Generation Time:** 38272ms
**Tokens:** 2581

```
# LRU Cache with Per-Key TTL Support

A production-ready, thread-safe LRU cache implementation with per-key TTL, lazy expiration, eviction callbacks, and cache statistics.

## Implementation (Python)

```python
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Tuple
from enum import Enum


class EvictionReason(Enum):
    SIZE = "size_limit"
    EXPIRED = "expired"
    REMOVED = "removed"
    CLEARED = "cleared"


@dataclass
class CacheEntry:
    """Represents a single cache entry with metadata."""
    key: Any
    value: Any
    expiration_time: float
    created_at: float = field(default_factory=time.time)
    
    def is_expired(self) -> bool:
        return time.time() > self.expiration_time
    
    def ttl_remaining(self) -> float:
        return max(0, self.expiration_time - time.time())


@dataclass
class CacheStats:
    """Cache statistics container."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'expirations': self.expirations,
            'hit_rate': self.hit_rate,
            'total_requests': self.hits + self.misses
        }


class LRUCacheWithTTL:
    """
    Thread-safe LRU cache with per-key TTL support.
    
    Features:
    - O(1) get/put operations
    - Per-key TTL with lazy expiration
    - Configurable max size
    - Eviction callbacks
    - Cache hit/miss statistics
    - Thread-safe with read/write locks
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: Optional[float] = None,
        eviction_callback: Optional[Callable[[Any, ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*