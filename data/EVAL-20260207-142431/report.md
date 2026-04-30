# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-142431
**Timestamp:** 2026-02-07T14:24:31.149545
**Category:** Programming & Code
**Model Pool:** 10 code-optimized models

## Question

Implement a production-ready API rate limiter with the following requirements:
1. Token bucket algorithm
2. Support for different rate limits per API key
3. Redis backend for distributed systems
4. Graceful degradation when Redis is unavailable
5. Proper async support
6. Comprehensive logging

Include the main class, Redis integration, and a FastAPI middleware example.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.2-Codex | 9.16 | 8.60 | 9.80 | 0.48 |
| 2 | Gemini 3 Flash Preview | 9.09 | 8.60 | 9.80 | 0.49 |
| 3 | Grok Code Fast 1 | 8.99 | 8.20 | 9.80 | 0.64 |
| 4 | Grok 3 (Direct) | 8.00 | 6.75 | 9.35 | 0.84 |
| 5 | DeepSeek V3.2 | 7.48 | 5.65 | 8.80 | 1.02 |
| 6 | Claude Sonnet 4.5 | 6.91 | 3.05 | 9.60 | 1.85 |
| 7 | GLM 4.7 | 6.60 | 2.00 | 8.80 | 3.16 |
| 8 | MiniMax M2.1 | 6.50 | 2.00 | 8.80 | 3.09 |
| 9 | Claude Opus 4.5 | 6.26 | 2.85 | 8.60 | 2.17 |
| 10 | Gemini 3 Pro Preview | 4.17 | 2.45 | 6.10 | 1.27 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.2-Codex | 5.41 |
| 2 | Gemini 3 Pro Preview | 5.80 |
| 3 | Grok Code Fast 1 | 6.73 |
| 4 | GLM 4.7 | 7.04 |
| 5 | MiniMax M2.1 | 7.09 |
| 6 | Grok 3 (Direct) | 7.52 |
| 7 | Claude Opus 4.5 | 7.64 |
| 8 | Claude Sonnet 4.5 | 8.21 |
| 9 | DeepSeek V3.2 | 8.22 |
| 10 | Gemini 3 Flash Preview | 8.67 |

**Strictest Judge:** gpt_codex
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 76

---

## Model Pool

Models selected for **Programming & Code** evaluation:

1. **Grok Code Fast 1** (openrouter)
2. **Claude Opus 4.5** (openrouter)
3. **Gemini 3 Flash Preview** (openrouter)
4. **Claude Sonnet 4.5** (openrouter)
5. **Gemini 3 Pro Preview** (openrouter)
6. **MiniMax M2.1** (openrouter)
7. **GLM 4.7** (openrouter)
8. **DeepSeek V3.2** (openrouter)
9. **GPT-5.2-Codex** (openrouter)
10. **Grok 3 (Direct)** (xai)

---

## Model Responses

### Grok Code Fast 1

**Generation Time:** 14219ms
**Tokens:** 2838

```
Below is a complete, production-ready implementation of an API rate limiter in Python, adhering to the specified requirements. I'll explain the key design decisions and components before presenting the code.

### Key Design Decisions
- **Token Bucket Algorithm**: Implemented using a Lua script executed atomically in Redis. Each API key is associated with a Redis hash containing `tokens` (current token count) and `last_refill` (timestamp of last refill). On each request, tokens are refilled based on elapsed time, then checked and decremented if available.
- **Per-API-Key Rate Limits**: Rate limits (refill rate in tokens/second and burst capacity) are configurable per API key. Stored in a Redis hash for easy lookup and updates.
- **Redis Backend**: Uses `redis.asyncio` (aioredis) for asynchronous operations. Data is stored in Redis to support distributed systems (e.g., multiple server instances).
- **Graceful Degradation**: If Redis is unavailable (e.g., connection errors), the limiter allows all requests (defaults to no limiting) to avoid blocking the API. This is logged as a warning. In production, you could enhance this with a local in-memory fallback (e.g., using a dict with asyncio.Lock), but for simplicity, it falls back to allowing requests.
- **Async Support**: All operations are async, using `asyncio` and aioredis. The limiter can be awaited in async contexts.
- **Comprehensive Logging**: Uses Python's `logging` module. Logs include rate limit decisions, Redis errors, refills, and middleware actions at appropriate levels (INFO, WARNING, ERROR).
- **Performance and Scalability**: The Lua script ensures atomicity, preventing race conditions in distributed setups. Redis is efficient for this use case.
- **Dependencies**: Requires `redis[asyncio]`, `fastapi`, and `uvicorn` (for running the example). Install via `pip install redis fastapi uvicorn`.
- **Security Note**: API keys are assumed to be extracted from request headers (e.g., `X-API-Key`). In production, va...
```

### Claude Opus 4.5

**Generation Time:** 21347ms
**Tokens:** 2137

```
# Production-Ready API Rate Limiter

A comprehensive, production-ready rate limiter implementation using the token bucket algorithm with Redis backend, graceful degradation, and FastAPI integration.

## Project Structure

```
rate_limiter/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── token_bucket.py
│   ├── rate_limit_config.py
│   └── exceptions.py
├── backends/
│   ├── __init__.py
│   ├── base.py
│   ├── redis_backend.py
│   └── memory_backend.py
├── middleware/
│   ├── __init__.py
│   └── fastapi_middleware.py
├── utils/
│   ├── __init__.py
│   └── logging_config.py
└── tests/
    ├── __init__.py
    ├── test_token_bucket.py
    └── test_middleware.py
```

## Implementation

```python
# rate_limiter/__init__.py
"""
Production-Ready API Rate Limiter

A distributed rate limiting solution using the token bucket algorithm
with Redis backend and graceful degradation support.
"""

from .core.token_bucket import TokenBucket, RateLimiter
from .core.rate_limit_config import RateLimitConfig, RateLimitTier
from .core.exceptions import RateLimitExceeded, RateLimiterError
from .backends.redis_backend import RedisBackend
from .backends.memory_backend import MemoryBackend
from .middleware.fastapi_middleware import RateLimitMiddleware

__version__ = "1.0.0"
__all__ = [
    "TokenBucket",
    "RateLimiter", 
    "RateLimitConfig",
    "RateLimitTier",
    "RateLimitExceeded",
    "RateLimiterError",
    "RedisBackend",
    "MemoryBackend",
    "RateLimitMiddleware",
]
```

```python
# rate_limiter/core/exceptions.py
"""Custom exceptions for the rate limiter."""

from typing import Optional
from datetime import datetime


class RateLimiterError(Exception):
    """Base exception for rate limiter errors."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> dict:
        return ...
```

### Gemini 3 Flash Preview

**Generation Time:** 11754ms
**Tokens:** 1775

```
This implementation uses **Python 3.10+**, **FastAPI**, and **Redis-py**. It follows a "fail-open" strategy for graceful degradation, ensuring your API stays up even if Redis goes down.

### 1. The Rate Limiter Core (Token Bucket)

We use a Lua script to ensure atomicity. This prevents "check-then-set" race conditions in a distributed environment.

```python
import time
import logging
import asyncio
from typing import Optional, Tuple
from redis.asyncio import Redis, ConnectionError, TimeoutError

logger = logging.getLogger(__name__)

LUA_TOKEN_BUCKET = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- Get bucket state
local bucket = redis.call("HMGET", key, "tokens", "last_updated")
local tokens = tonumber(bucket[1]) or capacity
local last_updated = tonumber(bucket[2]) or now

-- Refill tokens based on time passed
local elapsed = math.max(0, now - last_updated)
local refill = elapsed * refill_rate
tokens = math.min(capacity, tokens + refill)

-- Check if enough tokens
local allowed = tokens >= requested
if allowed then
    tokens = tokens - requested
end

-- Save state
redis.call("HMSET", key, "tokens", tokens, "last_updated", now)
redis.call("EXPIRE", key, 600) -- TTL to cleanup unused keys

return {allowed and 1 or 0, tokens}
"""

class TokenBucketRateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self._lua_script = None

    async def is_allowed(
        self, 
        key: str, 
        capacity: int, 
        refill_rate: float, 
        requested: int = 1
    ) -> Tuple[bool, float]:
        """
        Returns (is_allowed, remaining_tokens).
        Defaults to True if Redis is unavailable (Fail-Open).
        """
        try:
            if not self._lua_script:
                self._lua_script = self.redis.register_script(LUA_TOKEN_BUCKET)

            now = time.time()
            # result: [a...
```

### Claude Sonnet 4.5

**Generation Time:** 24518ms
**Tokens:** 2137

```
```python
import asyncio
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import json

import redis.asyncio as aioredis
from redis.asyncio import Redis
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimitTier(Enum):
    """Rate limit tiers for different API key types"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    capacity: int  # Maximum number of tokens
    refill_rate: float  # Tokens added per second
    tier: RateLimitTier
    
    @classmethod
    def from_tier(cls, tier: RateLimitTier) -> 'RateLimitConfig':
        """Create configuration based on tier"""
        configs = {
            RateLimitTier.FREE: cls(capacity=100, refill_rate=10, tier=tier),
            RateLimitTier.BASIC: cls(capacity=1000, refill_rate=50, tier=tier),
            RateLimitTier.PREMIUM: cls(capacity=5000, refill_rate=200, tier=tier),
            RateLimitTier.ENTERPRISE: cls(capacity=50000, refill_rate=1000, tier=tier),
        }
        return configs[tier]


@dataclass
class TokenBucketState:
    """State of a token bucket"""
    tokens: float
    last_refill: float
    capacity: int
    refill_rate: float


class LocalTokenBucket:
    """In-memory fallback token bucket implementation"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()
...
```

### Gemini 3 Pro Preview

**Generation Time:** 20950ms
**Tokens:** 2118

```
Here is a complete, production-ready implementation of a Distributed Token Bucket Rate Limiter using Python, Redis, and FastAPI.

### Prerequisites

You will need the following dependencies:
```bash
pip install fastapi uvicorn redis
```

### 1. The Core Rate Limiter Class

This class handles the communication with Redis and executes a Lua script to ensure atomicity. Atomicity is crucial here so that two concurrent requests don't calculate the token refill incorrectly.

```python
import logging
import time
from typing import Tuple, Optional
import redis.asyncio as redis
from redis.exceptions import RedisError

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RateLimiter")

class DistributedRateLimiter:
    """
    Async Distributed Rate Limiter using the Token Bucket algorithm.
    """
    
    # Lua script for atomic Token Bucket operations in Redis
    # ARGV[1]: Refill rate (tokens per second)
    # ARGV[2]: Capacity (max tokens)
    # ARGV[3]: Current timestamp
    # ARGV[4]: Requested tokens (cost)
    # KEYS[1]: Unique key for the user/IP
    LUA_SCRIPT = """
    local key = KEYS[1]
    local rate = tonumber(ARGV[1])
    local capacity = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    local requested = tonumber(ARGV[4])

    -- Retrieve current state
    local state = redis.call('HMGET', key, 'tokens', 'last_updated')
    local tokens = tonumber(state[1])
    local last_updated = tonumber(state[2])

    -- Initialize if missing
    if not tokens then
        tokens = capacity
        last_updated = now
    end

    -- Calculate refill
    local delta =
```

### MiniMax M2.1

**Generation Time:** 24668ms
**Tokens:** 2164

```

```

### GLM 4.7

**Generation Time:** 30901ms
**Tokens:** 2127

```

```

### DeepSeek V3.2

**Generation Time:** 122686ms
**Tokens:** 2126

```
Here's a production-ready API rate limiter implementation with all your requirements:

## 1. Core Rate Limiter Class

```python
# rate_limiter.py
import asyncio
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from contextlib import asynccontextmanager
from functools import wraps

logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting per API key"""
    requests_per_second: float
    burst_capacity: int
    enabled: bool = True

class RateLimiterError(Exception):
    """Base exception for rate limiter errors"""
    pass

class TokenBucket:
    """Token bucket algorithm implementation"""
    
    def __init__(self, capacity: float, refill_rate: float):
        """
        Args:
            capacity: Maximum number of tokens the bucket can hold
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def consume(self, tokens: float = 1.0) -> bool:
        """
        Try to consume tokens from the bucket.
        Returns True if tokens were consumed, False otherwise.
        """
        async with self._lock:
            # Refill tokens based on elapsed time
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(
                self.capacity,
                self.tokens + (elapsed * self.refill_rate)
            )
            self.last_refill = now
            
            # Check if we have enough tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    async def get_wait_time(self, tokens: float = 1.0) -> float:
        """
        Calculate how long to wait before tokens will be available.
        Returns 0 if tokens are...
```

### GPT-5.2-Codex

**Generation Time:** 25522ms
**Tokens:** 1987

```
Below is a **production‑ready, async, Redis‑backed token bucket rate limiter** with:

✅ Token bucket algorithm  
✅ Different rate limits per API key  
✅ Redis for distributed systems  
✅ Graceful degradation when Redis is unavailable  
✅ Proper async support  
✅ Comprehensive logging  

It includes:

- **Core rate limiter class**
- **Redis integration (Lua script)**
- **FastAPI middleware example**

---

## ✅ Core Implementation (Token Bucket + Redis + Fallback)

```python
import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

import redis.asyncio as redis  # `pip install redis>=4.2`

logger = logging.getLogger("rate_limiter")
logger.setLevel(logging.INFO)


@dataclass(frozen=True)
class RateLimit:
    capacity: int         # max tokens in bucket
    refill_rate: float    # tokens per second


class LocalTokenBucket:
    """In‑memory fallback bucket per process."""
    def __init__(self):
        self._buckets: Dict[str, Tuple[float, float]] = {}
        self._lock = asyncio.Lock()

    async def allow(self, key: str, limit: RateLimit, cost: int = 1) -> bool:
        async with self._lock:
            now = time.time()
            tokens, ts = self._buckets.get(key, (limit.capacity, now))
            # refill
            delta = max(0, now - ts)
            tokens = min(limit.capacity, tokens + delta * limit.refill_rate)
            allowed = tokens >= cost
            if allowed:
                tokens -= cost
            self._buckets[key] = (tokens, now)
            return allowed


class RedisTokenBucket:
    """Redis-based token bucket (atomic via Lua)."""
    LUA_SCRIPT = """
    local key = KEYS[1]
    local rate = tonumber(ARGV[1])
    local cap = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    local cost = tonumber(ARGV[4])

    local data = redis.call("HMGET", key, "tokens", "ts")
    local tokens = tonumber(data[1]) or cap
    local ts = tonumber(data[2]) or now

    local de...
```

### Grok 3 (Direct)

**Generation Time:** 19636ms
**Tokens:** 1880

```
I'll implement a production-ready API rate limiter using the token bucket algorithm with all the specified requirements. The implementation will be split into multiple components for better organization and maintainability.

```python
# rate_limiter.py
import time
import redis
import logging
import json
from typing import Optional, Dict
from dataclasses import dataclass
from asyncio import Lock
from contextlib import AsyncExitStack, asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    tokens: int  # bucket capacity
    refill_rate: float  # tokens per second

class RateLimiter:
    def __init__(
        self,
        redis_host: str = 'localhost',
        redis_port: int = 6379,
        redis_db: int = 0,
        default_config: RateLimitConfig = RateLimitConfig(tokens=10, refill_rate=1.0)
    ):
        self.default_config = default_config
        self.locks: Dict[str, Lock] = {}
        self._redis_client = None
        self._redis_params = {
            'host': redis_host,
            'port': redis_port,
            'db': redis_db,
            'decode_responses': True
        }
        self._fallback_storage: Dict[str, dict] = {}  # In-memory fallback
        
        try:
            self._redis_client = redis.Redis(**self._redis_params)
            self._redis_client.ping()
            logger.info("Successfully connected to Redis")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.warning("Falling back to in-memory storage")

    async def get_lock(self, api_key: str) -> Lock:
        if api_key not in self.locks:
            self.locks[api_key] = Lock()
        return self.locks[api_key]

    async def get_bucket(self, api_key: str) -> dict:
        """Get or initialize bucket data for an API key"""
        try:
  ...
```

---

*Generated by The Multivac V5*
*https://multivac.com*