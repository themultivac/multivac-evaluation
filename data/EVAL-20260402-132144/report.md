# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-132144
**Timestamp:** 2026-04-02T13:21:44.320817
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python. It should support add, remove, lookup, and merge operations. Include a proof that merge is commutative, associative, and idempotent. Write tests demonstrating conflict resolution between two divergent replicas.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| None | GPT-5.4 | 8.75 | 8.25 | 9.45 | 0.44 |
| None | Claude Opus 4.6 | 7.39 | 4.65 | 8.80 | 1.89 |
| None | Gemini 3.1 Pro | 4.19 | 1.65 | 7.60 | 2.71 |
| None | Claude Sonnet 4.6 | 7.48 | 6.00 | 8.60 | 1.17 |
| None | DeepSeek V3 | 8.49 | 7.40 | 8.95 | 0.73 |
| None | GPT-OSS-120B | 8.17 | 6.75 | 9.60 | 1.20 |
| None | Gemini 3 Flash Preview | 8.97 | 8.45 | 9.80 | 0.58 |
| None | MiMo-V2-Flash | 8.00 | 7.65 | 8.80 | 0.47 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 6.14 |
| 2 | MiMo-V2-Flash | 7.34 |
| 3 | MiniMax M2.5 | 7.73 |
| 4 | Claude Sonnet 4.6 | 7.83 |
| 5 | Gemini 3.1 Pro | 7.88 |
| 6 | Grok 4.20 | 8.22 |
| 7 | DeepSeek V3 | 8.92 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 90
**Valid Judgments:** 38

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

**Generation Time:** 32992ms
**Tokens:** 2116

```
Below is a complete Python implementation of a **Last-Writer-Wins Element Set (LWW-Element-Set)** CRDT, along with:

- `add`, `remove`, `lookup`, and `merge`
- a configurable tie-break policy
- a proof sketch that `merge` is **commutative**, **associative**, and **idempotent**
- tests showing conflict resolution for divergent replicas

---

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, Optional, Set, TypeVar


T = TypeVar("T")


@dataclass
class LWWElementSet(Generic[T]):
    """
    Last-Writer-Wins Element Set CRDT.

    Each element tracks:
      - latest add timestamp
      - latest remove timestamp

    Membership rule:
      - An element is present if add_ts > remove_ts
      - If timestamps are equal, tie is resolved by `bias`:
          * "add"    => present when add_ts == remove_ts
          * "remove" => absent when add_ts == remove_ts

    This implementation assumes timestamps are totally ordered.
    """

    bias: str = "add"  # either "add" or "remove"
    adds: Dict[T, int] = field(default_factory=dict)
    removes: Dict[T, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.bias not in ("add", "remove"):
            raise ValueError("bias must be either 'add' or 'remove'")

    def add(self, element: T, timestamp: int) -> None:
        """
        Record an add operation for `element` at `timestamp`.
        Keeps only the maximum add timestamp for that element.
        """
        current = self.adds.get(element)
        if current is None or timestamp > current:
            self.adds[element] = timestamp

    def remove(self, element: T, timestamp: int) -> None:
        """
        Record a remove operation for `element` at `timestamp`.
        Keeps only the maximum remove timestamp for that element.
        """
        current = self.removes.get(element)
        if current is None or timestamp > current:
  ...
```

### Claude Opus 4.6

**Generation Time:** 35988ms
**Tokens:** 2126

```


# LWW-Element-Set CRDT Implementation

## Overview

A Last-Writer-Wins Element Set (LWW-Element-Set) is a state-based CRDT that maintains two internal sets: an **add set** and a **remove set**, each storing elements with associated timestamps. An element is considered in the set if it exists in the add set and either doesn't exist in the remove set, or its latest add timestamp is greater than or equal to its latest remove timestamp.

## Implementation

```python
"""
LWW-Element-Set CRDT (Last-Writer-Wins Element Set)

A state-based CRDT that resolves conflicts using timestamps.
Each element tracks its most recent add and remove timestamps.
The element is considered present if its add timestamp >= remove timestamp.

Bias: add-bias (element present when add timestamp == remove timestamp).
This is configurable via the `bias` parameter.
"""

from __future__ import annotations

import time
import copy
from enum import Enum
from typing import Any, Dict, Hashable, Optional, Set, Tuple


class Bias(Enum):
    """Determines winner when add and remove timestamps are equal."""
    ADD = "add"       # Element is considered present on tie
    REMOVE = "remove" # Element is considered absent on tie


class LWWElementSet:
    """
    Last-Writer-Wins Element Set CRDT.

    Maintains two internal dictionaries:
      - add_set:    {element: timestamp} — records the latest time each element was added
      - remove_set: {element: timestamp} — records the latest time each element was removed

    An element is a member of the set iff:
      - It exists in add_set, AND
      - Either it does NOT exist in remove_set,
        OR add_set[element] > remove_set[element]  (with >= for ADD bias)

    Properties guaranteed by the CRDT contract:
      - Merge is commutative:  A.merge(B) == B.merge(A)
      - Merge is associative:  A.merge(B).merge(C) == A.merge(B.merge(C))
      - Merge is idempotent:   A.merge(A) == A
    """

    def __init__(self, bias: Bias = Bias.ADD, replica_id: Optiona...
```

### Gemini 3.1 Pro

**Generation Time:** 26960ms
**Tokens:** 2102

```
Here is a complete guide to understanding and implementing a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python.

### 1. Python Implementation

The LWW-Element-Set maintains two internal dictionaries: an `add_set` and a `remove_set`. These dictionaries map elements to the timestamp of their most recent addition or removal. 

When looking up an element, we check both sets. If the add timestamp is strictly greater than the remove timestamp, the element is in the set. If the timestamps are exactly equal, we apply a predetermined bias (usually biased towards "add").

```python
from typing import Hashable, Dict, Set

class LWWElementSet:
    def __init__(self, bias: str = "add"):
        """
        Initializes the LWW-Element-Set.
        :param bias: "add" or "remove". Determines behavior when add and remove 
                     timestamps are exactly equal.
        """
        if bias not in ("add", "remove"):
            raise ValueError("Bias must be 'add' or 'remove'")
            
        self._adds: Dict[Hashable, float] = {}
        self._removes: Dict[Hashable, float] = {}
        self.bias = bias

    def add(self, element: Hashable, timestamp: float) -> None:
        """Adds an element to the set with a given timestamp."""
        current_ts = self._adds.get(element)
        if current_ts is None or timestamp > current_ts:
            self._adds[element] = timestamp

    def remove(self, element: Hashable, timestamp: float) -> None:
        """Removes an element from the set with a given timestamp."""
        current_ts = self._removes.get(element)
        if current_ts is None or timestamp > current_ts:
            self._rem
```

### Claude Sonnet 4.6

**Generation Time:** 34973ms
**Tokens:** 2126

```
# Last-Writer-Wins Element Set (LWW-Element-Set) CRDT

## Implementation

```python
"""
LWW-Element-Set CRDT Implementation
=====================================
A Last-Writer-Wins Element Set maintains two grow-only sets:
  - add_set:    {element -> timestamp}  (latest add timestamp)
  - remove_set: {element -> timestamp}  (latest remove timestamp)

Lookup rule: element is IN the set if:
  add_timestamp > remove_timestamp  (or element only in add_set)

This gives "remove-wins" on tie by using strict greater-than.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Timestamp abstraction
# ---------------------------------------------------------------------------

def now() -> float:
    """Monotonic wall-clock timestamp with sub-microsecond resolution."""
    return time.time()


# ---------------------------------------------------------------------------
# Core LWW-Element-Set
# ---------------------------------------------------------------------------

@dataclass
class LWWElementSet:
    """
    Last-Writer-Wins Element Set CRDT.

    Internal state
    --------------
    add_set    : dict[element, float]  – highest timestamp of any add
    remove_set : dict[element, float]  – highest timestamp of any remove

    The 'bias' parameter controls tie-breaking:
      'add'    – element is present when timestamps are equal
      'remove' – element is absent  when timestamps are equal  (default)
    """

    bias: str = "remove"                          # "add" | "remove"
    add_set: Dict[Any, float] = field(default_factory=dict)
    remove_set: Dict[Any, float] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def _record_add(self...
```

### DeepSeek V3

**Generation Time:** 160634ms
**Tokens:** 2025

```
# Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python

Here's an implementation of a LWW-Element-Set CRDT with the required operations, along with tests and proofs of its properties.

```python
import uuid
import time
from typing import Dict, Set, Optional, Tuple

class LWWElementSet:
    def __init__(self):
        # Dictionary to store added elements with their timestamps
        self.add_set: Dict[str, float] = {}
        # Dictionary to store removed elements with their timestamps
        self.remove_set: Dict[str, float] = {}
    
    def add(self, element: str, timestamp: Optional[float] = None) -> None:
        """Add an element to the set with the current timestamp."""
        ts = timestamp if timestamp is not None else time.time()
        
        # Only add if the element is not in add_set or new timestamp is greater
        if element not in self.add_set or ts > self.add_set[element]:
            self.add_set[element] = ts
    
    def remove(self, element: str, timestamp: Optional[float] = None) -> None:
        """Remove an element from the set with the current timestamp."""
        ts = timestamp if timestamp is not None else time.time()
        
        # Only remove if the element is in add_set and not already removed with a later timestamp
        if element in self.add_set and (element not in self.remove_set or ts > self.remove_set[element]):
            self.remove_set[element] = ts
    
    def lookup(self, element: str) -> bool:
        """Check if an element is in the set.
        An element is in the set if it's in add_set and:
        - not in remove_set, or
        - in remove_set but with an earlier timestamp than in add_set
        """
        in_add = element in self.add_set
        in_remove = element in self.remove_set
        
        if not in_add:
            return False
        if not in_remove:
            return True
        return self.add_set[element] > self.remove_set[element]
    
    def get_elements(self) -> Set[...
```

### GPT-OSS-120B

**Generation Time:** 18789ms
**Tokens:** 2188

```
## LWW‑Element‑Set CRDT  

A **Last‑Writer‑Wins Element Set** (LWW‑Element‑Set) is a **state‑based** (a.k.a. convergent) CRDT that stores two maps  

* **A** – “add‑set”  : `element → timestamp`  
* **R** – “remove‑set”: `element → timestamp`  

For every element we keep the *most recent* operation (add or remove).  
The element is considered present **iff**

```
timestamp_in_A > timestamp_in_R     (or the element is never removed)
```

Because the merge operation is defined as a **pair‑wise maximum** of timestamps, the set is **monotonic** (it never loses information) and all replicas that exchange their state eventually converge to the same set.

---

## 1.  Implementation  

```python
"""
lww_element_set.py

Implementation of a Last‑Writer‑Wins Element Set CRDT.

Features
--------
* add(element, ts=None)      – add an element with a timestamp.
* remove(element, ts=None)   – remove an element with a timestamp.
* lookup(element) -> bool    – true iff the element is currently in the set.
* merge(other)               – merge another replica into this one.
* elements() -> set          – the current logical contents of the set.

The timestamp is a comparable value (e.g. int, float, datetime).  If omitted,
the current UTC time (as a float) is used.  Supplying timestamps explicitly
makes the CRDT deterministic for unit‑testing.
"""

import time
from typing import Dict, Generic, Hashable, Optional, Set, TypeVar

T = TypeVar("T", bound=Hashable)


class LWWElementSet(Generic[T]):
    """
    Last‑Writer‑Wins Element Set CRDT.

    Internally we keep two dictionaries:
        _adds    : element → timestamp of the latest add
        _removes : element → timestamp of the latest remove
    """

    __slots__ = ("_adds", "_removes")

    def __init__(self) -> None:
        self._adds: Dict[T, float] = {}
        self._removes: Dict[T, float] = {}

    # --------------------------------------------------------------------- #
    # Helper – obtain a timestamp --------------------...
```

### Gemini 3 Flash Preview

**Generation Time:** 17146ms
**Tokens:** 1552

```
This implementation provides a **Last-Writer-Wins Element Set (LWW-Element-Set)**, a state-based CRDT where each element in the set is associated with a timestamp.

### 1. Implementation

```python
import time
from typing import Any, Dict, Set

class LWWElementSet:
    def __init__(self):
        # Maps element -> timestamp
        self.add_set: Dict[Any, float] = {}
        self.remove_set: Dict[Any, float] = {}

    def add(self, element: Any, timestamp: float = None):
        """Adds an element with a given timestamp (defaults to current time)."""
        ts = timestamp if timestamp is not None else time.time()
        # Only update if the new timestamp is higher
        if ts > self.add_set.get(element, -float('inf')):
            self.add_set[element] = ts

    def remove(self, element: Any, timestamp: float = None):
        """Removes an element with a given timestamp (defaults to current time)."""
        ts = timestamp if timestamp is not None else time.time()
        # Only update if the new timestamp is higher
        if ts > self.remove_set.get(element, -float('inf')):
            self.remove_set[element] = ts

    def lookup(self, element: Any) -> bool:
        """
        An element is in the set if it's in the add_set AND
        (not in remove_set OR add_timestamp > remove_timestamp).
        Bias is towards removal in case of equal timestamps.
        """
        if element not in self.add_set:
            return False
        
        add_ts = self.add_set[element]
        remove_ts = self.remove_set.get(element, -float('inf'))
        
        # LWW logic: element exists if added more recently than removed
        return add_ts > remove_ts

    def get_elements(self) -> Set[Any]:
        """Returns all elements currently in the set."""
        return {el for el in self.add_set if self.lookup(el)}

    def merge(self, other: 'LWWElementSet'):
        """Merges another LWW-Element-Set into this one."""
        # Merge Add Sets: for each key, take the...
```

### MiniMax M2.5

**Generation Time:** 45347ms
**Tokens:** 2148

```

```

### MiMo-V2-Flash

**Generation Time:** 23147ms
**Tokens:** 2148

```
Here is a complete implementation of a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python, including the mathematical proof of convergence properties and a test suite demonstrating conflict resolution.

### 1. Python Implementation

We use a `NamedTuple` for the timestamped operations to ensure immutability and type safety.

```python
import time
from typing import Any, Dict, List, Set, Tuple, NamedTuple, Optional

# A simple logical clock representation (float for simplicity, could be (timestamp, node_id))
Timestamp = float

class Operation(NamedTuple):
    """
    Represents a single add or remove operation with a timestamp.
    """
    element: Any
    timestamp: Timestamp
    is_add: bool  # True for add, False for remove

class LWWElementSet:
    def __init__(self):
        # Maps element -> (add_timestamp, remove_timestamp)
        self._store: Dict[Any, Tuple[Timestamp, Timestamp]] = {}

    def add(self, element: Any, timestamp: Optional[Timestamp] = None):
        """
        Adds an element at a specific timestamp. 
        If no timestamp is provided, the current system time is used.
        """
        if timestamp is None:
            timestamp = time.time()

        if element not in self._store:
            self._store[element] = (timestamp, 0.0)
        else:
            curr_add, curr_rem = self._store[element]
            # Only update if this add is newer than the existing add
            if timestamp > curr_add:
                self._store[element] = (timestamp, curr_rem)

    def remove(self, element: Any, timestamp: Optional[Timestamp] = None):
        """
        Removes an element at a specific timestamp.
        """
        if timestamp is None:
            timestamp = time.time()

        if element not in self._store:
            # If element never existed, we record the remove anyway
            # (in case a concurrent add arrives later with a lower timestamp)
            self._store[element] = (0.0, timestamp)
        else:
  ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*