# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-081848
**Timestamp:** 2026-04-03T08:18:48.001527
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

This Python async function has 3 bugs: a race condition, an unhandled exception, and a resource leak. Find all three and explain why each is problematic.

```python
import asyncio
import aiohttp

class DataFetcher:
    def __init__(self):
        self.cache = {}
        self.session = aiohttp.ClientSession()
    
    async def fetch_data(self, urls):
        results = []
        for url in urls:
            if url in self.cache:
                results.append(self.cache[url])
            else:
                async with self.session.get(url) as response:
                    data = await response.json()
                    self.cache[url] = data
                    results.append(data)
        return results
    
    async def fetch_parallel(self, urls):
        tasks = [self.fetch_single(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def fetch_single(self, url):
        if url in self.cache:
            return self.cache[url]
        async with self.session.get(url) as response:
            data = await response.json()
            self.cache[url] = data
            return data
```

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-OSS-120B | 9.46 | 8.80 | 10.00 | 0.50 |
| 2 | Grok 4.20 | 9.36 | 8.65 | 10.00 | 0.56 |
| 3 | Claude Sonnet 4.6 | 9.34 | 7.95 | 10.00 | 0.66 |
| 4 | GPT-5.4 | 9.32 | 8.65 | 10.00 | 0.49 |
| 5 | Claude Opus 4.6 | 9.31 | 8.55 | 10.00 | 0.60 |
| 6 | MiMo-V2-Flash | 9.03 | 8.40 | 10.00 | 0.52 |
| 7 | Gemini 3 Flash Preview | 8.72 | 7.10 | 9.80 | 0.88 |
| 8 | DeepSeek V3 | 8.62 | 7.40 | 9.80 | 0.86 |
| 9 | Gemini 3.1 Pro | 7.48 | 6.00 | 8.90 | 1.12 |
| 10 | MiniMax M2.5 | 6.24 | 3.85 | 9.05 | 1.80 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 7.89 |
| 2 | GPT-5.4 | 7.96 |
| 3 | Claude Opus 4.6 | 8.23 |
| 4 | Claude Sonnet 4.6 | 8.52 |
| 5 | Grok 4.20 | 8.52 |
| 6 | MiniMax M2.5 | 8.56 |
| 7 | Gemini 3.1 Pro | 8.73 |
| 8 | DeepSeek V3 | 9.44 |
| 9 | Gemini 3 Flash Preview | 9.46 |
| 10 | MiMo-V2-Flash | 9.46 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** mimo_v2_flash
**Total Judgments:** 100
**Valid Judgments:** 89

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

**Generation Time:** 11193ms
**Tokens:** 940

```
Here are the 3 bugs:

## 1. Race condition in `fetch_single` / `fetch_parallel`

### Where
```python
if url in self.cache:
    return self.cache[url]
async with self.session.get(url) as response:
    data = await response.json()
    self.cache[url] = data
    return data
```

### Why it’s a race
When `fetch_parallel()` runs multiple tasks at once, two or more tasks can request the same URL simultaneously.

Example:
- Task A checks `if url in self.cache` → not present
- Task B checks `if url in self.cache` → also not present
- Both perform `self.session.get(url)`
- Both fetch and write the same cache entry

### Why problematic
- Duplicate network requests
- Wasted bandwidth and latency
- Possible inconsistent results if the endpoint is non-deterministic
- Can lead to subtle bugs if cache writes are expected to happen only once

### Typical fix
Use a lock or track in-flight requests per URL so only one coroutine fetches a given URL at a time.

---

## 2. Unhandled exception in `fetch_parallel`

### Where
```python
return await asyncio.gather(*tasks)
```

and also:
```python
data = await response.json()
```

### Why it’s unhandled
If any request fails:
- connection error
- timeout
- invalid JSON
- HTTP error handling issue

then that exception propagates out of `asyncio.gather()`.

By default, `gather()` will raise on the first exception and fail the whole batch.

Also, there’s no check like:
```python
response.raise_for_status()
```
so bad HTTP responses may lead to confusing downstream failures when trying to parse JSON.

### Why problematic
- One bad URL can cause all parallel fetches to fail
- Caller may lose successful results from other URLs
- Exceptions like `aiohttp.ClientError`, `asyncio.TimeoutError`, or `JSONDecodeError` aren’t handled

### Typical fix
Either:
- catch exceptions inside `fetch_single`, or
- use `asyncio.gather(..., return_exceptions=True)`, and
- call `response.raise_for_status()` before parsing

---

## 3. Resource leak: `ClientSession` is n...
```

### Claude Opus 4.6

**Generation Time:** 128476ms
**Tokens:** 1355

```
# Three Bugs in `DataFetcher`

## Bug 1: Race Condition in `fetch_parallel` / `fetch_single`

```python
async def fetch_single(self, url):
    if url in self.cache:          # Thread A checks: not cached
        return self.cache[url]
    # --> Thread A suspends at await
    async with self.session.get(url) as response:
        data = await response.json()   # Thread B also fetches same URL
        self.cache[url] = data         # Both write to cache, both make redundant requests
        return data
```

**Why it's problematic:** When `fetch_parallel` launches multiple tasks, two tasks with the **same URL** can both pass the `if url in self.cache` check before either completes. Every `await` is a suspension point where another coroutine can run. This means:
- Duplicate network requests for the same URL
- In more complex scenarios, one coroutine could read a partially-updated cache state

**Fix:** Use an `asyncio.Lock` per URL, or a dictionary of `asyncio.Event`/`Future` objects so only the first coroutine fetches while others wait:

```python
def __init__(self):
    self.cache = {}
    self.locks = {}  # per-URL locks
    self.session = aiohttp.ClientSession()

async def fetch_single(self, url):
    if url not in self.locks:
        self.locks[url] = asyncio.Lock()
    async with self.locks[url]:
        if url in self.cache:
            return self.cache[url]
        async with self.session.get(url) as response:
            data = await response.json()
            self.cache[url] = data
            return data
```

## Bug 2: Unhandled Exception from `response.json()`

```python
async with self.session.get(url) as response:
    data = await response.json()  # Can raise ContentTypeError, JSONDecodeError,
                                   # ClientError, TimeoutError, etc.
```

**Why it's problematic:** If *any* URL returns non-JSON content (e.g., an HTML error page), a non-200 status, or the connection drops, the entire `fetch_parallel` call fails via `asyncio.gather...
```

### Gemini 3.1 Pro

**Generation Time:** 31682ms
**Tokens:** 2333

```
Here is the breakdown of the three bugs in the provided `DataFetcher` class, including where they occur and why they are problematic.

### 1. The Race Condition
**Where it happens:** In the `fetch_single` method (used by `fetch_parallel`).
```python
if url in self.cache:
    return self.cache[url]
async with self.session.get(url) as response:
    data = await response.json()
    self.cache[url] = data # <-- Populated too late
```
**Why it is problematic:** 
This is a classic "check-then-act" race condition. When `fetch_parallel` is called with a list containing duplicate URLs (or if multiple concurrent calls are made to `fetch_single`), multiple tasks will simultaneously check `if url in self.cache`. Because the network request (`await self.session.get`) yields control to the event loop, Task A will check the cache, find it empty, and start the network request. Before Task A finishes and populates the cache, Task B will also check the cache, find it empty, and start a redundant network request. 
**Consequence:** It defeats the purpose of the cache for concurrent requests, resulting in redundant network I/O, wasted bandwidth, and potentially hitting API rate limits.

### 2. The Unhandled Exception
**Where it happens:** In both `fetch_data` and `fetch_single` during the network request and JSON parsing.
```python
async with self.session.get(url) as response:
    data = await response.json()
```
**Why it is problematic:**
Network requests are inherently unreliable. The server might return a 404, a 500, timeout, or return an HTML error page instead of JSON. If any of these happen, `session.get()` might raise an `aiohttp.ClientError`, or `response.json()` will raise a `json.JSONDecodeError` / `aiohttp.ContentTypeError`. 
Because `fetch_parallel` uses `await asyncio.gather(*tasks)` without the `return_exceptions=True` flag, **a single failing URL will raise an exception that crashes the entire `gather
```

### Claude Sonnet 4.6

**Generation Time:** 22779ms
**Tokens:** 1740

```
## Bug Analysis

### Bug 1: Race Condition in `fetch_parallel` / `fetch_single`

```python
async def fetch_single(self, url):
    if url in self.cache:          # Thread A checks: url NOT in cache
        return self.cache[url]
    async with self.session.get(url) as response:  # Thread A suspends here (await point)
        data = await response.json()               # Thread B also fetches same URL
        self.cache[url] = data     # Both write to cache, duplicate requests made
        return data
```

**Why it's problematic:** When `fetch_parallel` creates multiple tasks for overlapping URLs, the `await` points allow the event loop to context-switch between coroutines. Two coroutines can both pass the cache check before either writes to it, resulting in:
- Duplicate HTTP requests for the same URL (wasted network/server resources)
- Potential inconsistency if responses differ (e.g., mutable API data)
- Under heavy load, this can cause request storms

**Fix:** Use a lock and a "pending" set to prevent duplicate in-flight requests:

```python
def __init__(self):
    self.cache = {}
    self.pending = {}  # url -> asyncio.Task
    self._lock = asyncio.Lock()
    self.session = aiohttp.ClientSession()

async def fetch_single(self, url):
    # Check cache first (fast path, no lock needed for reads)
    if url in self.cache:
        return self.cache[url]
    
    async with self._lock:
        # Double-check after acquiring lock
        if url in self.cache:
            return self.cache[url]
        
        # Reuse existing in-flight request if present
        if url not in self.pending:
            self.pending[url] = asyncio.ensure_future(self._do_fetch(url))
        task = self.pending[url]
    
    try:
        return await task
    finally:
        self.pending.pop(url, None)

async def _do_fetch(self, url):
    async with self.session.get(url) as response:
        data = await response.json()
        self.cache[url] = data
        return data
```

---

### Bug 2...
```

### Grok 4.20

**Generation Time:** 4082ms
**Tokens:** 1077

```
**The three bugs are:**

### 1. Race Condition (in `fetch_parallel` + `fetch_single`)

**Bug:** Multiple concurrent calls to `fetch_parallel()` (or even a single call with duplicate URLs) can trigger multiple simultaneous HTTP requests for the same URL.

**Why it's problematic:**

```python
# If the same URL appears twice, or multiple fetch_parallel() calls overlap:
tasks = [self.fetch_single(url) for url in urls]  # creates N tasks
await asyncio.gather(*tasks)
```

In `fetch_single()`:

```python
if url in self.cache:          # Check
    return self.cache[url]

# Time window here — another task can also pass the check
async with self.session.get(url) as response:  # Both make the request!
```

This is a classic **TOCTOU** (Time-of-Check to Time-of-Use) race condition. It defeats the purpose of the cache and can cause unnecessary load on the server (or even rate-limiting bans).

**Worse:** If the requests return slightly different data (e.g. due to eventual consistency), the cache can end up in an inconsistent state depending on which one finishes last.

---

### 2. Resource Leak (the `ClientSession`)

**Bug:** `self.session = aiohttp.ClientSession()` is created in `__init__` but **never closed**.

**Why it's problematic:**

- `ClientSession` holds open TCP connections, SSL contexts, and internal task cleanup.
- Without `await session.close()` (or using it as a context manager), these resources are not properly released.
- In long-running applications, this leads to **socket leaks**, file descriptor exhaustion, and memory leaks.
- The `DataFetcher` object becoming garbage-collected does *not* guarantee proper cleanup because `ClientSession` manages background tasks.

**Correct pattern:**

```python
async def close(self):
    await self.session.close()

# or better:
async def __aenter__(self):
    return self
async def __aexit__(self, *args):
    await self.session.close()
```

---

### 3. Unhandled Exception (in both `fetch_data` and `fetch_single`)

**Bug:** There...
```

### DeepSeek V3

**Generation Time:** 17011ms
**Tokens:** 823

```
Let's analyze the three bugs in this code:

1. **Race Condition**:
   - Location: In both `fetch_data` and `fetch_single` when checking cache and updating it
   - Problem: Multiple coroutines might check the cache simultaneously, find the URL missing, and all proceed to make the same request unnecessarily. Between checking `url in self.cache` and setting `self.cache[url]`, another coroutine could check the cache and also find it empty.
   - Why problematic: This leads to duplicate network requests which wastes resources and could cause inconsistent data if the responses differ.

2. **Unhandled Exception**:
   - Location: No error handling around the HTTP request and JSON parsing
   - Problem: Both `session.get()` and `response.json()` can raise exceptions (like aiohttp.ClientError, JSONDecodeError, etc.) that aren't caught.
   - Why problematic: Unhandled exceptions will propagate up and likely crash the application. In production code, network requests should have proper error handling.

3. **Resource Leak**:
   - Location: The `ClientSession` is never closed
   - Problem: The session is created in `__init__` but there's no cleanup method (like `close()` or `__del__`) or context manager usage.
   - Why problematic: Leaving sessions open can lead to connection leaks, file descriptor exhaustion, and other resource issues. Sessions should always be properly closed.

Fixed version would need to:
1. Add proper synchronization (like asyncio.Lock) around cache access
2. Add try-except blocks around network operations
3. Implement a close method and/or context manager protocol

Example fixes could include:

```python
import asyncio
import aiohttp

class DataFetcher:
    def __init__(self):
        self.cache = {}
        self.session = None
        self.lock = asyncio.Lock()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
    
  ...
```

### GPT-OSS-120B

**Generation Time:** 29667ms
**Tokens:** 2328

```
**Short answer**

| Bug | Where it lives | Why it is a bug |
|-----|----------------|-----------------|
| 1️⃣ Race condition on the shared `self.cache` | `fetch_data` **and** `fetch_single` (both read‑then‑write the dict) | Two coroutines can check “`url not in cache`”, both start a network request, and then both write the result – the cache may be populated twice, and the *first* result can be silently overwritten by the second. |
| 2️⃣ Unhandled exception from the HTTP call / JSON decode | `async with self.session.get(url) … await response.json()` (both methods) and the `asyncio.gather` in `fetch_parallel` | If the request fails (timeout, DNS error, non‑200 status) or the body is not valid JSON, `aiohttp` or `response.json()` raises an exception. The code never catches it, so the exception propagates out of the coroutine and (in `fetch_parallel`) aborts the whole `gather`, cancelling the other pending tasks. |
| 3️⃣ Resource leak – never closing the `aiohttp.ClientSession` | `self.session = aiohttp.ClientSession()` in `__init__` | A `ClientSession` holds sockets, a connector pool, and background tasks. If you never call `await session.close()` (or use it as an async context manager) the underlying TCP connections stay open until the interpreter exits, which can exhaust file descriptors or keep the event loop alive indefinitely. |

Below is a more detailed walk‑through of each problem and why it matters in a real‑world async program.

---

## 1️⃣ Race condition on the cache

### Where it happens
```python
if url in self.cache:
    return self.cache[url]          # read
# …
self.cache[url] = data              # write
```
Both `fetch_data` (the sequential loop) **and** `fetch_single` (the parallel version) perform a *check‑then‑act* sequence on the same mutable dictionary that lives on the `DataFetcher` instance.

### Why it is a problem
`asyncio` runs many coroutines on the *same* thread.  The check (`url in self.cache`) and the subsequent write (`self.cache[url] = ...
```

### Gemini 3 Flash Preview

**Generation Time:** 6270ms
**Tokens:** 954

```
Here are the three bugs identified in the code, along with explanations for why they are problematic:

### 1. The Race Condition (Cache Stampede)
**Location:** `fetch_single` method.

**The Problem:** 
In `fetch_parallel`, multiple tasks are initiated simultaneously. When multiple tasks request the same `url` at the exact same time, they all check `if url in self.cache`. Since the cache is empty, all tasks proceed to make redundant network requests to the same URL. Once the requests finish, they all overwrite the same key in `self.cache`.

**Why it’s problematic:** 
This defeats the purpose of caching. It wastes bandwidth, puts unnecessary load on the server, and in a production environment, could lead to rate-limiting or a "Thundering Herd" problem where a single popular expired key causes a system crash.

### 2. The Resource Leak
**Location:** `__init__` method and the `ClientSession` object.

**The Problem:** 
The code instantiates `aiohttp.ClientSession()`, but it never calls `await self.session.close()`. `aiohttp` sessions hold onto underlying connection pools. Because the session is never closed, the program will hang or emit `Unclosed client session` warnings upon exit. Furthermore, there is no `__aenter__` or `__aexit__` logic to manage the lifecycle of the session.

**Why it’s problematic:** 
Resource leaks lead to memory exhaustion and "too many open files" (socket) errors. In long-running applications, this will eventually cause the application to crash because it can no longer open new network connections.

### 3. The Unhandled Exception (Partial Failure)
**Location:** `fetch_parallel` method calling `asyncio.gather`.

**The Problem:** 
By default, `asyncio.gather(*tasks)` will raise the **first** exception that occurs among the tasks. If one URL fails (e.g., a 404, a DNS error, or invalid JSON), the entire `fetch_parallel` call crashes immediately. However, the other tasks that were running in the background are not automatically cancelled; they continu...
```

### MiniMax M2.5

**Generation Time:** 32468ms
**Tokens:** 2318

```
Below is a concise breakdown of the three hidden problems in the snippet, together with why each of them is dangerous.

---

## 1️⃣ Race condition (concurrent cache access)

**What the code does**  
Both `fetch_data` and `fetch_single` look at `self.cache` with a plain Python dictionary:

```python
if url in self.cache:
    return self.cache[url]
else:
    # … fetch the URL and store the result …
```

**Why it’s a race**  
The *check‑then‑act* (`if url in cache … else …`) is **not atomic**. When several coroutines run `fetch_single` (or the loop in `fetch_data`) at the same time they can all see “not in cache”, all issue a network request for the same URL, and all try to write the result back to the dictionary. The outcome is:

* **Duplicate network calls** – wasteful and slower.
* **Potential data inconsistency** – one coroutine may overwrite another’s result, or the dictionary may be left in a partially‑updated state.
* **Lost updates** – if two coroutines write different data for the same key, the final value may be whichever one finished last, not necessarily the “correct” one.

In an async program this is especially easy to trigger because `await` yields control to the event loop, allowing other tasks to slip in between the check and the write.

*Fix*: Protect the cache with an `asyncio.Lock`, or dedupe requests by storing a `Future` (or task) for each URL so that concurrent callers wait on the same network request.

---

## 2️⃣ Unhandled exception (no error handling)

**What the code does
```

### MiMo-V2-Flash

**Generation Time:** 29786ms
**Tokens:** 1888

```
Of course. Here are the three bugs in the provided code, with explanations for why each is problematic.

### 1. Bug: Race Condition

**Location:** In the `fetch_parallel` method, which calls `fetch_single`.

**Explanation:**
The `fetch_parallel` method uses `asyncio.gather` to run multiple `fetch_single` tasks concurrently. Both `fetch_single` and `fetch_data` contain a common pattern:
1.  Check if `url` is in `self.cache`.
2.  If not, fetch the data from the network.
3.  Store the data in `self.cache`.

This sequence is a classic **Time-of-Check to Time-of-Use (TOCTOU)** vulnerability. When multiple tasks run concurrently, they can interleave their operations, leading to a race condition.

Here's how the race can occur with two concurrent tasks for the same URL (e.g., `http://example.com/data`) that is not yet in the cache:

1.  **Task A** checks `if url in self.cache`. It's `False`.
2.  **Task B** checks `if url in self.cache`. It's also `False`.
3.  **Task A** proceeds to make a network request: `async with self.session.get(url)...`
4.  **Task B** also proceeds to make a network request for the *exact same URL*.

**Why this is problematic:**
*   **Unnecessary Network Load:** Two separate requests are made for the same resource, wasting bandwidth and server resources.
*   **Inconsistent State:** While the `aiohttp.ClientSession` may have connection pooling, this is still redundant work.
*   **Potential for Logic Errors:** If the cache operation was more complex (e.g., `self.cache[url] = some_operation(data)`), you could get inconsistent results if the two tasks don't perform the exact same operation.

---

### 2. Bug: Unhandled Exception

**Location:** In any of the fetching methods (`fetch_data` or `fetch_single`).

**Explanation:**
The methods `fetch_data` and `fetch_single` make network requests using `self.session.get(url)`. Network operations are inherently unreliable and can fail for many reasons: DNS resolution failure, connection timeout, server error (5xx...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*