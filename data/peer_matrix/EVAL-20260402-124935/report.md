# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-124935
**Timestamp:** 2026-04-02T12:49:35.986600
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

This Python application has a memory leak. Find it and explain the fix.

```python
import threading
import time
from functools import lru_cache

class EventProcessor:
    _instances = []
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        EventProcessor._instances.append(self)
    
    def register_callback(self, func):
        self.callbacks.append(func)
    
    @lru_cache(maxsize=10000)
    def process(self, event_data):
        results = []
        for callback in self.callbacks:
            result = callback(event_data)
            results.append(result)
        return tuple(results)
    
    def __del__(self):
        print(f"Processor {self.name} deleted")

def create_processor_for_request(request_id):
    processor = EventProcessor(f"processor_{request_id}")
    processor.register_callback(lambda x: x.upper())
    processor.register_callback(lambda x: len(x))
    return processor

# Simulated request handling
def handle_request(request_id, data):
    processor = create_processor_for_request(request_id)
    return processor.process(data)

# This runs for hours...
for i in range(1000000):
    result = handle_request(i, f"event_data_{i}")
    time.sleep(0.001)
```

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.54 | 8.80 | 10.00 | 0.45 |
| 2 | Grok 4.20 | 9.06 | 8.40 | 10.00 | 0.59 |
| 3 | Claude Opus 4.6 | 8.81 | 7.55 | 10.00 | 0.76 |
| 4 | Claude Sonnet 4.6 | 8.69 | 6.75 | 10.00 | 1.08 |
| 5 | GPT-OSS-120B | 8.46 | 5.30 | 9.80 | 1.62 |
| 6 | Gemini 3 Flash Preview | 8.46 | 7.80 | 9.60 | 0.53 |
| 7 | DeepSeek V3 | 7.55 | 6.35 | 9.15 | 1.03 |
| 8 | MiniMax M2.5 | 7.11 | 4.80 | 9.55 | 1.73 |
| 9 | Gemini 3.1 Pro | 6.62 | 3.30 | 9.25 | 2.00 |
| 10 | MiMo-V2-Flash | 6.42 | 3.65 | 9.60 | 1.79 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.48 |
| 2 | Gemini 3.1 Pro | 7.12 |
| 3 | Grok 4.20 | 7.26 |
| 4 | Claude Opus 4.6 | 7.52 |
| 5 | Claude Sonnet 4.6 | 7.91 |
| 6 | GPT-OSS-120B | 7.93 |
| 7 | MiniMax M2.5 | 8.41 |
| 8 | MiMo-V2-Flash | 9.04 |
| 9 | Gemini 3 Flash Preview | 9.39 |
| 10 | DeepSeek V3 | 9.47 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
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

**Generation Time:** 19369ms
**Tokens:** 1442

```
There are actually two memory-retention problems here, and one of them is especially subtle.

## Main leak: `_instances` grows forever

This line is the biggest issue:

```python
class EventProcessor:
    _instances = []
```

and then in `__init__`:

```python
EventProcessor._instances.append(self)
```

Every `EventProcessor` ever created is stored in a class-level list. Since that list holds strong references, none of those instances can be garbage-collected.

So this loop:

```python
for i in range(1000000):
    result = handle_request(i, f"event_data_{i}")
```

creates 1,000,000 `EventProcessor` objects, and all of them stay alive forever because `_instances` keeps them referenced.

### Why `__del__` never runs
Because the objects are never freed. The `_instances` list still points to them, so Python cannot collect them, and:

```python
def __del__(self):
    print(f"Processor {self.name} deleted")
```

won’t be called.

## Second issue: `@lru_cache` on an instance method

This is also problematic:

```python
@lru_cache(maxsize=10000)
def process(self, event_data):
```

When you decorate an instance method with `lru_cache`, the cache key includes `self` as part of the arguments. That means the cache stores references to each `EventProcessor` instance used in calls.

So even if you removed `_instances`, the cache can still keep up to 10,000 processor instances alive, because entries look conceptually like:

```python
(self, event_data) -> result
```

If each request creates a new processor and calls `process()` once, the cache fills with entries for many distinct `self` objects.

This is not as catastrophic as `_instances` because `maxsize=10000` bounds it, but it still causes unnecessary retention and can look like a leak.

---

# Fix

## Fix 1: remove the global instance list
If you do not need to keep every instance, delete this entirely:

```python
_instances = []
...
EventProcessor._instances.append(self)
```

If you only want to track live instances for debu...
```

### Claude Opus 4.6

**Generation Time:** 20461ms
**Tokens:** 1318

```
# Memory Leak Analysis

There are **three distinct memory leaks** in this code. Let me break down each one:

## Leak 1: The `_instances` Class Variable

```python
class EventProcessor:
    _instances = []  # ← Every instance is appended here and NEVER removed
    
    def __init__(self, name):
        ...
        EventProcessor._instances.append(self)  # ← Strong reference kept forever
```

Every call to `create_processor_for_request` creates a new `EventProcessor` that gets appended to the class-level `_instances` list. This list holds strong references, preventing garbage collection. After 1,000,000 iterations, you have 1,000,000 objects permanently in memory.

## Leak 2: The `@lru_cache` on an Instance Method

```python
@lru_cache(maxsize=10000)
def process(self, event_data):  # ← `self` is part of the cache key
```

This is the **subtlest and most dangerous** leak. `lru_cache` is a **class-level** decorator, so the cache is shared across all instances. Since `self` is an argument, each instance becomes a cache key — meaning **the cache holds strong references to up to 10,000 instances**, preventing their garbage collection even if all other references are dropped. The `__del__` method will never fire for cached instances.

## Leak 3: Lambda Closures (Minor)

The lambdas registered as callbacks create closures, but this is secondary to the above issues — the objects they're attached to are already leaking.

---

## The Fix

```python
import threading
import time
import weakref

class EventProcessor:
    _instances = []

    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        self._cache = {}                          # ← Per-instance cache instead
        EventProcessor._instances.append(weakref.ref(self))  # ← Weak reference

    def register_callback(self, func):
        self.callbacks.append(func)

    def process(self, event_data):
        # Per-instance cache that dies with the instance
...
```

### Gemini 3.1 Pro

**Generation Time:** 28847ms
**Tokens:** 2409

```
This application actually has **two** memory leaks (one unbounded, one bounded). 

Here is the breakdown of why they happen and how to fix them.

### 1. The Primary Leak: The Class-Level `_instances` List
In the `__init__` method, every time a new `EventProcessor` is created, it appends itself to the class-level list `EventProcessor._instances`. 
Because the main loop creates a new processor for every single request, this list grows indefinitely. The list holds a "strong reference" to every object, meaning Python's Garbage Collector can never destroy them. The `__del__` method will never be called.

### 2. The Secondary Leak (Bloat): `@lru_cache` on
```

### Claude Sonnet 4.6

**Generation Time:** 20491ms
**Tokens:** 1509

```
## Memory Leak Analysis

This code has **three distinct memory leaks** that compound each other.

---

### Leak 1: `_instances` Class Variable Holds Strong References

```python
class EventProcessor:
    _instances = []  # ← Every processor ever created lives here forever
    
    def __init__(self, name):
        EventProcessor._instances.append(self)  # ← Never removed
```

**Problem:** Every `EventProcessor` is appended to this list and never removed. After 1,000,000 requests, 1,000,000 processor objects are retained in memory. The `__del__` method **never fires** because the reference count never reaches zero.

---

### Leak 2: `lru_cache` on an Instance Method

```python
@lru_cache(maxsize=10000)
def process(self, event_data):
    ...
```

**Problem:** `lru_cache` is applied at the **class level**, not per-instance. The cache key includes `self`, so:
- Each unique `(self, event_data)` pair is cached
- The cache holds a **strong reference to `self`**, preventing garbage collection even if `_instances` were fixed
- With `maxsize=10000`, up to 10,000 processor instances are pinned in memory by the cache alone

---

### Leak 3: Lambdas Capture Enclosing Scope

```python
def create_processor_for_request(request_id):
    processor = EventProcessor(f"processor_{request_id}")
    processor.register_callback(lambda x: x.upper())  # Fine here, but
    processor.register_callback(lambda x: len(x))     # pattern is risky
```

**Problem:** In this specific code the lambdas are simple, but the `callbacks` list on each processor creates a **reference cycle** when combined with the cache holding `self` — the processor holds callbacks, the cache holds the processor.

---

### The Fix

```python
import threading
import time
import weakref
from functools import lru_cache

class EventProcessor:
    # Fix 1: Use WeakSet so instances can be garbage collected
    _instances = weakref.WeakSet()
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
   ...
```

### Grok 4.20

**Generation Time:** 4559ms
**Tokens:** 933

```
**The memory leak is here:**

```python
class EventProcessor:
    _instances = []  # ← This is the root cause
    
    def __init__(self, name):
        ...
        EventProcessor._instances.append(self)  # ← Strong reference forever
```

### Why this leaks

1. Every `EventProcessor` instance is appended to a **class-level list** (`_instances`).
2. This creates a **strong reference** that keeps the object alive even after `handle_request()` finishes.
3. The list grows to 1,000,000+ objects and never shrinks.
4. The `@lru_cache` on `process()` makes it even worse: the cache keys hold references to the `EventProcessor` instances (because `self` is part of the cache key), creating a second retention path.

Even though you have a `__del__` method, it almost never runs because the objects are never garbage collected.

### The fix

**Option A — Best (recommended): Remove the `_instances` list entirely** if you don't actually need it.

```python
class EventProcessor:
    # Remove _instances completely
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        # No append!
```

**Option B — If you really need to track instances** (for debugging, metrics, etc.), use a **weak reference**:

```python
import weakref

class EventProcessor:
    _instances = weakref.WeakSet()
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        EventProcessor._instances.add(self)   # weak reference
```

### Additional improvements (strongly recommended)

1. **Don't use `lru_cache` on a method that depends on mutable instance state**:

```python
# Bad - caches based on self + event_data
@lru_cache(maxsize=10000)
def process(self, event_data):
    ...
```

Better:

```python
def process(self, event_data):
    with self._lock:
        results = [cb(event_data) for cb in self.callbacks]
        return tuple(results)
```

Or if you really want cachi...
```

### DeepSeek V3

**Generation Time:** 39749ms
**Tokens:** 1007

```
The memory leak in this Python application stems from several interrelated issues:

1. **Instance Accumulation**: The `EventProcessor._instances` class variable keeps growing indefinitely because:
   - Every request creates a new `EventProcessor` instance
   - The instances are stored in `_instances` but never removed
   - The `__del__` method (destructor) is rarely called because of circular references

2. **LRU Cache Growth**: The `@lru_cache` on the `process()` method will grow up to `maxsize=10000` and hold references to processed events, but this is a secondary issue compared to the instance accumulation.

3. **Lambda Functions**: The lambda functions in `create_processor_for_request()` create circular references between the processor and its callbacks, preventing proper garbage collection.

### The Fixes:

1. **Remove the `_instances` list** unless absolutely necessary, as it's the primary cause of the leak:
   ```python
   class EventProcessor:
       def __init__(self, name):
           self.name = name
           self.callbacks = []
           self._lock = threading.Lock()
   ```

2. **Clear the LRU cache periodically** if you need to keep it:
   ```python
   def process(self, event_data):
       results = []
       for callback in self.callbacks:
           result = callback(event_data)
           results.append(result)
       return tuple(results)
   
   # Optional: add a method to clear the cache
   def clear_cache(self):
       self.process.cache_clear()
   ```

3. **Better alternative**: Use weak references if you need to track instances:
   ```python
   import weakref
   
   class EventProcessor:
       _instances = weakref.WeakSet()
   ```

### Full Fixed Version:
```python
import threading
import time
from functools import lru_cache

class EventProcessor:
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
    
    def register_callback(self, func):
        self.callbacks.append(fu...
```

### GPT-OSS-120B

**Generation Time:** 48057ms
**Tokens:** 2073

```
**What is leaking?**  

Two things keep the `EventProcessor` objects (and the data they produce) alive long after a request has been handled:

1. **The class‑level list `_instances`**  
   ```python
   class EventProcessor:
       _instances = []          # ← global strong references
       …
       def __init__(self, name):
           …
           EventProcessor._instances.append(self)   # ← adds a strong reference
   ```
   Every time `create_processor_for_request` runs a new `EventProcessor` is appended to this list.  
   Because the list holds a *strong* reference, the object can never be garbage‑collected, so `__del__` is never called and the memory used by each processor (its `callbacks`, its lock, its LRU cache, etc.) stays allocated forever.

2. **The `@lru_cache` on an *instance method***  
   ```python
   @lru_cache(maxsize=10000)
   def process(self, event_data):
       …
   ```
   `lru_cache` builds a **per‑instance cache** that uses the bound method (`self.process`) as the cache key.  
   In the loop each request supplies a *different* `event_data` value (`"event_data_0"`, `"event_data_1"` …).  
   The cache therefore stores a new entry for every distinct `event_data` until it reaches `maxsize`.  
   When the cache is full it starts evicting the *oldest* entries, but **the cache itself lives as long as the processor instance lives** – and the processor never dies because of `_instances`.  
   So each processor ends up holding up to 10 000 cached results (tuples of an uppercase string and its length) that are never released.

Together these two patterns cause the program’s memory usage to climb steadily even though each request only needs the processor for a single call.

---

## How to fix it

### 1. Stop keeping strong references to every processor

If you really need to track live processors, use a *weak* container; otherwise just drop the list entirely.

```python
import weakref

class EventProcessor:
    # WeakSet holds only weak references – object...
```

### Gemini 3 Flash Preview

**Generation Time:** 6824ms
**Tokens:** 1222

```
This application contains **two distinct memory leaks** that prevent the `EventProcessor` objects and their associated data from being garbage collected.

### 1. The Global Reference Leak
The most obvious leak is in the `__init__` method:
```python
_instances = []
# ...
EventProcessor._instances.append(self)
```
Every time a `handle_request` is called, a new instance is created and stored in the class-level `_instances` list. Because this list holds a strong reference to every object ever created, the `__del__` method will never be called, and the memory will never be reclaimed.

### 2. The `lru_cache` Instance Method Leak
There is a more subtle, technical leak involving the `@lru_cache` decorator on an instance method:
```python
@lru_cache(maxsize=10000)
def process(self, event_data):
```
In Python, `@lru_cache` creates a permanent internal dictionary to store arguments and results. When you decorate an **instance method**, the `self` argument is stored as part of the cache key. 
*   The cache belongs to the **method object**, which is tied to the **class**.
*   The cache stores a reference to `self` (the instance).
*   Even if you removed the `_instances` list, the `lru_cache` would still hold a reference to the instance until the cache is cleared or overwritten. Since the cache is shared across the class definition for that method, it creates a "zombie" reference preventing cleanup.

### The Fix

To fix this, you should:
1.  **Remove the global tracking list** (unless you use `weakref`).
2.  **Move the cache** so it doesn't hold a reference to `self`, or use a functional approach where the cache is keyed only by the data.

Here is the corrected code:

```python
import threading
import time
from functools import lru_cache

class EventProcessor:
    # REMOVED: _instances = [] (This was the primary leak)
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
    
    def register_callback(self, f...
```

### MiniMax M2.5

**Generation Time:** 38999ms
**Tokens:** 1575

```
# Memory Leak Analysis

There are **two memory leaks** in this code:

## Leak #1: Unbounded `_instances` List (Primary Issue)

```python
class EventProcessor:
    _instances = []  # Class variable - grows forever!
    
    def __init__(self, name):
        # ...
        EventProcessor._instances.append(self)  # Never removed!
```

Every `EventProcessor` ever created is stored in `_instances` and **never removed**. With 1,000,000 requests, this creates 1 million objects that can never be garbage collected.

## Leak #2: Per-Instance `lru_cache` (Secondary Issue)

```python
@lru_cache(maxsize=10000)
def process(self, event_data):
    # ...
```

Each `EventProcessor` instance gets its own cache. Since a new processor is created per request and **never reused**, these caches accumulate useless entries.

---

## The Fix

```python
import threading
import time
from functools import lru_cache

class EventProcessor:
    _instances = []
    _max_instances = 10  # Limit instance tracking
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        
        # Fix: Limit how many instances we track
        if len(EventProcessor._instances) >= self._max_instances:
            EventProcessor._instances.pop(0)
        EventProcessor._instances.append(self)
    
    def register_callback(self, func):
        self.callbacks.append(func)
    
    # Fix: Use a module-level cache instead of instance-level
    @lru_cache(maxsize=1000)
    def process(self, event_data):
        results = []
        for callback in self.callbacks:
            result = callback(event_data)
            results.append(result)
        return tuple(results)
    
    def __del__(self):
        print(f"Processor {self.name} deleted")


# Fix: Reuse processors instead of creating new ones per request
def create_processor_for_request(request_id):
    # Use modulo to limit to a fixed number of processors
    processor = EventProcessor(f"process...
```

### MiMo-V2-Flash

**Generation Time:** 10581ms
**Tokens:** 1233

```
### The Memory Leak

The memory leak is caused by the combination of the `lru_cache` decorator on the `process` method and the creation of new `EventProcessor` instances in a loop.

**The Root Cause:**
1.  **`lru_cache` Behavior:** The `lru_cache` decorator stores the arguments passed to the function in a dictionary (the cache) as keys. These keys hold references to the objects passed as arguments.
2.  **Instance Creation:** In the loop, `create_processor_for_request(i)` creates a **new** `EventProcessor` instance for every iteration.
3.  **The Cycle:**
    *   The `process` method is called with the new `processor` instance as the `self` argument.
    *   The `lru_cache` stores `self` (the `EventProcessor` instance) as a key in its internal dictionary.
    *   The `EventProcessor` instance holds a reference to the `lru_cache` method (via `self.process`).
    *   **Result:** The cache prevents the `EventProcessor` instance from being garbage collected because the cache holds a reference to it. Since the cache has a maxsize of 10,000, it will grow indefinitely (or until the limit is hit), keeping 10,000 instances alive in memory at a time, constantly adding new ones as the loop runs.

### The Fix

To fix this, you need to prevent the `EventProcessor` instance from being used as a cache key. You can achieve this by making the `process` method a `staticmethod`.

Since `process` relies on `self.callbacks`, you must pass the callbacks as an argument to the static method.

Here is the corrected code:

```python
import threading
import time
from functools import lru_cache

class EventProcessor:
    _instances = []
    
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self._lock = threading.Lock()
        EventProcessor._instances.append(self)
    
    def register_callback(self, func):
        self.callbacks.append(func)
    
    # FIX: Make process a static method and pass callbacks explicitly
    @staticmethod
    @lru_cache(maxs...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*