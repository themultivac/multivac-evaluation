# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-151320
**Timestamp:** 2026-04-02T15:13:20.331062
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Build a simple but production-worthy task queue in Python with: async worker pool, retry with exponential backoff, dead letter queue for failed tasks, priority levels, task deduplication, and graceful shutdown. Use only asyncio and standard library (no Celery/RQ). Include a demonstration with 3 worker types.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 7.96 | 5.50 | 9.55 | 1.20 |
| 2 | Gemini 3 Flash Preview | 7.67 | 6.20 | 8.80 | 1.06 |
| 3 | DeepSeek V3 | 7.38 | 6.35 | 9.35 | 1.05 |
| 4 | Claude Sonnet 4.6 | 6.97 | 4.70 | 9.60 | 2.03 |
| 5 | MiMo-V2-Flash | 6.93 | 4.40 | 9.15 | 1.69 |
| 6 | GPT-OSS-120B | 6.85 | 3.65 | 9.20 | 1.99 |
| 7 | Claude Opus 4.6 | 6.78 | 2.05 | 9.00 | 2.24 |
| 8 | GPT-5.4 | 6.64 | 3.40 | 9.00 | 1.83 |
| 9 | MiniMax M2.5 | 2.14 | 0.40 | 4.30 | 1.37 |
| 10 | Gemini 3.1 Pro | 1.90 | 0.25 | 6.00 | 1.74 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.82 |
| 2 | Gemini 3.1 Pro | 5.35 |
| 3 | Claude Opus 4.6 | 5.44 |
| 4 | GPT-OSS-120B | 5.54 |
| 5 | Grok 4.20 | 5.83 |
| 6 | Claude Sonnet 4.6 | 6.18 |
| 7 | MiniMax M2.5 | 6.59 |
| 8 | MiMo-V2-Flash | 7.45 |
| 9 | Gemini 3 Flash Preview | 7.64 |
| 10 | DeepSeek V3 | 8.47 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 27427ms
**Tokens:** 2117

```
Below is a simple but production-worthy in-process async task queue using only `asyncio` and the Python standard library.

It includes:

- Async worker pool
- Retry with exponential backoff
- Dead letter queue
- Priority levels
- Task deduplication
- Graceful shutdown
- Demonstration with 3 worker types

It is designed as a solid foundation, not a distributed queue like Celery.

---

# Features and design

## What this queue does

- Accepts tasks with:
  - type
  - payload
  - priority
  - retry policy
  - optional deduplication key
- Dispatches tasks to registered async handlers
- Runs tasks concurrently with a worker pool
- Retries failures using exponential backoff
- Moves permanently failed tasks to a dead letter queue
- Prevents duplicate tasks from being enqueued while pending/running
- Shuts down gracefully:
  - stops accepting new tasks
  - lets in-flight tasks finish
  - cancels scheduler/worker loops cleanly

## What this queue does not do

- Durable persistence across process restarts
- Multi-process / distributed coordination
- Exactly-once semantics
- External broker integration

For true distributed production systems, you’d add persistence and coordination. But for an in-process service, this is practical and robust.

---

# Complete implementation

```python
import asyncio
import heapq
import itertools
import logging
import random
import signal
import time
import uuid
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
)
logger = logging.getLogger("taskqueue")


# -----------------------------------------------------------------------------
# Priority
# ---------------------------------------------------...
```

### Claude Opus 4.6

**Generation Time:** 41478ms
**Tokens:** 2125

```


# Production-Ready Async Task Queue in Python

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Task Queue System                       │
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────┐  │
│  │ Producer  │───▶│ Priority     │───▶│ Worker Pool       │  │
│  │          │    │ Queue        │    │  ┌─────────────┐  │  │
│  └──────────┘    │ (heapq)      │    │  │ Worker 1    │  │  │
│                  │              │    │  │ Worker 2    │  │  │
│  ┌──────────┐    │ Dedup Filter │    │  │ Worker 3    │  │  │
│  │ Retry    │───▶│              │    │  │ ...         │  │  │
│  │ Scheduler│    └──────────────┘    │  └─────────────┘  │  │
│  └──────────┘                        └───────┬───────────┘  │
│       ▲                                      │              │
│       │          ┌──────────────┐             │              │
│       └──────────│ Failed Task  │◀────────────┘              │
│                  └──────┬───────┘                            │
│                         │ max retries exceeded               │
│                         ▼                                    │
│                  ┌──────────────┐                            │
│                  │ Dead Letter  │                            │
│                  │ Queue        │                            │
│                  └──────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## Complete Implementation

```python
"""
Production-Ready Async Task Queue
==================================
Features:
  - Async worker pool with configurable concurrency
  - Retry with exponential backoff (jitter included)
  - Dead letter queue for permanently failed tasks
  - Priority levels (CRITICAL, HIGH, NORMAL, LOW)
  - Task deduplication via content-based hashing
  - Graceful shutdown with in-flight task completion
  -...
```

### Gemini 3.1 Pro

**Generation Time:** 40708ms
**Tokens:** 2107

```
1
        self.all_done.clear()

        # on success/dlq:
        self.in_flight -= 1
        if self.in_flight == 0:
            self.all_done.set()
        ```
        Then `shutdown()` awaits `self.all_done.wait()`. This perfectly handles tasks sleeping in back
```

### Claude Sonnet 4.6

**Generation Time:** 23497ms
**Tokens:** 2125

```
# Production-Worthy Async Task Queue in Python

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Task Queue System                        │
│                                                             │
│  Producers → Priority Queue → Worker Pool → Results        │
│                    ↓                ↓                       │
│             Deduplication     Retry Logic                   │
│                              (Exp. Backoff)                 │
│                                   ↓                        │
│                          Dead Letter Queue                  │
└─────────────────────────────────────────────────────────────┘
```

## Complete Implementation

```python
"""
production_task_queue.py

A production-worthy async task queue with:
- Async worker pool
- Priority levels (1=highest, 10=lowest)
- Retry with exponential backoff
- Dead letter queue for permanently failed tasks
- Task deduplication
- Graceful shutdown
- Metrics & monitoring
"""

import asyncio
import hashlib
import json
import logging
import signal
import time
import traceback
import uuid
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

# ─────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("taskqueue")


# ─────────────────────────────────────────────
# Constants & Enums
# ─────────────────────────────────────────────
class Priority(IntEnum):
    CRITICAL = 1
    HIGH = 3
    NORMAL = 5
    LOW = 7
    BACKGROUND = 10


class TaskStatus(str):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    DEAD = "dead"
    DUPLICATE = "duplicate"


# ────────────────────────────────...
```

### Grok 4.20

**Generation Time:** 10504ms
**Tokens:** 2233

```
**Here's a production-worthy async task queue** using only `asyncio` and the standard library:

```python
import asyncio
import json
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any, Awaitable, Callable, Dict, Optional, Set

class Priority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass(order=True)
class Task:
    priority: int
    scheduled_at: float
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    retries: int = 0
    max_retries: int = 3
    backoff_factor: float = 2.0
    created_at: float = field(default_factory=time.time)

    def __post_init__(self):
        if isinstance(self.priority, Priority):
            self.priority = self.priority.value


class DeadLetterQueue:
    def __init__(self, max_size: int = 1000):
        self.queue: deque[Task] = deque(maxlen=max_size)
        self.failed_counts: Dict[str, int] = defaultdict(int)

    def add(self, task: Task, error: Exception):
        self.queue.append(task)
        self.failed_counts[task.name] += 1
        print(f"♻️  Task {task.task_id} moved to DLQ after {task.retries} failures. "
              f"Error: {type(error).__name__}: {error}")

    def stats(self):
        return {
            "total_dead": len(self.queue),
            "by_task_type": dict(self.failed_counts)
        }


class TaskQueue:
    def __init__(self, num_workers: int = 5, dlq_max_size: int = 1000):
        self.num_workers = num_workers
        self.workers: Set[asyncio.Task] = set()
        self.running = False
        self._shutdown_event = asyncio.Event()

        # Priority queues (higher number = higher priority)
        self.queues: Dict[int, deque[Task]] = defaultdict(deque)
        self.lock = asyncio.Lock()
        
        #...
```

### DeepSeek V3

**Generation Time:** 108551ms
**Tokens:** 2758

```
# Asynchronous Task Queue with Worker Pool

Here's a production-worthy task queue implementation using only Python's asyncio and standard library. This solution includes all requested features.

```python
import asyncio
import time
import uuid
import heapq
import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple, Deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Priority(IntEnum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2


@dataclass(order=True)
class PrioritizedItem:
    priority: Priority
    timestamp: float = field(compare=False)
    task_id: str = field(compare=False)
    task: Any = field(compare=False)


class TaskQueue:
    def __init__(self, max_retries: int = 3, initial_backoff: float = 1.0):
        self.queue: List[PrioritizedItem] = []
        self.in_progress: Set[str] = set()
        self.task_data: Dict[str, Any] = {}
        self.retry_counts: Dict[str, int] = defaultdict(int)
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.dead_letter_queue: Deque[Tuple[str, Any, str]] = deque()
        self.deduplication_cache: Dict[str, bool] = {}
        self._shutdown = False
        self._workers: Set[asyncio.Task] = set()
        self._lock = asyncio.Lock()

    async def add_task(
        self,
        task_func: Callable[..., Coroutine],
        *args: Any,
        task_id: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        dedupe_key: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Add a task to the queue with optional deduplication."""
        task_id = task_id or str(uuid.uuid4())

        async with self._lock:
            if dedupe_key and dedupe_key in self.deduplication_cache:
                logger.info(f"Task with dedupe_key {dedupe_key} already exists, skipping")
     ...
```

### GPT-OSS-120B

**Generation Time:** 17521ms
**Tokens:** 2176

```
Below is a **complete, self‑contained** implementation of a production‑grade task queue that satisfies every requirement you asked for:

* **Async worker pool** – any number of workers run concurrently, pulling tasks from a priority queue.
* **Retry with exponential back‑off** – a task is automatically re‑queued after a delay that grows exponentially (with jitter) until `max_retries` is hit.
* **Dead‑letter queue** – tasks that exhaust their retries are moved to a separate queue for later inspection / manual handling.
* **Priority levels** – tasks are ordered by an integer priority (lower numbers = higher priority) using `asyncio.PriorityQueue`.
* **Task deduplication** – the queue keeps a set of the IDs of tasks that are already pending or in‑flight, so the same task cannot be enqueued twice.
* **Graceful shutdown** – on `SIGINT` / `SIGTERM` the queue stops accepting new work, lets the workers finish their current jobs, flushes the pending queue and then exits cleanly.

Only the **standard library** (`asyncio`, `signal`, `logging`, `random`, `time`, `dataclasses`, `typing`) is used – no external dependencies such as Celery or RQ.

---

## 1️⃣  The implementation

```python
#!/usr/bin/env python3
"""
A minimal yet production‑ready async task queue.

Features
--------
* asyncio‑based priority queue
* worker pool with graceful shutdown
* exponential back‑off retry (with jitter)
* dead‑letter queue
* in‑memory deduplication (by task_id)
* simple “task type” dispatch (demo uses three different workers)

Only the Python standard library is used.
"""

import asyncio
import signal
import logging
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, Set, Tuple

# --------------------------------------------------------------------------- #
# Logging configuration (feel free to replace with your own logger setup)
# --------------------------------------------------------------------------- #
logging.basicConfig(...
```

### Gemini 3 Flash Preview

**Generation Time:** 13877ms
**Tokens:** 1837

```
This implementation provides a robust, pure-Python task queue using `asyncio`. It handles concurrency, failures, and lifecycle management without external dependencies.

### The Implementation

```python
import asyncio
import heapq
import time
import uuid
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, Optional

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@dataclass(order=True)
class Task:
    priority: int  # Lower numbers = higher priority
    id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    retries: int = field(default=0, compare=False)
    max_retries: int = field(default=3, compare=False)
    created_at: float = field(default_factory=time.time, compare=False)

class TaskQueue:
    def __init__(self, num_workers: int = 3):
        self._queue = asyncio.PriorityQueue()
        self._num_workers = num_workers
        self._workers = []
        self._running = False
        self._dedup_set = set()  # Simplified deduplication
        self._dlq = []  # Dead Letter Queue

    async def enqueue(self, task_id: str, priority: int, func: Callable, *args, max_retries=3):
        """Adds a task to the queue if the ID is unique."""
        if task_id in self._dedup_set:
            logger.warning(f"Task {task_id} is a duplicate. Skipping.")
            return
        
        task = Task(priority, task_id, func, args, max_retries=max_retries)
        self._dedup_set.add(task_id)
        await self._queue.put(task)
        logger.info(f"Enqueued Task {task_id} (Priority: {priority})")

    async def _worker(self, worker_id: int):
        """Worker loop with exponential backoff and error handling."""
        while self._running:
            task: Task = await self._queue.get()
            try:
                logger.info(f"Worker-{w...
```

### MiniMax M2.5

**Generation Time:** 29833ms
**Tokens:** 2148

```
This is a complete, production-grade implementation using only Python's standard library and `asyncio`.

### Architecture Overview

1.  **`Task`**: A dataclass containing payload, priority, metadata, and retry logic.
2.  **`TaskBroker`**: The core engine. It manages the priority queue, tracks task
```

### MiMo-V2-Flash

**Generation Time:** 17838ms
**Tokens:** 2148

```
This solution implements a robust, type-safe Task Queue using only `asyncio` and the standard library.

### Design Highlights

1.  **Architecture**: Uses `asyncio.PriorityQueue` for ordering and `asyncio.Event` for flow control (shutdown).
2.  **Retry Logic**: Implements exponential backoff with "Jitter" to prevent thundering herds.
3.  **Deduplication**: Uses a `set` to track in-flight and recently completed Task IDs.
4.  **Dead Letter Queue (DLQ)**: Failed tasks after max retries are captured in a separate queue for analysis.
5.  **Worker Types**: Demonstrated via specific handler functions that simulate different latency and failure modes.

### The Code

```python
import asyncio
import uuid
import time
import random
import logging
from dataclasses import dataclass, field
from typing import Callable, Optional, Dict, Any, List
from enum import IntEnum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("TaskQueue")

# --- Constants ---
MAX_RETRIES = 3
BASE_DELAY = 1.0  # Seconds
DLQ_TOPIC = "DEAD_LETTER_QUEUE"

# --- Data Structures ---

class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass(order=True)
class Task:
    priority: int
    task_id: str = field(compare=False)
    handler_name: str = field(compare=False)
    payload: Any = field(compare=False)
    retry_count: int = field(default=0, compare=False)
    created_at: float = field(default_factory=time.time, compare=False)

    def __str__(self):
        return f"Task(id={self.task_id}, type={self.handler_name}, retry={self.retry_count})"

# --- The Queue Engine ---

class AsyncTaskQueue:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        self.dlq = asyncio.Queue() # Dead Letter Queue
        self.shutdown_event = asyncio.Event()
        self.active_tasks: set = set() # For deduplication
        self.completed_tasks: set = set() # For deduplic...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*