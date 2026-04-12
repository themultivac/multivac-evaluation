# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-130102
**Timestamp:** 2026-04-02T13:01:02.430846
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

This distributed lock implementation has a subtle race condition that can cause two processes to hold the lock simultaneously. Find the bug and fix it.

```python
import redis
import time
import uuid

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())
    
    def acquire(self):
        while True:
            if self.redis.setnx(self.lock_name, self.token):
                self.redis.expire(self.lock_name, self.timeout)
                return True
            time.sleep(0.1)
    
    def release(self):
        if self.redis.get(self.lock_name) == self.token:
            self.redis.delete(self.lock_name)
```

Explain why this is dangerous in production and provide a correct implementation.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Sonnet 4.6 | 9.44 | 8.80 | 10.00 | 0.48 |
| 2 | GPT-5.4 | 9.41 | 8.05 | 10.00 | 0.72 |
| 3 | Claude Opus 4.6 | 9.27 | 8.40 | 10.00 | 0.54 |
| 4 | Grok 4.20 | 9.18 | 8.80 | 9.80 | 0.36 |
| 5 | Gemini 3 Flash Preview | 9.07 | 8.60 | 10.00 | 0.57 |
| 6 | MiMo-V2-Flash | 9.02 | 8.45 | 10.00 | 0.54 |
| 7 | GPT-OSS-120B | 8.83 | 7.50 | 10.00 | 0.75 |
| 8 | MiniMax M2.5 | 8.68 | 6.85 | 10.00 | 1.00 |
| 9 | DeepSeek V3 | 7.94 | 5.90 | 9.80 | 1.37 |
| 10 | Gemini 3.1 Pro | 5.06 | 1.65 | 8.80 | 2.84 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.27 |
| 2 | GPT-OSS-120B | 7.86 |
| 3 | MiniMax M2.5 | 8.24 |
| 4 | Grok 4.20 | 8.46 |
| 5 | Claude Sonnet 4.6 | 8.50 |
| 6 | Claude Opus 4.6 | 8.58 |
| 7 | Gemini 3.1 Pro | 8.59 |
| 8 | MiMo-V2-Flash | 9.01 |
| 9 | DeepSeek V3 | 9.58 |
| 10 | Gemini 3 Flash Preview | 9.69 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 84

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

**Generation Time:** 21511ms
**Tokens:** 1818

```
The bug is that both acquire and release are non-atomic in ways that can break mutual exclusion.

## The race conditions

### 1. `setnx()` + `expire()` is not atomic
In `acquire()`:

```python
if self.redis.setnx(self.lock_name, self.token):
    self.redis.expire(self.lock_name, self.timeout)
    return True
```

If the process crashes, gets paused, or loses connectivity after `setnx()` succeeds but before `expire()` runs, the lock is created without a TTL.

That means:
- the lock may never expire
- all other processes can block forever
- in production, this can become a permanent deadlock until manual intervention

The correct pattern is to set the value and TTL in one atomic Redis command:
- `SET key value NX EX timeout`

---

### 2. `get()` + `delete()` is not atomic
In `release()`:

```python
if self.redis.get(self.lock_name) == self.token:
    self.redis.delete(self.lock_name)
```

This is the more subtle and dangerous bug that can allow **two processes to believe they hold the lock**.

#### Example timeline
1. Process A acquires the lock with token `A`, TTL 10s.
2. Process A runs longer than 10s.
3. Lock expires in Redis.
4. Process B acquires the same lock with token `B`.
5. Process A now calls `release()`.
6. A executes `get(lock)` and sees... depending on timing, it may see its own token earlier, or the lock may change between operations.
7. Before A does `delete()`, Redis state changes.
8. A deletes the lock that B now owns.

Now B is in its critical section, but the lock has been removed. A third process C can acquire it, so **B and C can both proceed simultaneously**.

Even without the exact interleaving above, any `GET` followed by `DELETE` is unsafe because another client can change the key between those two commands.

The fix is to release the lock with an atomic compare-and-delete using a Lua script.

---

## Why this is dangerous in production

Distributed locks are usually used to protect things like:
- payments
- job scheduling
- inventory updates...
```

### Claude Opus 4.6

**Generation Time:** 36883ms
**Tokens:** 2295

```


# The Race Conditions in This Distributed Lock

There are **two critical race conditions** in this implementation. Let me trace through exactly how each one breaks.

---

## Bug #1: Non-Atomic Acquire (`setnx` + `expire`)

```python
# DANGEROUS: Two separate commands, not atomic
if self.redis.setnx(self.lock_name, self.token):  # Step 1: Set the key
    self.redis.expire(self.lock_name, self.timeout) # Step 2: Set expiration
    return True
```

**The failure scenario:**

```
Timeline:
─────────────────────────────────────────────────────────────
Process A:  SETNX lock "token-A" → OK (acquired!)
Process A:  *** CRASHES HERE (before EXPIRE runs) ***

            The lock now exists FOREVER with no TTL.
            
Process B:  SETNX lock "token-B" → FAIL
Process B:  SETNX lock "token-B" → FAIL
Process B:  (spins forever — deadlock)
─────────────────────────────────────────────────────────────
```

The lock key persists indefinitely because `SETNX` and `EXPIRE` are two separate commands. If the process dies between them, no TTL is ever set.

## Bug #2: Non-Atomic Release (`GET` + `DELETE`)

```python
# DANGEROUS: Check-then-act on two separate commands
if self.redis.get(self.lock_name) == self.token:  # Step 1: Check ownership
    # *** ANOTHER PROCESS CAN INTERVENE HERE ***
    self.redis.delete(self.lock_name)              # Step 2: Delete
```

**The failure scenario:**

```
Timeline:
─────────────────────────────────────────────────────────────
Process A:  GET lock → "token-A" (matches! I own it)

            ⚡ Lock expires naturally (TTL runs out)

Process B:  SET lock "token-B" NX EX 10 → OK (acquired!)
Process B:  ... doing critical work ...

Process A:  DELETE lock → OK  ← DELETES PROCESS B's LOCK!

Process C:  SET lock "token-C" NX EX 10 → OK (acquired!)

            💥 Process B and Process C both think they hold the lock
─────────────────────────────────────────────────────────────
```

---

## The Correct Implementation

```python
import redis
import time
...
```

### Gemini 3.1 Pro

**Generation Time:** 26868ms
**Tokens:** 2279

```
There are actually **two** critical concurrency bugs in this implementation. The one that causes two processes to hold the lock simultaneously is in the `release()` method, but there is also a severe deadlock bug in the `acquire()` method.

Here is the breakdown of why this is dangerous, followed by the correct implementation.

### 1. The Mutual Exclusion Bug (Two processes holding the lock)

```

### Claude Sonnet 4.6

**Generation Time:** 29531ms
**Tokens:** 2295

```
## The Race Conditions

This implementation has **two separate race conditions**:

### Bug 1: Non-Atomic Acquire (`setnx` + `expire`)

```python
# DANGEROUS: Two separate operations
if self.redis.setnx(self.lock_name, self.token):  # Step 1: Set key
    self.redis.expire(self.lock_name, self.timeout) # Step 2: Set expiry
    # If process crashes HERE, the key exists forever with no expiry
    # → Lock is permanently held, system deadlocks
```

**Scenario:** Process acquires lock via `setnx`, then crashes before `expire`. The key persists indefinitely with no TTL. No other process can ever acquire the lock.

### Bug 2: Non-Atomic Release (check-then-act)

```python
# DANGEROUS: Check and delete are separate operations
if self.redis.get(self.lock_name) == self.token:  # Step 1: Verify ownership
    self.redis.delete(self.lock_name)              # Step 2: Delete
    # Between steps 1 and 2:
    # - Our lock expires due to slow execution
    # - Process B acquires the lock
    # - We delete Process B's lock!
    # → TWO processes now believe they hold the lock
```

**Timeline of Bug 2:**
```
Process A: GET lock → "token-A"  ✓ (we own it)
    [A is slow, lock TTL expires]
Process B: SET lock "token-B"    ✓ (B acquires lock)
Process A: DEL lock              ✗ (A deletes B's lock!)
Process C: SET lock "token-C"    ✓ (C acquires lock)
    → B and C both think they hold the lock
```

## Correct Implementation

```python
import redis
import time
import uuid
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Lua script for atomic release: verify ownership and delete in one operation
# Redis executes Lua scripts atomically - no other commands run between steps
RELEASE_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""

# Lua script for atomic extend: verify ownership and reset TTL
EXTEND_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.ca...
```

### Grok 4.20

**Generation Time:** 6573ms
**Tokens:** 1255

```
**The Bug**

This implementation has a **critical race condition** that can cause two (or more) processes to believe they both hold the lock simultaneously.

### Root Cause

The `acquire()` method does two separate Redis commands:

1. `SETNX` (set if not exists)
2. `EXPIRE` (set TTL)

If a process succeeds at `SETNX` but **crashes or gets paused** before calling `EXPIRE`, the lock is set **forever** (no TTL).

Even worse, there's a subtler and more dangerous race in the current code:

```python
if self.redis.get(self.lock_name) == self.token:
    self.redis.delete(self.lock_name)
```

This is the classic "check-then-act" anti-pattern in distributed systems. Between the `GET` and the `DELETE`, another process can:

- See the lock is held by a different token
- Timeout and acquire the lock itself
- Then your `DELETE` executes and removes *someone else's* lock

This is the **most common distributed lock bug**.

---

### Why This Is Dangerous in Production

* Multiple processes can enter the critical section simultaneously
* Can cause data corruption, duplicate messages, double charging, etc.
* The bug is probabilistic and timing-dependent — very hard to reproduce in tests
* Gets worse under high load or network latency
* Redis failover or client retries make it even more likely

This is the exact bug that has caused outages at many companies using naive Redis locks.

---

### Correct Implementation

Here's a robust implementation using the modern `SET` command with `NX` + `PX` in one atomic operation, plus proper token-based unlocking using a Lua script:

```python
import redis
import uuid
import time
from typing import Optional

class DistributedLock:
    def __init__(self, redis_client, lock_name: str, timeout: int = 10, retry_delay: float = 0.1):
        self.redis: redis.Redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout          # seconds
        self.retry_delay = retry_delay
        self.token = str(uuid.uuid4())
   ...
```

### DeepSeek V3

**Generation Time:** 35212ms
**Tokens:** 725

```
The bug in this implementation is in the `acquire()` method where there's a race condition between the `setnx` and `expire` operations. If the process crashes after `setnx` but before `expire`, the lock will never get a timeout and will remain held indefinitely, causing a deadlock.

**Why this is dangerous in production:**
1. If a process crashes after acquiring the lock but before setting the expiration, the lock becomes permanently stuck
2. Other processes waiting for the lock will be blocked indefinitely
3. This can lead to system-wide deadlocks and service outages
4. Manual intervention would be required to delete the stuck lock

**Corrected implementation:**
```python
import redis
import time
import uuid

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())
    
    def acquire(self):
        while True:
            # Use single atomic operation to set both value and expiration
            if self.redis.set(self.lock_name, self.token, nx=True, ex=self.timeout):
                return True
            time.sleep(0.1)
    
    def release(self):
        # Use Lua script for atomic check-and-delete
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        self.redis.eval(script, 1, self.lock_name, self.token)
```

Key improvements:
1. In `acquire()`, using a single atomic `set` operation with both `nx` and `ex` parameters ensures the lock either gets set with expiration or fails completely
2. In `release()`, using a Lua script ensures the token check and delete happen atomically
3. The lock will always have a timeout, preventing deadlocks
4. Only the lock owner can release the lock (verified by token)

Additional recommendations for production:
1. Consider impl...
```

### GPT-OSS-120B

**Generation Time:** 397100ms
**Tokens:** 2298

```
## 1️⃣  What’s wrong with the original code?

| Step | Original code | Why it is unsafe |
|------|---------------|------------------|
| **A. Acquire** | `SETNX lock_name token` → **then** `EXPIRE lock_name timeout` | `SETNX` and `EXPIRE` are two separate commands. If the process crashes **after** `SETNX` but **before** `EXPIRE`, the lock stays forever (or until another client manually deletes it).  <br>Two processes can also race: Process 1 does `SETNX` → succeeds, but before it calls `EXPIRE` Process 2 runs `SETNX` (fails) → sleeps, then sees the key (still without TTL) and thinks the lock is “stale” and may delete it or acquire it after a manual clean‑up. |
| **B. Release** | `if GET lock_name == token: DELETE lock_name` | This is a **check‑then‑act** sequence that is **not atomic**. Between the `GET` and the `DELETE` another client may have acquired the lock (because the original lock timed‑out). In that case the `DELETE` removes the *new* owner’s lock – two processes think they own the lock at the same time. |
| **C. No renewal / watchdog** | – | If a client holds the lock longer than `timeout`, the lock expires and another client can acquire it while the first client is still working. |
| **D. No error handling / back‑off** | Busy‑wait + fixed `sleep(0.1)` | In production this can cause thundering‑herd spikes and makes the lock unsuitable under high contention. |

All of the above can lead to **two (or more) processes simultaneously believing they own the lock**, which defeats the whole purpose of a distributed lock and can corrupt shared state, break invariants, or cause duplicate work.

---

## 2️⃣  The correct way to implement a Redis‑based lock

Redis itself already provides an **atomic** command that does everything we need for the *acquire* step:

```redis
SET key value NX PX <ttl>
```

* `NX` – set only if the key does **not** exist (i.e. acquire the lock).  
* `PX` – set the key’s TTL in **milliseconds** (so the lock will auto‑expire).  
* The whole ope...
```

### Gemini 3 Flash Preview

**Generation Time:** 6461ms
**Tokens:** 1112

```
### The Bug: Non-Atomic Operations

There are two major race conditions in this implementation:

1.  **In `acquire()` (The "Crash between SETNX and EXPIRE"):**
    The `setnx` and `expire` calls are two separate network requests. If the process crashes or the network fails **after** `setnx` succeeds but **before** `expire` is called, the lock will stay in Redis forever (or until manual intervention). This leads to a **deadlock** where no other process can ever acquire the lock.

2.  **In `release()` (The "Check-then-Act" Race):**
    The `get` and `delete` are non-atomic. Imagine this scenario:
    *   **Process A** acquires the lock.
    *   **Process A** hangs (GC pause or slow network) and the lock expires.
    *   **Process B** acquires the lock.
    *   **Process A** resumes and calls `release()`. It performs the `get`, sees its token is still there (unlikely if B took it, but possible if a 3rd process is involved), or more commonly: **Process A** verifies the token, but right before it calls `delete`, the lock expires and **Process B** takes it. **Process A** then calls `delete`, which deletes **Process B's** lock.
    *   **Process C** now acquires the lock while **Process B** still thinks it holds it.

### Why this is dangerous in production
Data corruption is the primary risk. If two processes believe they have exclusive access to a resource (like a database row, a file, or an external API), they will both perform writes simultaneously, leading to "lost updates" or inconsistent state that is extremely difficult to debug.

### The Correct Implementation

To fix this, we must use:
1.  The atomic `SET lock_name value NX PX timeout` command.
2.  A **Lua script** for releasing the lock to ensure the "get-and-delete" happens as a single atomic unit within Redis.

```python
import redis
import time
import uuid

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10):
        self.redis = redis_client
        self.lock_name = f"lock:{lock...
```

### MiniMax M2.5

**Generation Time:** 129175ms
**Tokens:** 2268

```
## The bug

```python
def acquire(self):
    while True:
        if self.redis.setnx(self.lock_name, self.token):   # ①
            self.redis.expire(self.lock_name, self.timeout) # ②
            return True
        time.sleep(0.1)
```

* `SETNX` and `EXPIRE` are **two separate Redis commands**.  
  They are not executed atomically, so a crash (or a network glitch) can happen between them:

* **Process A** executes `SETNX` → lock is taken.  
* **Process A** crashes **before** `EXPIRE` runs → the key has **no expiry**.  
* The lock now lives forever – every other client will wait forever.

A second, equally serious race lives in `release`:

```python
def release(self):
    if self.redis.get(self.lock_name) == self.token:   # ③
        self.redis.delete(self.lock_name)               # ④
```

* Between the `GET` (③) and the `DELETE` (④) the lock may have **expired** and another process may have **re‑acquired** it.  
* When the original owner finally executes `DELETE`, it **removes the new owner’s lock** – two processes end up inside the critical section simultaneously.

Both places break the fundamental promise of a distributed lock: *the lock must be acquired atomically and released only by the rightful owner*.

---

## Why this is dangerous in production

| Symptom | Consequence |
|---------|-------------|
| **Lock never expires** (①‑② race) | Deadlock – all clients wait forever – service outage. |
| **Premature release** (③‑④ race) | Two processes run the critical section together → data corruption, inconsistent state, financial errors, etc. |
| **No ownership guarantee** | Any client can delete the key, even if it never owned it – the lock becomes useless. |

In a real‑world system the critical section often touches shared resources (database rows, cloud buckets, payment ledgers). When two processes enter at the same time the results can be catastrophic.

---

## A correct implementation

We need two atomic primitives:

1. **Acquire** – use a *single* `SET … NX … E...
```

### MiMo-V2-Flash

**Generation Time:** 11961ms
**Tokens:** 1538

```
### The Bug

The race condition occurs between the `setnx` and `expire` commands in the `acquire` method.

**The Scenario:**
1.  **Process A** calls `acquire`. It executes `self.redis.setnx(self.lock_name, self.token)`.
2.  **Process A** successfully acquires the lock (returns `True`).
3.  **Process A** is immediately paused by the operating system (context switch) or the Redis server is momentarily slow to process the next command.
4.  **Process B** calls `acquire`. It finds the key already exists, so it waits.
5.  **Process A** resumes and tries to execute `self.redis.expire(self.lock_name, self.timeout)`, but it crashes (e.g., power failure, OOM) or the connection drops before this command is sent to Redis.
6.  **Result:** The key exists in Redis with no expiration time (a "persistent" key). Process B will wait forever (or until the lock is manually cleared), causing a deadlock.

### Why This is Dangerous in Production

1.  **Deadlocks:** As described above, if the `expire` command fails to execute, the lock never times out. All other processes waiting for that lock will hang indefinitely, potentially requiring a manual restart of services or flushing Redis keys.
2.  **Blocking Event Loop:** The `acquire` method uses `while True` with a blocking `time.sleep`. In asynchronous frameworks (like asyncio or Tornado), this freezes the entire event loop, preventing other tasks from running.
3.  **Lack of Atomicity:** The check-then-act pattern (`setnx` followed by `expire`) is not atomic. Distributed systems rely on atomic operations to guarantee consistency.

### The Fix

To fix this, we must use a single atomic command. Redis provides the `SET` command with specific options: `NX` (only set if not exists) and `EX` (expiration in seconds).

Additionally, we should implement a **safe release** mechanism using a Lua script. This ensures that we only delete the lock if we own it (matching the token), preventing a process from accidentally deleting a lock acquired by anothe...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*