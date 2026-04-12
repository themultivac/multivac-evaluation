# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-085232
**Timestamp:** 2026-04-03T08:52:32.440539
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python. It should support add, remove, lookup, and merge operations. Include a proof that merge is commutative, associative, and idempotent. Write tests demonstrating conflict resolution between two divergent replicas.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.23 | 8.80 | 10.00 | 0.45 |
| 2 | Gemini 3 Flash Preview | 8.89 | 8.00 | 9.80 | 0.58 |
| 3 | MiMo-V2-Flash | 8.44 | 6.70 | 9.80 | 0.94 |
| 4 | DeepSeek V3 | 8.39 | 7.00 | 9.80 | 0.85 |
| 5 | Grok 4.20 | 8.06 | 6.00 | 9.80 | 1.29 |
| 6 | GPT-OSS-120B | 7.23 | 2.85 | 10.00 | 2.31 |
| 7 | Claude Sonnet 4.6 | 6.91 | 3.25 | 9.25 | 1.86 |
| 8 | Claude Opus 4.6 | 6.87 | 3.05 | 9.60 | 2.32 |
| 9 | Gemini 3.1 Pro | 3.86 | 1.65 | 6.35 | 1.64 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.95 |
| 2 | GPT-OSS-120B | 6.78 |
| 3 | Claude Opus 4.6 | 6.79 |
| 4 | MiniMax M2.5 | 7.12 |
| 5 | Claude Sonnet 4.6 | 7.63 |
| 6 | Gemini 3.1 Pro | 7.78 |
| 7 | Grok 4.20 | 8.08 |
| 8 | MiMo-V2-Flash | 8.57 |
| 9 | Gemini 3 Flash Preview | 8.78 |
| 10 | DeepSeek V3 | 8.84 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 79

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

**Generation Time:** 23509ms
**Tokens:** 2116

```
```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, Optional, TypeVar
import time
import unittest


T = TypeVar("T")


@dataclass
class LWWElementSet(Generic[T]):
    """
    Last-Writer-Wins Element Set CRDT.

    Each element may appear in:
      - add_set[element] = timestamp of latest add
      - remove_set[element] = timestamp of latest remove

    Membership rule:
      element is present iff add_ts exists and
      (remove_ts does not exist or add_ts > remove_ts)

    Tie-break policy:
      If add_ts == remove_ts, remove wins by default.
    """
    add_set: Dict[T, float] = field(default_factory=dict)
    remove_set: Dict[T, float] = field(default_factory=dict)

    def add(self, element: T, timestamp: Optional[float] = None) -> None:
        ts = time.time() if timestamp is None else timestamp
        current = self.add_set.get(element)
        if current is None or ts > current:
            self.add_set[element] = ts

    def remove(self, element: T, timestamp: Optional[float] = None) -> None:
        ts = time.time() if timestamp is None else timestamp
        current = self.remove_set.get(element)
        if current is None or ts > current:
            self.remove_set[element] = ts

    def lookup(self, element: T) -> bool:
        add_ts = self.add_set.get(element)
        if add_ts is None:
            return False
        remove_ts = self.remove_set.get(element)
        if remove_ts is None:
            return True
        return add_ts > remove_ts

    def elements(self) -> set[T]:
        return {e for e in self.add_set if self.lookup(e)}

    def merge(self, other: "LWWElementSet[T]") -> "LWWElementSet[T]":
        """
        Merge by taking pointwise maximum timestamp for both add and remove maps.
        """
        merged_add = dict(self.add_set)
        for element, ts in other.add_set.items():
            if element not in merged_add or ts > merged_add[element]:
 ...
```

### Claude Opus 4.6

**Generation Time:** 84796ms
**Tokens:** 2126

```


# LWW-Element-Set CRDT Implementation

## Overview

A Last-Writer-Wins Element Set (LWW-Element-Set) is a state-based CRDT that maintains two internal sets: an **add set** and a **remove set**, each storing elements with timestamps. An element is considered in the set if it exists in the add set and either doesn't exist in the remove set, or its latest add timestamp is greater than or equal to its latest remove timestamp.

## Implementation

```python
"""
LWW-Element-Set CRDT (Last-Writer-Wins Element Set)

A state-based CRDT that resolves conflicts using timestamps.
Each element is associated with a timestamp in both an add-set and a remove-set.
The element is considered present if its latest add timestamp >= its latest remove timestamp.

Bias: add-bias (ties go to "present"). This is configurable.
"""

from __future__ import annotations

import copy
import time
from enum import Enum, auto
from typing import Any, Dict, FrozenSet, Hashable, Optional, Set, TypeVar

T = TypeVar("T", bound=Hashable)


class Bias(Enum):
    """Determines conflict resolution when add and remove timestamps are equal."""
    ADD = auto()     # Element is considered present on tie
    REMOVE = auto()  # Element is considered absent on tie


class LWWElementSet:
    """
    Last-Writer-Wins Element Set CRDT.

    Internally maintains two dictionaries:
        - add_set:    {element -> timestamp} tracking the latest add time
        - remove_set: {element -> timestamp} tracking the latest remove time

    An element is in the logical set iff:
        - It exists in add_set, AND
        - Either it does NOT exist in remove_set, OR
        - Its add timestamp beats its remove timestamp (with bias breaking ties)

    Properties (proven below):
        - merge is commutative:  A.merge(B) == B.merge(A)
        - merge is associative:  A.merge(B).merge(C) == A.merge(B.merge(C))
        - merge is idempotent:   A.merge(A) == A
    """

    def __init__(self, bias: Bias = Bias.ADD, replica_id: Opti...
```

### Gemini 3.1 Pro

**Generation Time:** 19691ms
**Tokens:** 2102

```
Here is a complete implementation of a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python, followed by the mathematical proof of its merge properties, and a comprehensive test suite demonstrating conflict resolution.

### Python Implementation

```python
class LWWElementSet:
    """
    A Last-Writer-Wins Element Set (LWW-Element-Set) CRDT.
    Uses 'Add-Wins' bias in the event of identical timestamps.
    """
    def __init__(self):
        # Dictionaries mapping element -> timestamp
        self._adds = {}
        self._removes = {}

    def add(self, element, timestamp):
        """Adds an element to the set with a given timestamp."""
        # Only update if the new timestamp is strictly greater
        if element not in self._adds or timestamp > self._adds[element]:
            self._adds[element] = timestamp

    def remove(self, element, timestamp):
        """Removes an element from the set with
```

### Claude Sonnet 4.6

**Generation Time:** 26737ms
**Tokens:** 2126

```
# Last-Writer-Wins Element Set (LWW-Element-Set) CRDT

## Implementation

```python
"""
Last-Writer-Wins Element Set (LWW-Element-Set) CRDT Implementation

An LWW-Element-Set maintains two grow-only sets (G-Sets):
  - add_set: {element -> timestamp} — records the latest add timestamp
  - remove_set: {element -> timestamp} — records the latest remove timestamp

An element is considered IN the set if:
  add_set[element] > remove_set.get(element, -∞)

This gives us Last-Writer-Wins semantics: the most recent operation wins.
"""

import time
import copy
import unittest
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Timestamp abstraction (monotonic float; swap for Hybrid Logical Clock, etc.)
# ---------------------------------------------------------------------------

def now() -> float:
    """Return a monotonically increasing wall-clock timestamp."""
    return time.monotonic()


# ---------------------------------------------------------------------------
# Core LWW-Element-Set
# ---------------------------------------------------------------------------

@dataclass
class LWWElementSet:
    """
    Last-Writer-Wins Element Set CRDT.

    Internal state
    --------------
    add_set    : dict[element, float]  — element → latest add-timestamp
    remove_set : dict[element, float]  — element → latest remove-timestamp

    Bias
    ----
    When add_ts == remove_ts we must break the tie deterministically.
    `bias='add'`    → element is considered present  (add wins ties)
    `bias='remove'` → element is considered absent   (remove wins ties)
    """

    bias: str = "add"                              # 'add' or 'remove'
    add_set: Dict[Any, float] = field(default_factory=dict)
    remove_set: Dict[Any, float] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Validation
    # -------...
```

### Grok 4.20

**Generation Time:** 6207ms
**Tokens:** 1705

```
**LWW-Element-Set CRDT Implementation**

```python
from dataclasses import dataclass
from typing import Set, Tuple, Dict, Any
import time


@dataclass(eq=True, frozen=True)
class TimestampedEntry:
    timestamp: float
    is_add: bool      # True = add, False = remove


class LWElementSet:
    """
    Last-Writer-Wins Element Set CRDT.
    """
    
    def __init__(self):
        self.add_set: Dict[Any, float] = {}      # element -> timestamp of last add
        self.remove_set: Dict[Any, float] = {}   # element -> timestamp of last remove
    
    def add(self, element: Any) -> None:
        """Add an element with current wall-clock timestamp."""
        ts = time.time()
        self.add_set[element] = ts
        # Clean up any older remove if this add wins
        if element in self.remove_set and self.remove_set[element] < ts:
            del self.remove_set[element]
    
    def remove(self, element: Any) -> None:
        """Remove an element with current wall-clock timestamp."""
        ts = time.time()
        self.remove_set[element] = ts
        # Clean up any older add if this remove wins
        if element in self.add_set and self.add_set[element] < ts:
            del self.add_set[element]
    
    def lookup(self, element: Any) -> bool:
        """
        Returns True if the element is in the set.
        An element is present if it was added and the latest operation is an add.
        """
        add_ts = self.add_set.get(element, 0.0)
        rem_ts = self.remove_set.get(element, 0.0)
        return add_ts > rem_ts
    
    def merge(self, other: 'LWElementSet') -> None:
        """
        Merge another LWW-Element-Set into this one.
        For each element, we keep the operation with the highest timestamp.
        """
        # Merge add timestamps
        for elem, ts in other.add_set.items():
            if elem not in self.add_set or ts > self.add_set[elem]:
                self.add_set[elem] = ts
        
        # Merge remove timestamps
     ...
```

### DeepSeek V3

**Generation Time:** 54047ms
**Tokens:** 2111

```
# Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python

Below is a Python implementation of a LWW-Element-Set CRDT with the required operations, along with proofs of the merge operation properties and test cases.

```python
import time
from typing import Dict, Set, Tuple, TypeVar

T = TypeVar('T')

class LWWElementSet:
    """
    A Last-Writer-Wins Element Set (LWW-Element-Set) CRDT implementation.
    
    The set supports add, remove, lookup, and merge operations. Conflicts are
    resolved by keeping the operation (add or remove) with the latest timestamp.
    """
    
    def __init__(self):
        # Dictionary to store add timestamps for elements
        self.add_set: Dict[T, float] = {}
        # Dictionary to store remove timestamps for elements
        self.remove_set: Dict[T, float] = {}
    
    def add(self, element: T, timestamp: float = None) -> None:
        """
        Add an element to the set.
        
        Args:
            element: The element to add
            timestamp: Optional timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Only update if this is a newer add operation
        if element not in self.add_set or timestamp > self.add_set[element]:
            self.add_set[element] = timestamp
    
    def remove(self, element: T, timestamp: float = None) -> None:
        """
        Remove an element from the set.
        
        Args:
            element: The element to remove
            timestamp: Optional timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Only update if this is a newer remove operation
        if element not in self.remove_set or timestamp > self.remove_set[element]:
            self.remove_set[element] = timestamp
    
    def lookup(self, element: T) -> bool:
        """
        Check if an element is in the set.
        
        An element is...
```

### GPT-OSS-120B

**Generation Time:** 46757ms
**Tokens:** 2179

```
Below is a **complete, self‑contained implementation** of a **Last‑Writer‑Wins Element Set (LWW‑Element‑Set)** CRDT in Python 3.8+.  
The implementation follows the classic design described in “A comprehensive study of Convergent and Commutative Replicated Data Types” (Shapiro et al., 2011).

* **Two internal maps** – `add_set` and `remove_set` – store, for each element, the **timestamp** (and replica identifier) of the last *add* or *remove* operation.  
* The **timestamp** is a totally ordered pair `(ts, replica_id)`. Python’s tuple ordering gives us the required “last‑writer‑wins” semantics: a later `ts` wins; if timestamps are equal the replica id breaks the tie deterministically.  
* **merge** simply takes the per‑element maximum of the two maps – the classic LWW‑merge.  

After the code you will find a **formal proof** that the merge operation is **commutative, associative, and idempotent**, followed by a **test‑suite** that demonstrates conflict resolution between two divergent replicas.

---

## 1. Implementation

```python
"""
lww_element_set.py

A Python implementation of the Last‑Writer‑Wins Element Set (LWW‑Element‑Set) CRDT.

Features
--------
* add(element, timestamp=None)          – registers an add‑operation.
* remove(element, timestamp=None)       – registers a remove‑operation.
* lookup(element) -> bool                – tells whether the element is present.
* merge(other) -> LWWElementSet           – returns a new LWW‑Element‑Set that is the
                                            merge of self and other (the operation
                                            is also performed in‑place for convenience).

The class can be used with any hashable element type.  Timestamps are ordered
pairs ``(ts, replica_id)`` where ``ts`` is a numeric (e.g. ``int``) or a
``datetime`` value and ``replica_id`` is a string that uniquely identifies the
replica that generated the operation.  The tuple ordering gives a total order,
so the “last writer” is well defin...
```

### Gemini 3 Flash Preview

**Generation Time:** 11553ms
**Tokens:** 1564

```
This implementation follows the standard definition of a **Last-Writer-Wins Element Set (LWW-Element-Set)**. It maintains two internal dictionaries (the "Add Set" and the "Remove Set"), storing elements mapped to their highest observed timestamps.

### Python Implementation

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
        # Only update if the new timestamp is greater than what we already have
        if ts > self.add_set.get(element, -float('inf')):
            self.add_set[element] = ts

    def remove(self, element: Any, timestamp: float = None):
        """Removes an element with a given timestamp (defaults to current time)."""
        ts = timestamp if timestamp is not None else time.time()
        if ts > self.remove_set.get(element, -float('inf')):
            self.remove_set[element] = ts

    def lookup(self, element: Any) -> bool:
        """
        An element is in the set if it is in the add set and:
        1. It is not in the remove set, OR
        2. Its timestamp in the add set is > its timestamp in the remove set.
        (Bias: In case of equal timestamps, we treat it as removed).
        """
        if element not in self.add_set:
            return False
        
        add_ts = self.add_set[element]
        remove_ts = self.remove_set.get(element, -float('inf'))
        
        return add_ts > remove_ts

    def get_elements(self) -> Set[Any]:
        """Returns all elements currently in the set."""
        return {el for el in self.add_set if self.lookup(el)}

    def merge(self, other: 'LWWElementSet'):
        """Merges another LWW-Element-Set into this ...
```

### MiniMax M2.5

**Generation Time:** 28777ms
**Tokens:** 2145

```

```

### MiMo-V2-Flash

**Generation Time:** 15959ms
**Tokens:** 2148

```
Here is a complete implementation of a Last-Writer-Wins Element Set (LWW-Element-Set) CRDT in Python.

### 1. Implementation

The LWW-Element-Set maintains two internal sets:
1.  **Add Set**: Stores elements added along with their timestamps.
2.  **Remove Set**: Stores elements removed along with their timestamps.

An element is considered present in the set if the timestamp of its latest addition is strictly greater than the timestamp of its latest removal.

```python
import time
from typing import Any, Set, Tuple, Dict

class LWWElementSet:
    def __init__(self):
        # Stores element -> timestamp for additions
        self.add_set: Dict[Any, float] = {}
        # Stores element -> timestamp for removals
        self.remove_set: Dict[Any, float] = {}

    def add(self, element: Any, timestamp: float = None):
        """
        Adds an element to the set.
        If no timestamp is provided, the current system time is used.
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Only update if the new timestamp is later than the existing one
        current_ts = self.add_set.get(element, 0)
        if timestamp > current_ts:
            self.add_set[element] = timestamp

    def remove(self, element: Any, timestamp: float = None):
        """
        Removes an element from the set.
        If no timestamp is provided, the current system time is used.
        """
        if timestamp is None:
            timestamp = time.time()
            
        # Only update if the new timestamp is later than the existing one
        current_ts = self.remove_set.get(element, 0)
        if timestamp > current_ts:
            self.remove_set[element] = timestamp

    def lookup(self, element: Any) -> bool:
        """
        Returns True if the element is present in the set, False otherwise.
        An element is present if its latest add timestamp > latest remove timestamp.
        """
        add_ts = self.add_set.get(element, 0)
 ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*