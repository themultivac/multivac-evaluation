# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-124253
**Timestamp:** 2026-04-02T12:42:53.063531
**Category:** Code Generation
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
| 1 | Gemini 3 Flash Preview | 8.28 | 7.45 | 9.35 | 0.65 |
| 2 | Grok 4.20 | 7.94 | 5.40 | 9.35 | 1.22 |
| 3 | GPT-5.4 | 7.71 | 5.65 | 9.60 | 1.28 |
| 4 | MiMo-V2-Flash | 7.44 | 5.20 | 9.00 | 1.20 |
| 5 | Claude Opus 4.6 | 7.00 | 3.70 | 9.60 | 1.93 |
| 6 | GPT-OSS-120B | 6.87 | 3.05 | 9.20 | 1.89 |
| 7 | Claude Sonnet 4.6 | 6.82 | 4.05 | 8.80 | 1.74 |
| 8 | DeepSeek V3 | 6.81 | 4.80 | 9.15 | 1.40 |
| 9 | MiniMax M2.5 | 4.97 | 2.85 | 7.60 | 1.78 |
| 10 | Gemini 3.1 Pro | 3.12 | 0.85 | 8.40 | 2.45 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.28 |
| 2 | Claude Opus 4.6 | 5.91 |
| 3 | GPT-OSS-120B | 6.00 |
| 4 | MiniMax M2.5 | 6.22 |
| 5 | Gemini 3.1 Pro | 6.33 |
| 6 | Grok 4.20 | 6.59 |
| 7 | Claude Sonnet 4.6 | 7.01 |
| 8 | MiMo-V2-Flash | 7.54 |
| 9 | Gemini 3 Flash Preview | 8.27 |
| 10 | DeepSeek V3 | 8.62 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 87

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

**Generation Time:** 23670ms
**Tokens:** 2127

```
```python
"""
Production-ready API rate limiter using:
- Token bucket algorithm
- Per-API-key limits
- Redis backend for distributed environments
- Graceful degradation when Redis is unavailable
- Proper async support
- Comprehensive logging
- FastAPI middleware example

Requirements:
    pip install fastapi redis uvicorn

Notes:
- Uses redis.asyncio from redis-py.
- Includes local in-memory fallback when Redis is unavailable.
- Uses a Lua script for atomic Redis token bucket updates.
- Middleware reads API key from "X-API-Key" header by default.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Optional, Dict, Tuple, Callable, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

try:
    from redis.asyncio import Redis
    from redis.exceptions import RedisError
except ImportError:  # pragma: no cover
    Redis = None
    RedisError = Exception


# ------------------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------------------

logger = logging.getLogger("rate_limiter")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# ------------------------------------------------------------------------------
# Configuration models
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class RateLimitConfig:
    capacity: int
    refill_rate: float  # tokens per second

    def validate(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be > 0")
        if self.refill_rate <= 0:
            raise ValueError("refill_rate must be > 0")


@dataclass
class RateLimitRes...
```

### Claude Opus 4.6

**Generation Time:** 84274ms
**Tokens:** 2137

```


# Production-Ready API Rate Limiter

## Project Structure

```
rate_limiter/
├── __init__.py
├── core.py
├── backends/
│   ├── __init__.py
│   ├── base.py
│   ├── redis_backend.py
│   └── memory_backend.py
├── middleware.py
├── models.py
├── config.py
├── exceptions.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    ├── test_backends.py
    └── test_middleware.py
```

## Models and Configuration

```python
# rate_limiter/models.py
"""Data models for the rate limiter."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class RateLimitResult(Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    DEGRADED_ALLOWED = "degraded_allowed"  # Allowed due to graceful degradation


@dataclass(frozen=True)
class RateLimitPolicy:
    """Defines rate limiting parameters for a token bucket.
    
    Attributes:
        tokens_per_second: Rate at which tokens are added to the bucket.
        bucket_size: Maximum number of tokens the bucket can hold.
        tokens_per_request: Number of tokens consumed per request.
        name: Optional human-readable name for this policy.
    """
    tokens_per_second: float
    bucket_size: int
    tokens_per_request: int = 1
    name: str = "default"

    def __post_init__(self):
        if self.tokens_per_second <= 0:
            raise ValueError("tokens_per_second must be positive")
        if self.bucket_size <= 0:
            raise ValueError("bucket_size must be positive")
        if self.tokens_per_request <= 0:
            raise ValueError("tokens_per_request must be positive")
        if self.tokens_per_request > self.bucket_size:
            raise ValueError("tokens_per_request cannot exceed bucket_size")


@dataclass
class BucketState:
    """Represents the current state of a token bucket."""
    tokens: float
    last_refill_time: float
    
    @classmethod
    def new(cls, policy: RateLimitPolicy) -> "BucketState":
        """Create a new bucket state with full to...
```

### Gemini 3.1 Pro

**Generation Time:** 34349ms
**Tokens:** 2119

```
Here is a production-ready asynchronous API rate limiter implementing the Token Bucket algorithm. 

This solution uses **Redis** with a **Lua script** to ensure atomicity in a distributed environment. It includes a localized, thread-safe in-memory fallback to ensure **graceful degradation** if Redis goes down.

### 1. Prerequisites
```bash
pip install fastapi uvicorn
```

### Claude Sonnet 4.6

**Generation Time:** 27977ms
**Tokens:** 2136

```
# Production-Ready API Rate Limiter

## Project Structure
```
rate_limiter/
├── __init__.py
├── core.py          # Core token bucket implementation
├── backends.py      # Redis and fallback backends
├── middleware.py    # FastAPI middleware
├── config.py        # Configuration models
└── exceptions.py    # Custom exceptions
```

## Implementation

### `config.py` - Configuration Models

```python
"""Configuration models for the rate limiter."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RateLimitConfig:
    """Rate limit configuration for an API key or default policy."""
    
    # Tokens added per second
    refill_rate: float
    # Maximum tokens in the bucket
    capacity: int
    # Initial tokens (defaults to capacity if not set)
    initial_tokens: Optional[int] = None
    # Human-readable identifier for logging
    tier_name: str = "default"
    
    def __post_init__(self):
        if self.refill_rate <= 0:
            raise ValueError(f"refill_rate must be positive, got {self.refill_rate}")
        if self.capacity <= 0:
            raise ValueError(f"capacity must be positive, got {self.capacity}")
        if self.initial_tokens is None:
            self.initial_tokens = self.capacity
        if self.initial_tokens < 0:
            raise ValueError(f"initial_tokens must be non-negative, got {self.initial_tokens}")
    
    @classmethod
    def from_requests_per_minute(
        cls,
        rpm: int,
        burst_multiplier: float = 1.5,
        tier_name: str = "default"
    ) -> "RateLimitConfig":
        """Convenience constructor from requests-per-minute."""
        refill_rate = rpm / 60.0
        capacity = max(1, int(rpm * burst_multiplier / 60))
        return cls(
            refill_rate=refill_rate,
            capacity=capacity,
            tier_name=tier_name
        )
    
    @classmethod
    def from_requests_per_second(
        cls,
        rps: int,
        burst_multiplier: float = 1.5,
       ...
```

### Grok 4.20

**Generation Time:** 9018ms
**Tokens:** 2243

```
**✅ Production-Ready Token Bucket Rate Limiter**

```python
import asyncio
import time
import logging
from typing import Optional, Dict, Tuple, Callable, Any
from dataclasses import dataclass
from functools import wraps
from contextlib import asynccontextmanager

import redis.asyncio as redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# =============================================================================
# Logging
# =============================================================================

logger = logging.getLogger("rate_limiter")
logger.setLevel(logging.INFO)

@dataclass
class RateLimitConfig:
    """Rate limit configuration per API key or default"""
    requests: int      # e.g., 100
    window: int        # seconds, e.g., 60


class RateLimit:
    """Token bucket rate limiter with Redis + graceful degradation"""
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        default_limit: RateLimitConfig = RateLimitConfig(100, 60),
        redis_connect_timeout: float = 2.0,
        redis_command_timeout: float = 1.0,
        fallback_to_local: bool = True,
    ):
        self.default_limit = default_limit
        self.fallback_to_local = fallback_to_local
        self.redis_connect_timeout = redis_connect_timeout
        self.redis_command_timeout = redis_command_timeout
        
        self._redis: Optional[redis.Redis] = None
        self._redis_available = False
        self._local_buckets: Dict[str, Dict[str, float]] = {}  # api_key -> {tokens: float, last_refill: float}
        
        self.redis_url = redis_url
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize Redis connection"""
        if self._redis:
            return
        
        try:
            self._redis...
```

### DeepSeek V3

**Generation Time:** 44713ms
**Tokens:** 2126

```
# Production-Ready API Rate Limiter with Token Bucket Algorithm

Here's a complete implementation of a rate limiter that meets all your requirements:

```python
import asyncio
import logging
import time
from typing import Optional, Dict, Tuple
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    capacity: int  # Maximum tokens in the bucket
    refill_rate: float  # Tokens added per second
    key_prefix: str = "rl:"  # Prefix for Redis keys

class RateLimiter:
    def __init__(
        self,
        redis_client: Optional[redis.Redis] = None,
        default_config: Optional[RateLimitConfig] = None,
        redis_enabled: bool = True,
        cache: Optional[Dict[str, Tuple[float, float]]] = None
    ):
        """
        Initialize the rate limiter.
        
        Args:
            redis_client: Async Redis client
            default_config: Default rate limit config
            redis_enabled: Whether to use Redis (can be disabled for fallback)
            cache: Local cache dictionary for fallback mode
        """
        self.redis = redis_client
        self.default_config = default_config or RateLimitConfig(
            capacity=10,
            refill_rate=1
        )
        self.redis_enabled = redis_enabled
        self.local_cache = cache or {}
        self.local_cache_lock = asyncio.Lock()

    async def get_config_for_key(self, api_key: str) -> RateLimitConfig:
        """
        Retrieve rate limit configuration for an API key.
        In a r...
```

### GPT-OSS-120B

**Generation Time:** 40322ms
**Tokens:** 2175

```
Below is a **complete, production‑ready implementation** of an API rate‑limiter that satisfies every requirement you listed.

* **Token‑bucket algorithm** – each API‑key has its own bucket (`capacity`, `refill_rate`).  
* **Per‑key limits** – the limits are read from a configurable mapping (or a DB, etc.).  
* **Redis backend** – the bucket state lives in Redis and is updated atomically with a Lua script.  
* **Graceful degradation** – if Redis cannot be reached the limiter falls‑back to an in‑memory bucket (still thread‑safe).  
* **Async‑first** – everything is `async`/`await` and uses `redis.asyncio`.  
* **Comprehensive logging** – every decision, error and state change is logged with structured messages.  

The answer is split into three sections:

1. **`rate_limiter.py`** – the core `AsyncRateLimiter` class (Redis integration + in‑memory fallback).  
2. **`settings.py`** – a tiny `pydantic` settings container (helps with DI in FastAPI).  
3. **`fastapi_app.py`** – a FastAPI example that wires the limiter as a middleware.

---

## 1️⃣ `rate_limiter.py`

```python
"""
rate_limiter.py

Async token‑bucket rate limiter with Redis backend and in‑memory graceful fallback.
"""

import asyncio
import json
import logging
import time
from typing import Any, Callable, Dict, Optional, Tuple

import redis.asyncio as redis
from pydantic import BaseModel, Field, validator

# --------------------------------------------------------------------------- #
# Logging configuration (feel free to replace with structlog, loguru, etc.)
# --------------------------------------------------------------------------- #
logger = logging.getLogger("rate_limiter")
if not logger.handlers:
    # Basic configuration only runs once per interpreter session.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

# --------------------------------------------------------------------------- #
# Helper data structures
# -------------...
```

### Gemini 3 Flash Preview

**Generation Time:** 12020ms
**Tokens:** 1664

```
This implementation uses a **Token Bucket** algorithm with **Redis** as the distributed storage. It includes a "fail-open" mechanism for graceful degradation, atomic operations via Lua scripting, and a FastAPI middleware integration.

### 1. The Rate Limiter Core (Redis + Lua)

We use a Lua script to ensure atomicity. This prevents race conditions where two concurrent requests might read the same bucket state before updating it.

```python
import time
import logging
import asyncio
from typing import Optional, Tuple
from redis.asyncio import Redis, ConnectionError, TimeoutError

logger = logging.getLogger(__name__)

LUA_RATE_LIMITER = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local bucket = redis.call('hmget', key, 'tokens', 'last_updated')
local tokens = tonumber(bucket[1])
local last_updated = tonumber(bucket[2])

if tokens == nil then
    tokens = capacity
    last_updated = now
else
    local elapsed = math.max(0, now - last_updated)
    tokens = math.min(capacity, tokens + (elapsed * refill_rate))
end

local allowed = tokens >= requested
if allowed then
    tokens = tokens - requested
end

redis.call('hset', key, 'tokens', tokens, 'last_updated', now)
redis.call('expire', key, math.ceil(capacity / refill_rate))

return {allowed and 1 or 0, tokens}
"""

class RateLimiter:
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
        Checks if a request is allowed.
        Returns: (is_allowed, remaining_tokens)
        """
        try:
            if not self._lua_script:
                self._lua_script = self.redis.register_script(LUA_RATE_LIMITER)

            # result: [allowed_int, remaining_tokens]
    ...
```

### MiniMax M2.5

**Generation Time:** 35535ms
**Tokens:** 2162

```
Here is a production-ready implementation. It is modular, using a Lua script in Redis for atomic operations (crucial for distributed rate limiting), and includes graceful degradation logic.

### Prerequisites
You will need to install the following packages:
```bash
pip install fastapi uvicorn redis pydantic
```

### 1. Configuration (`config.py`)
We use Pydantic for settings management to keep configuration strict and separate from code.

```python
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Rate Limiter Defaults
    default_rate_limit: int = 100  # tokens
    default_time_window: int = 60  # seconds
    
    # Failover
    fail_open: bool = True  # If Redis fails, allow requests (True) or block (False)

    class Config:
        env_file = ".env"


settings = Settings()
```

### 2. Redis Storage & Token Bucket Logic (`storage.py`)
This module handles the Redis connection and the **Lua Script**. Using a Lua script is essential because standard Redis commands are not atomic. We need to check the token count, calculate the refill, and decrement the token in a single database transaction to prevent race conditions.

```python
import redis.asyncio as redis
from redis.asyncio import Redis
from typing import Optional
import logging
import json

from config import settings

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self._pool: Optional[redis.ConnectionPool] = None
        # Lua script for atomic Token Bucket algorithm
        self.token_bucket_script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local capacity = tonumber(ARGV[2])
        local rate = tonumber(ARGV[3]) -- Tokens per second
        
        local bucket = redis
```

### MiMo-V2-Flash

**Generation Time:** 18367ms
**Tokens:** 2159

```
Here is a production-ready implementation of a Token Bucket rate limiter. It includes the core logic, Redis integration with fallback, async support, logging, and a FastAPI middleware example.

### Architecture Overview

1.  **Token Bucket Algorithm**: Tokens are added to a bucket at a fixed rate. Requests consume tokens. If the bucket is empty, the request is rejected.
2.  **Redis Backend**: Uses atomic Lua scripts to ensure thread-safety and consistency in distributed environments.
3.  **Graceful Degradation**: If Redis is unreachable, the system logs the error and allows traffic (fail-open) or rejects it (fail-closed) depending on configuration. Here, we implement **fail-open** for availability.
4.  **Async Support**: Built on `asyncio` and `aioredis` (via `redis-py` async interface).

---

### Prerequisites

You will need the following Python packages:

```bash
pip install fastapi uvicorn redis pydantic-settings structlog
```

---

### 1. Configuration & Models

We use Pydantic for settings management and data modeling.

```python
# config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    # Fail-open (allow traffic) if Redis is down. Set to False to fail-closed (block traffic).
    rate_limiter_fail_open: bool = True 
    default_rate_limit_per_sec: float = 10.0

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. The Token Bucket Engine (Redis Lua Script)

We use a Lua script to execute the token bucket logic atomically within Redis. This prevents race conditions between multiple API instances.

**Lua Script Logic:**
1. Get current bucket state (tokens, last_refill_timestamp).
2. Calculate refill amount based on time elapsed.
3. Deduct cost for the current request.
4. Save new state.

```python
# lua_scripts.py

# KEYS[1]: Redis key for the bucket (e.g., "ratelimit:user123:endpoint")
# ARGV[1]: Refill rate (tokens per second)
# A...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*