# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-131157
**Timestamp:** 2026-04-02T13:11:57.792015
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a production-ready circuit breaker pattern in Python. It should support three states (closed, open, half-open), configurable failure thresholds, automatic recovery with exponential backoff, proper async support, and metrics collection. Include usage example wrapping an HTTP client.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 7.44 | 5.00 | 9.15 | 1.31 |
| 2 | Gemini 3 Flash Preview | 7.03 | 5.30 | 9.60 | 1.42 |
| 3 | GPT-5.4 | 7.00 | 3.60 | 9.00 | 1.78 |
| 4 | Claude Opus 4.6 | 6.82 | 3.05 | 9.60 | 2.23 |
| 5 | MiMo-V2-Flash | 6.60 | 4.15 | 9.15 | 1.61 |
| 6 | DeepSeek V3 | 6.23 | 3.80 | 8.55 | 1.53 |
| 7 | GPT-OSS-120B | 5.90 | 2.80 | 7.85 | 1.61 |
| 8 | Claude Sonnet 4.6 | 5.84 | 3.05 | 8.60 | 1.86 |
| 9 | MiniMax M2.5 | 4.92 | 1.85 | 7.80 | 2.26 |
| 10 | Gemini 3.1 Pro | 3.23 | 0.65 | 8.40 | 2.42 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.29 |
| 2 | Gemini 3.1 Pro | 4.92 |
| 3 | GPT-OSS-120B | 4.99 |
| 4 | Claude Opus 4.6 | 5.11 |
| 5 | Grok 4.20 | 6.22 |
| 6 | Claude Sonnet 4.6 | 6.28 |
| 7 | MiniMax M2.5 | 6.81 |
| 8 | MiMo-V2-Flash | 7.56 |
| 9 | Gemini 3 Flash Preview | 7.69 |
| 10 | DeepSeek V3 | 8.75 |

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

**Generation Time:** 25111ms
**Tokens:** 2104

```
Below is a production-ready, async-friendly circuit breaker implementation in Python with:

- 3 states: `closed`, `open`, `half_open`
- Configurable failure threshold
- Automatic recovery with exponential backoff
- Proper async support
- Metrics collection
- Example usage wrapping an HTTP client (`httpx`)

It is designed to be practical, thread-safe for asyncio use, and extensible.

---

## Features

- **Closed**
  - Requests flow normally
  - Failures are counted
  - Once failure threshold is reached, breaker opens

- **Open**
  - Requests are rejected immediately
  - After recovery timeout expires, breaker transitions to half-open

- **Half-open**
  - Allows a limited number of test requests
  - If enough succeed, breaker closes
  - If one fails, breaker re-opens
  - Recovery timeout grows with exponential backoff after repeated failed recovery attempts

- **Metrics**
  - Total requests
  - Successes / failures
  - Rejections
  - State transitions
  - Consecutive failures
  - Timestamps

---

# Implementation

```python
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


class CircuitBreakerError(Exception):
    """Base circuit breaker exception."""


class CircuitBreakerOpenError(CircuitBreakerError):
    """Raised when the circuit is open and calls are rejected."""


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerMetrics:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    state_transitions: int = 0

    consecutive_failures: int = 0
    consecutive_successes: int = 0

    last_failure_ts: Optional[float] = None
    last_success_ts: Optional[float] = None
    last_rejected_ts: Optional[float] = None
    opened_at_ts: Optional[float] = None
    half_opened_at_ts: Op...
```

### Claude Opus 4.6

**Generation Time:** 28160ms
**Tokens:** 2114

```


# Production-Ready Circuit Breaker Pattern in Python

```python
"""
Production-ready Circuit Breaker Pattern implementation with:
- Three states: CLOSED, OPEN, HALF-OPEN
- Configurable failure thresholds and recovery timeouts
- Exponential backoff for recovery attempts
- Full async support
- Metrics collection and reporting
- Thread safety for sync usage
- Decorator and context manager interfaces
"""

from __future__ import annotations

import asyncio
import enum
import functools
import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import (
    Any,
    Awaitable,
    Callable,
    Deque,
    Dict,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

logger = logging.getLogger(__name__)


# ─── Exceptions ──────────────────────────────────────────────────────────────

class CircuitBreakerError(Exception):
    """Base exception for circuit breaker errors."""
    def __init__(self, circuit_breaker: "CircuitBreaker", *args: Any):
        super().__init__(*args)
        self.circuit_breaker = circuit_breaker


class CircuitOpenError(CircuitBreakerError):
    """Raised when a call is attempted while the circuit is OPEN."""
    def __init__(self, circuit_breaker: "CircuitBreaker", remaining_timeout: float):
        self.remaining_timeout = remaining_timeout
        super().__init__(
            circuit_breaker,
            f"Circuit '{circuit_breaker.name}' is OPEN. "
            f"Retry after {remaining_timeout:.1f}s",
        )


# ─── States ──────────────────────────────────────────────────────────────────

class CircuitState(enum.Enum):
    CLOSED = "closed"       # Normal operation — requests flow through
    OPEN = "open"           # Failing — requests are blocked
    HALF_OPEN = "half_open" # Testing — limited requests allowed through


# ─── Metrics ─────────────────────────────────────────────────────────────────

@dataclass
class CircuitBreakerMetrics:
    """Collects and reports c...
```

### Gemini 3.1 Pro

**Generation Time:** 29202ms
**Tokens:** 2096

```
Here is a production-ready asynchronous Circuit Breaker implementation in Python. 

It uses `asyncio`, features thread-safe state management (via asyncio Locks), exponential backoff, configurable exception handling, logging, and comprehensive metrics collection.

### 1. The Circuit Breaker Implementation (`circuit_breaker.py`)

```python
import asyncio
import functools
import logging
import time

```

### Claude Sonnet 4.6

**Generation Time:** 24862ms
**Tokens:** 2114

```
# Production-Ready Circuit Breaker Pattern in Python

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Circuit Breaker                        │
│                                                           │
│  CLOSED ──(failures >= threshold)──► OPEN                │
│     ▲                                  │                  │
│     │                           (timeout expires)         │
│     │                                  │                  │
│     └──(success)──── HALF-OPEN ◄───────┘                  │
│                          │                                │
│                    (failure)──► OPEN                      │
└─────────────────────────────────────────────────────────┘
```

## Implementation

### `circuit_breaker/state.py`
```python
"""Circuit breaker state definitions and transitions."""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation, requests pass through
    OPEN = "open"           # Failing, requests blocked
    HALF_OPEN = "half_open" # Testing recovery, limited requests


@dataclass
class CircuitSnapshot:
    """Immutable snapshot of circuit breaker state for metrics."""
    state: CircuitState
    failure_count: int
    success_count: int
    total_requests: int
    last_failure_time: Optional[datetime]
    last_success_time: Optional[datetime]
    last_state_change: datetime
    consecutive_successes: int
    consecutive_failures: int
    error_rate: float
    name: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_requests": self.total_requests,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else...
```

### Grok 4.20

**Generation Time:** 8135ms
**Tokens:** 2220

```
**Production-Ready Circuit Breaker in Python**

```python
from enum import Enum
from functools import wraps
from typing import Callable, TypeVar, Any, Dict, Optional
import asyncio
import time
import logging
from dataclasses import dataclass
from contextlib import contextmanager
import httpx
from datetime import datetime, timedelta

T = TypeVar('T')
logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Failing fast
    HALF_OPEN = "HALF_OPEN"  # Testing recovery


@dataclass
class CircuitMetrics:
    failures: int = 0
    successes: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    total_requests: int = 0
    blocked_requests: int = 0

    def record_failure(self):
        self.failures += 1
        self.total_requests += 1
        self.last_failure_time = time.time()

    def record_success(self):
        self.successes += 1
        self.total_requests += 1
        self.last_success_time = time.time()

    def record_blocked(self):
        self.blocked_requests += 1
        self.total_requests += 1


class CircuitBreaker:
    """
    Production-ready Circuit Breaker with async support and metrics.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        reset_timeout: float = 60.0,
        name: str = "default",
        exponential_backoff: bool = True,
        max_timeout: float = 300.0,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.reset_timeout = reset_timeout
        self.name = name
        self.exponential_backoff = exponential_backoff
        self.max_timeout = max_timeout

        self.state = CircuitState.CLOSED
        self.metrics = CircuitMetrics()
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.next_attempt_time: Optional[flo...
```

### DeepSeek V3

**Generation Time:** 85586ms
**Tokens:** 2102

```
# Production-Ready Circuit Breaker in Python

Here's a comprehensive implementation of the Circuit Breaker pattern in Python with all the requested features:

```python
import time
import math
import functools
from collections import deque
from typing import Callable, Optional, Any, Deque, Dict, Union
from datetime import datetime, timedelta
import logging
import asyncio
from contextlib import contextmanager

# Metrics collection interface
class CircuitBreakerMetrics:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.latency_metrics: Deque[float] = deque(maxlen=1000)
        self.state_changes: Deque[Dict[str, Any]] = deque(maxlen=100)

    def record_success(self, latency: float):
        self.success_count += 1
        self.latency_metrics.append(latency)

    def record_failure(self):
        self.failure_count += 1

    def record_state_change(self, from_state: str, to_state: str):
        self.state_changes.append({
            "timestamp": datetime.utcnow(),
            "from_state": from_state,
            "to_state": to_state
        })

    def get_stats(self) -> Dict[str, Any]:
        return {
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "current_error_rate": self.failure_count / max(1, self.success_count + self.failure_count),
            "recent_latency": {
                "avg": sum(self.latency_metrics) / len(self.latency_metrics) if self.latency_metrics else 0,
                "p90": sorted(self.latency_metrics)[int(len(self.latency_metrics) * 0.9)] if self.latency_metrics else 0,
                "max": max(self.latency_metrics) if self.latency_metrics else 0,
            } if self.latency_metrics else {},
            "state_changes": list(self.state_changes)
        }

# Main Circuit Breaker class
class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_threshold: int =...
```

### GPT-OSS-120B

**Generation Time:** 25899ms
**Tokens:** 2170

```
Below is a **fully‑featured, production‑ready circuit‑breaker implementation** that works for both **synchronous** and **asynchronous** code.  

It provides  

* three states – **CLOSED**, **OPEN**, **HALF‑OPEN**  
* configurable failure thresholds, success thresholds and recovery time‑outs  
* **exponential back‑off** while the breaker is OPEN  
* **thread‑/async‑safe** operation (uses `threading.Lock` for sync, `asyncio.Lock` for async)  
* built‑in **metrics** (calls, successes, failures, state‑changes, timings)  
* clear public API (`call`, `call_async`) and a custom `CircuitBreakerOpenError` exception  

The example at the end shows how to wrap an HTTP client (`requests` for sync, `aiohttp` for async) with the breaker.

---

## 1. Core implementation

```python
# circuit_breaker.py
from __future__ import annotations
import time
import math
import threading
import asyncio
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Callable, Awaitable, TypeVar, Generic, Optional, Any, Union

T = TypeVar("T")
R = TypeVar("R")

# --------------------------------------------------------------------------- #
#  Exceptions
# --------------------------------------------------------------------------- #
class CircuitBreakerError(RuntimeError):
    """Base class for circuit‑breaker related errors."""


class CircuitBreakerOpenError(CircuitBreakerError):
    """Raised when a call is attempted while the breaker is OPEN."""


# --------------------------------------------------------------------------- #
#  State & Config
# --------------------------------------------------------------------------- #
class State(Enum):
    CLOSED = auto()      # everything works, failures are counted
    OPEN = auto()        # calls are rejected, waiting for timeout
    HALF_OPEN = auto()   # a limited number of trial calls are allowed


@dataclass
class CircuitBreakerConfig:
    # How many *consecutive* failures trigger the OPEN state
    failure_threshold: int ...
```

### Gemini 3 Flash Preview

**Generation Time:** 11065ms
**Tokens:** 1662

```
This implementation follows the classic **Circuit Breaker** pattern (similar to Netflix's Hystrix or Resilience4j). It uses `asyncio` for non-blocking operations and includes a state machine to manage transitions.

### 1. The Circuit Breaker Implementation

```python
import asyncio
import time
import logging
from enum import Enum
from functools import wraps
from typing import Callable, Any, Optional

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CircuitBreaker")

class State(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Failing fast
    HALF_OPEN = "HALF_OPEN" # Testing recovery

class CircuitBreakerError(Exception):
    """Raised when the circuit is open."""
    pass

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 10.0,
        expected_exception: type = Exception,
        name: str = "default"
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.state = State.CLOSED
        self.failures = 0
        self.last_failure_time: Optional[float] = None
        
        # Metrics
        self.metrics = {"success": 0, "failure": 0, "reject": 0}

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        self._before_call()

        if self.state == State.OPEN:
            self.metrics["reject"] += 1
            raise CircuitBreakerError(f"Circuit '{self.name}' is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure(e)
            raise

    def _before_call(self):
        """Check if we should transition from OPEN to HALF_OPEN."""
        if self.state == State.OPEN and self.last_failure_time:
            # ...
```

### MiniMax M2.5

**Generation Time:** 84453ms
**Tokens:** 2136

```
Here is a production-ready implementation of the Circuit Breaker pattern in Python.

It includes:
1.  **Thread/Task Safety**: Uses `asyncio.Lock` to handle concurrent access.
2.  **State Management**: Closed, Open, and Half-Open states.
3.  **Exponential Backoff**: The recovery timeout increases if the service remains unstable.
4.  **Metrics**: Tracks successes, failures, rejections, and current state.
5.  **Decorators**: A clean `@circuit_breaker` decorator for easy integration.

### The Implementation

```python
import asyncio
import logging
import time
from enum import Enum
from functools import wraps
from typing import Any, Callable, Optional, Set, Type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("circuit_breaker")


class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerError(Exception):
    """Raised when the circuit breaker is open and rejecting requests."""
    def __init__(self, message: str, state: CircuitBreakerState):
        self.message = message
        self.state = state
        super().__init__(self.message)


class CircuitBreaker:
    """
    An asynchronous Circuit Breaker implementation.
    
    Attributes:
        failure_threshold: Number of failures to trigger opening the circuit.
        recovery_timeout: Initial time in seconds to wait before attempting recovery.
        backoff_factor: Multiplier for recovery_timeout after every failed retry in Half-Open.
        excluded_exceptions: Exceptions that should not count towards failure thresholds.
    """
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        backoff_factor: float = 1.5,
        excluded_exceptions: Optional[Set[Type[Exception]]] = None

```

### MiMo-V2-Flash

**Generation Time:** 22186ms
**Tokens:** 2135

```
Here is a production-ready implementation of the Circuit Breaker pattern in Python.

This implementation features:
1.  **Thread-Safe State Management**: Uses atomic operations for state transitions.
2.  **Async Support**: Native `async/await` support for non-blocking I/O.
3.  **Exponential Backoff**: Configurable delay before attempting a reset.
4.  **Metrics Collection**: Hooks for monitoring success/failure rates and state changes.
5.  **Configurable Thresholds**: Control failure counts and timeouts.

### The Circuit Breaker Implementation

```python
import asyncio
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Optional, Any, Dict
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(Enum):
    CLOSED = "CLOSED"      # Normal operation, requests pass through
    OPEN = "OPEN"          # Failing fast, requests blocked
    HALF_OPEN = "HALF_OPEN" # Testing if service recovered

@dataclass
class Metrics:
    """Container for circuit breaker metrics."""
    successes: int = 0
    failures: int = 0
    timeouts: int = 0
    state_changes: int = 0
    last_failure_time: Optional[float] = None
    
    def reset(self) -> None:
        self.successes = 0
        self.failures = 0
        self.timeouts = 0

class CircuitBreakerException(Exception):
    """Custom exception for circuit breaker rejections."""
    pass

class CircuitBreaker:
    """
    A production-ready circuit breaker implementation.
    
    Args:
        failure_threshold (int): Number of failures before opening the circuit.
        recovery_timeout (float): Time in seconds before attempting reset (exponential backoff base).
        expected_exception (Exception): Exception types to count as failures.
        half_open_max_calls (int): Number of successful calls in half-open state to close.
    """
    def __init__(
        self,
        name: str,
  ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*