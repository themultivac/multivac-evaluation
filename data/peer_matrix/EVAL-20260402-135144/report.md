# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-135144
**Timestamp:** 2026-04-02T13:51:44.778541
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a minimal but correct event sourcing system in Python. Include: an Event base class, an EventStore (in-memory is fine), an Aggregate base class that rebuilds state from events, a BankAccount aggregate with deposit/withdraw/transfer commands, and snapshot support for performance. Demonstrate eventual consistency between two projections.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 7.72 | 6.40 | 9.45 | 1.07 |
| 2 | Gemini 3 Flash Preview | 7.41 | 6.00 | 9.60 | 1.25 |
| 3 | GPT-OSS-120B | 7.33 | 3.50 | 9.45 | 1.95 |
| 4 | Claude Opus 4.6 | 7.22 | 3.65 | 9.60 | 2.32 |
| 5 | GPT-5.4 | 6.84 | 4.60 | 8.60 | 1.53 |
| 6 | Claude Sonnet 4.6 | 6.75 | 3.25 | 9.60 | 2.06 |
| 7 | DeepSeek V3 | 6.19 | 4.20 | 8.55 | 1.46 |
| 8 | MiMo-V2-Flash | 6.13 | 2.05 | 9.60 | 2.17 |
| 9 | MiniMax M2.5 | 3.76 | 1.65 | 7.80 | 2.08 |
| 10 | Gemini 3.1 Pro | 3.25 | 0.85 | 8.80 | 3.05 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.54 |
| 2 | GPT-OSS-120B | 4.94 |
| 3 | Claude Opus 4.6 | 5.08 |
| 4 | Gemini 3.1 Pro | 5.22 |
| 5 | MiniMax M2.5 | 6.11 |
| 6 | Grok 4.20 | 6.33 |
| 7 | Claude Sonnet 4.6 | 6.38 |
| 8 | Gemini 3 Flash Preview | 7.74 |
| 9 | MiMo-V2-Flash | 8.28 |
| 10 | DeepSeek V3 | 8.97 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 90

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

**Generation Time:** 25830ms
**Tokens:** 2118

```
```python
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Type
from collections import defaultdict
import uuid


# =========================
# Events
# =========================

@dataclass(frozen=True)
class Event:
    aggregate_id: str
    version: int


@dataclass(frozen=True)
class AccountOpened(Event):
    owner: str


@dataclass(frozen=True)
class Deposited(Event):
    amount: int


@dataclass(frozen=True)
class Withdrawn(Event):
    amount: int


@dataclass(frozen=True)
class TransferredOut(Event):
    to_account_id: str
    amount: int
    transfer_id: str


@dataclass(frozen=True)
class TransferredIn(Event):
    from_account_id: str
    amount: int
    transfer_id: str


# =========================
# Snapshot
# =========================

@dataclass
class Snapshot:
    aggregate_id: str
    version: int
    state: Dict[str, Any]


# =========================
# Event Store
# =========================

class ConcurrencyError(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class EventStore:
    def __init__(self) -> None:
        self._streams: Dict[str, List[Event]] = defaultdict(list)
        self._all_events: List[Event] = []
        self._snapshots: Dict[str, Snapshot] = {}

    def load_stream(self, aggregate_id: str, after_version: int = 0) -> List[Event]:
        return [e for e in self._streams[aggregate_id] if e.version > after_version]

    def append(
        self,
        aggregate_id: str,
        expected_version: int,
        new_events: List[Event],
    ) -> None:
        stream = self._streams[aggregate_id]
        current_version = stream[-1].version if stream else 0
        if current_version != expected_version:
            raise ConcurrencyError(
                f"Expected version {expected_version}, got {current_version}"
            )

        next_version = current_version
        for e in new_events:
            next_version += 1
...
```

### Claude Opus 4.6

**Generation Time:** 118068ms
**Tokens:** 2125

```


# Event Sourcing System in Python

## Complete Implementation

```python
"""
A minimal but correct Event Sourcing system with:
- Event base class with metadata
- In-memory EventStore with optimistic concurrency
- Aggregate base class with state rebuild from events
- BankAccount aggregate with deposit/withdraw/transfer
- Snapshot support for performance
- Eventual consistency demonstration between projections
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type


# =============================================================================
# EVENTS
# =============================================================================

@dataclass(frozen=True)
class Event:
    """
    Base event class. All events are immutable records of something that happened.
    
    Frozen dataclass ensures immutability - events are facts that cannot change.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    aggregate_id: str = ""
    aggregate_type: str = ""
    version: int = 0  # Position in the aggregate's event stream

    def to_dict(self) -> dict:
        """Serialize event to dictionary for storage."""
        data = {}
        for f in self.__dataclass_fields__:
            val = getattr(self, f)
            if isinstance(val, Enum):
                data[f] = val.value
            else:
                data[f] = val
        data["_event_type"] = self.__class__.__name__
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        """Deserialize event from dictionary."""
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        re...
```

### Gemini 3.1 Pro

**Generation Time:** 32814ms
**Tokens:** 2109

```
Here is a complete, minimal, and correct implementation of an Event Sourcing system in Python. 

It includes the **Event** and **Aggregate** base classes, a **BankAccount** aggregate, an in-memory **EventStore** with **Snapshot** support, and an **Event Bus** that updates two different read-model **Projections** asynchronously to demonstrate eventual consistency.

### The Implementation
```

### Claude Sonnet 4.6

**Generation Time:** 33826ms
**Tokens:** 2124

```
```python
"""
Minimal but correct Event Sourcing system in Python.

Architecture:
    Commands → Aggregate → Events → EventStore → Projections
    
Includes:
    - Event base class with metadata
    - EventStore with optimistic concurrency control
    - Aggregate base class with event replay
    - Snapshot support
    - BankAccount aggregate (deposit/withdraw/transfer)
    - Two projections demonstrating eventual consistency
"""

from __future__ import annotations

import uuid
import time
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Generator, Optional, TypeVar

# ---------------------------------------------------------------------------
# Core domain primitives
# ---------------------------------------------------------------------------

def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

@dataclass
class Event:
    """
    Base class for all domain events.
    
    Every event carries:
        - event_id:       globally unique identifier
        - aggregate_id:   which aggregate produced this event
        - aggregate_type: class name of the aggregate
        - version:        monotonically increasing per-aggregate sequence number
        - occurred_on:    wall-clock time the event was created
        - metadata:       arbitrary key/value bag (correlation ids, causation, etc.)
    """
    aggregate_id: str
    aggregate_type: str
    version: int                              # 1-based, increments per aggregate
    occurred_on: datetime = field(default_factory=utcnow)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self...
```

### Grok 4.20

**Generation Time:** 10450ms
**Tokens:** 2233

```
**Here's a minimal but correct Event Sourcing implementation in Python:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
import json
import uuid

# =============================================
# 1. Event Base
# =============================================

T = TypeVar('T')


@dataclass
class Event(ABC):
    """Base class for all domain events"""
    event_id: str
    aggregate_id: str
    version: int
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['event_type'] = self.__class__.__name__
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        # Remove metadata before constructing
        clean = {k: v for k, v in data.items() 
                if k not in ('event_type', 'event_id', 'aggregate_id', 'version', 'timestamp')}
        return cls(
            event_id=data.get('event_id', str(uuid.uuid4())),
            aggregate_id=data['aggregate_id'],
            version=data['version'],
            timestamp=data.get('timestamp', datetime.now()),
            **clean
        )


# =============================================
# 2. Event Store (In-memory)
# =============================================

class EventStore:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}
        self._snapshots: Dict[str, Dict[int, Dict]] = {}

    def append(self, event: Event) -> None:
        if event.aggregate_id not in self._events:
            self._events[event.aggregate_id] = []
        
        # Simple optimistic concurrency check
        current_events = self._events[event.aggregate_id]
        if current_events and current_events[-1].version >= event.version:
            raise ConcurrencyError(f"Version conflict for aggregate {event.aggregate_id}")
        
        self._events[event.aggregate_id].append(even...
```

### DeepSeek V3

**Generation Time:** 45257ms
**Tokens:** 2117

```
# Minimal Event Sourcing System in Python

Here's a complete implementation of an event sourcing system with all the requested features:

```python
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Type, Optional, Callable, Any, TypeVar, Generic, Tuple


# Type Variables for generics
T = TypeVar('T')
E = TypeVar('E', bound='Event')
A = TypeVar('A', bound='Aggregate')


# Base Classes
class Event(ABC):
    event_id: str
    aggregate_id: str
    timestamp: datetime

    def __init__(self, aggregate_id: str):
        self.event_id = str(uuid.uuid4())
        self.aggregate_id = aggregate_id
        self.timestamp = datetime.now()

    @abstractmethod
    def apply(self, aggregate: 'Aggregate') -> None:
        pass


class Aggregate(ABC):
    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        self.version = 0
        self._changes: List[Event] = []

    @classmethod
    def replay_events(cls, aggregate_id: str, events: List[Event]) -> 'Aggregate':
        aggregate = cls(aggregate_id)
        for event in events:
            event.apply(aggregate)
            aggregate.version += 1
        return aggregate

    def apply_change(self, event: Event) -> None:
        event.apply(self)
        self._changes.append(event)

    def get_uncommitted_changes(self) -> List[Event]:
        return self._changes

    def clear_uncommitted_changes(self) -> None:
        self._changes = []


class EventStore:
    def __init__(self):
        self._store: Dict[str, List[Event]] = {}
        self._snapshots: Dict[str, Tuple[Aggregate, int]] = {}
        self._projections: Dict[str, Callable[[Event], None]] = {}

    def save(self, aggregate: Aggregate) -> None:
        changes = aggregate.get_uncommitted_changes()
        if aggregate.id not in self._store:
            self._store[aggregate.id] = []
        self._store[aggregate.id].extend(changes)
        aggregate.c...
```

### GPT-OSS-120B

**Generation Time:** 12974ms
**Tokens:** 2190

```
Below is a **complete, self‑contained** example of a tiny event‑sourcing toolbox written in pure Python.  
It contains

* an `Event` base class and a few concrete events,
* an **in‑memory** `EventStore` (with snapshot support),
* an `AggregateRoot` base class that can **re‑play** its own events,
* a `BankAccount` aggregate that supports **deposit / withdraw / transfer** commands,
* a simple **snapshot** mechanism to avoid replaying the whole event stream,
* two **projections** (`BalanceProjection` and `TransactionProjection`) that are updated asynchronously, demonstrating **eventual consistency**.

You can copy‑paste the whole file into a single `event_sourcing_demo.py` and run it with Python 3.10+.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Minimal event‑sourcing system in Python.

Features
--------
* Event base class + concrete events.
* In‑memory EventStore (append‑only, versioned per aggregate).
* Snapshot store (in‑memory) for fast re‑hydration.
* AggregateRoot base class that knows how to apply events.
* BankAccount aggregate with deposit / withdraw / transfer commands.
* Two read‑model projections that are updated asynchronously,
  showing eventual consistency.
"""

from __future__ import annotations
import dataclasses
import datetime as dt
import json
import uuid
import threading
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, TypeVar

# ----------------------------------------------------------------------
# 1.  Event model
# ----------------------------------------------------------------------


class Event:
    """
    Base class for all domain events.

    Every event carries:
    * `aggregate_id` – the UUID of the aggregate that produced it,
    * `version`      – the aggregate version **after** the event was applied,
    * `timestamp`    – when the event happened (UTC),
    * any payload defined by subclasses.
    """

    def __init__(self, aggregate_id: uuid.UUID, version: int):
        self.agg...
```

### Gemini 3 Flash Preview

**Generation Time:** 12620ms
**Tokens:** 1777

```
This implementation provides a clean, minimal foundation for Event Sourcing in Python.

### 1. Core Architecture

```python
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Type, Optional

# --- Base Classes ---

@dataclass(frozen=True)
class Event:
    aggregate_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 0

class Aggregate:
    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        self.version = 0
        self.changes: List[Event] = []

    def apply(self, event: Event):
        """Updates internal state and increments version."""
        method_name = f"on_{type(event).__name__.lower()}"
        method = getattr(self, method_name, None)
        if method:
            method(event)
        self.version = event.version

    def apply_new(self, event: Event):
        """Used for new commands to track changes."""
        self.version += 1
        new_event = dataclass_replace(event, version=self.version)
        self.apply(new_event)
        self.changes.append(new_event)

def dataclass_replace(obj, **kwargs):
    from dataclasses import replace
    return replace(obj, **kwargs)

# --- Event Store & Snapshots ---

class EventStore:
    def __init__(self):
        self._storage: Dict[str, List[Event]] = {}
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self._subscribers = []

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def save(self, aggregate: Aggregate):
        if aggregate.id not in self._storage:
            self._storage[aggregate.id] = []
        
        for event in aggregate.changes:
            self._storage[aggregate.id].append(event)
            # Notify subscribers (for eventual consistency)
            for sub in self._subscribers:
                sub(event)
        
        aggregate.changes = []

    def save_snapshot(self, aggregate: Aggregate):
  ...
```

### MiniMax M2.5

**Generation Time:** 103020ms
**Tokens:** 2150

```
Here is a complete, minimal, and correct implementation of an Event Sourcing system in Python.

It includes:
1.  **Event Store**: Handles persistence and **Snapshots**.
2.  **Aggregate Root**: Handles state reconstruction and uncommitted events.
3.  **Bank Account**: specific domain logic with Deposit, Withdraw, and Transfer.
4.  **Projections**: Demonstrates **Eventual Consistency** by building two different read models from the same event stream.

### The Implementation

```python
import uuid
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

# ==========================================
# 1. The Event Model
# ==========================================

class Event:
    """Base class for all events."""
    def __init__(self, aggregate_id: str, payload: dict):
        self.id = str(uuid.uuid4())
        self.aggregate_id = aggregate_id
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.payload = payload

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        # Simple factory logic for demo purposes
        # In a real system, you'd use a registry of event types
        cls_name = data['payload'].get('type', 'Event')
        # Re-instantiate the specific class would go here, 
        # for now we return a generic
```

### MiMo-V2-Flash

**Generation Time:** 17916ms
**Tokens:** 2149

```
Here is a complete, minimal, yet correct implementation of an Event Sourcing system in Python.

This implementation includes:
1.  **Core Classes**: `Event`, `EventStore`, `Aggregate`.
2.  **Domain Model**: `BankAccount` with commands and business logic.
3.  **Snapshots**: To optimize replay performance.
4.  **Projections**: Read models for querying data.
5.  **Demonstration**: A script showing command execution, snapshotting, and eventual consistency between two separate projections.

```python
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Type, Callable
from datetime import datetime
from copy import deepcopy

# ==========================================
# 1. Core Event Sourcing Infrastructure
# ==========================================

@dataclass
class Event:
    """Base class for all domain events."""
    aggregate_id: str
    version: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

class EventStore:
    """In-memory store for events and snapshots."""
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}
        self._snapshots: Dict[str, Dict[str, Any]] = {}

    def save_events(self, aggregate_id: str, events: List[Event], expected_version: int):
        """Append new events to the stream."""
        if aggregate_id not in self._events:
            self._events[aggregate_id] = []
        
        # Optimistic concurrency check
        current_version = len(self._events[aggregate_id])
        if current_version != expected_version:
            raise ValueError(f"Version mismatch for {aggregate_id}. Expected {expected_version}, got {current_version}")

        self._events[aggregate_id].extend(events)

    def get_events(self, aggregate_id: str) -> List[Event]:
        return self._events.get(aggregate_id, [])

    def save_snapshot(self, aggregate_id: str, state: Dict[str, Any]):
  ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*