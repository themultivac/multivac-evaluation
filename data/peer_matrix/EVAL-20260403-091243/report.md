# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-091243
**Timestamp:** 2026-04-03T09:12:43.592727
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Refactor this 'working but unmaintainable' code into clean, testable, well-structured code. Explain every design decision.

```python
def process(data, mode, flag1=False, flag2=True, output_type='json'):
    results = []
    for item in data:
        if mode == 'fast':
            if item.get('type') == 'A':
                val = item['value'] * 1.1 if flag1 else item['value']
                if val > 100:
                    if flag2:
                        results.append({'id': item['id'], 'val': val, 'status': 'high'})
                    else:
                        results.append({'id': item['id'], 'val': val * 0.9, 'status': 'adjusted'})
                else:
                    results.append({'id': item['id'], 'val': val, 'status': 'normal'})
            elif item.get('type') == 'B':
                val = item['value'] * 0.95
                results.append({'id': item['id'], 'val': val, 'status': 'discounted'})
            else:
                if flag1 and flag2:
                    results.append({'id': item['id'], 'val': 0, 'status': 'skip'})
        elif mode == 'careful':
            try:
                val = float(item.get('value', 0))
                if val < 0: raise ValueError('negative')
                results.append({'id': item['id'], 'val': val, 'status': 'validated'})
            except:
                results.append({'id': item['id'], 'val': 0, 'status': 'error'})
    if output_type == 'json':
        import json; return json.dumps(results)
    elif output_type == 'csv':
        return '\n'.join([f"{r['id']},{r['val']},{r['status']}" for r in results])
    return results
```

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.36 | 8.80 | 10.00 | 0.47 |
| 2 | MiMo-V2-Flash | 8.99 | 6.95 | 9.80 | 0.89 |
| 3 | Grok 4.20 | 8.73 | 6.30 | 9.80 | 1.10 |
| 4 | Gemini 3 Flash Preview | 8.71 | 7.20 | 9.60 | 0.70 |
| 5 | DeepSeek V3 | 8.42 | 5.75 | 9.80 | 1.14 |
| 6 | Claude Sonnet 4.6 | 8.04 | 5.05 | 9.80 | 1.61 |
| 7 | Claude Opus 4.6 | 7.67 | 3.70 | 9.60 | 1.95 |
| 8 | GPT-OSS-120B | 7.53 | 3.65 | 10.00 | 2.13 |
| 9 | Gemini 3.1 Pro | 3.75 | 0.85 | 8.60 | 2.17 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.93 |
| 2 | GPT-OSS-120B | 6.83 |
| 3 | Claude Opus 4.6 | 7.77 |
| 4 | MiniMax M2.5 | 7.82 |
| 5 | Gemini 3.1 Pro | 7.89 |
| 6 | Grok 4.20 | 8.05 |
| 7 | Claude Sonnet 4.6 | 8.28 |
| 8 | MiMo-V2-Flash | 8.72 |
| 9 | Gemini 3 Flash Preview | 8.93 |
| 10 | DeepSeek V3 | 9.59 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 80

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

**Generation Time:** 27865ms
**Tokens:** 2459

```
Below is a refactor that makes the code:

- easier to read
- easier to test
- easier to extend
- safer around invalid input
- clearer about responsibilities

---

# Refactored code

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable
import csv
import io
import json


class ProcessingMode(str, Enum):
    FAST = "fast"
    CAREFUL = "careful"


class OutputType(str, Enum):
    JSON = "json"
    CSV = "csv"
    RAW = "raw"


class Status(str, Enum):
    HIGH = "high"
    ADJUSTED = "adjusted"
    NORMAL = "normal"
    DISCOUNTED = "discounted"
    SKIP = "skip"
    VALIDATED = "validated"
    ERROR = "error"


@dataclass(frozen=True)
class ProcessOptions:
    mode: ProcessingMode
    apply_type_a_boost: bool = False   # formerly flag1
    preserve_high_values: bool = True  # formerly flag2
    output_type: OutputType = OutputType.JSON


@dataclass(frozen=True)
class ItemResult:
    item_id: Any
    value: float
    status: Status

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.item_id,
            "val": self.value,
            "status": self.status.value,
        }


class ItemProcessor:
    def process(self, items: Iterable[dict[str, Any]], options: ProcessOptions) -> str | list[dict[str, Any]]:
        results = [result for item in items if (result := self._process_item(item, options)) is not None]
        return self._format_output(results, options.output_type)

    def _process_item(self, item: dict[str, Any], options: ProcessOptions) -> ItemResult | None:
        if options.mode == ProcessingMode.FAST:
            return self._process_fast(item, options)

        if options.mode == ProcessingMode.CAREFUL:
            return self._process_careful(item)

        raise ValueError(f"Unsupported processing mode: {options.mode}")

    def _process_fast(self, item: dict[str, Any], options: ProcessOptions) -> ItemResult | None:
        item_type = item.ge...
```

### Claude Opus 4.6

**Generation Time:** 427624ms
**Tokens:** 2552

```


# Refactoring: From Unmaintainable to Clean Architecture

## Problems with the Original Code

Let me first catalog what's wrong:

1. **God function** — one function doing processing, validation, business logic, AND serialization
2. **Boolean flag arguments** — `flag1`, `flag2` are meaningless names that create hidden behavioral branches
3. **Nested conditionals** — 5+ levels of nesting make control flow nearly impossible to trace
4. **Bare `except`** — silently catches everything including `KeyboardInterrupt`
5. **Inline import** — `import json` buried in function body
6. **Open/Closed violation** — adding a new mode or type requires modifying the function internals
7. **No type hints** — no way to know what `data` looks like
8. **Untestable** — you can't test pricing logic without also testing serialization

## The Refactored Code

```python
"""
Item processing pipeline with pluggable strategies and serializers.

Design philosophy:
- Each class has exactly one reason to change (SRP)
- New item types, processing modes, and output formats are added
  by extension, not modification (OCP)
- Every component is independently testable
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Sequence


# ──────────────────────────────────────────────
# Domain Models
# ──────────────────────────────────────────────
# DECISION: Dataclasses replace raw dicts to get type safety, immutability,
# and self-documenting field names. A dict with keys 'id', 'value', 'type'
# is a data class screaming to be born.

class ItemType(str, Enum):
    """Exhaustive enumeration prevents typo-driven bugs like type='a'."""
    A = "A"
    B = "B"
    OTHER = "OTHER"


class Status(str, Enum):
    """Centralizes status strings — no more magic string mismatches."""
    HIGH = "high"
    ADJUSTED = "adjusted"
    NORMAL = "normal"
    DISCOUNTED = "discounted"
    SKIPPED = "skip"
    VALID...
```

### Gemini 3.1 Pro

**Generation Time:** 28294ms
**Tokens:** 2499

```
This is a classic example of "spaghetti code." It works, but it violates several core software engineering principles: **Single Responsibility Principle (SRP)**, **Open/Closed Principle (OCP)**, and it suffers from code smells like **Magic Strings**, **Boolean Traps**, and **Bare Exceptions**.

Here is the refactored, clean, and testable version, followed by
```

### Claude Sonnet 4.6

**Generation Time:** 33434ms
**Tokens:** 2552

```
# Refactored Code: Clean, Testable, Well-Structured

## Problems with the Original Code

Before diving in, let me enumerate every issue:

1. **One function does everything** — processing logic, business rules, and output formatting are tangled together
2. **Boolean flags as behavior switches** — `flag1`, `flag2` create hidden, combinatorial behavior (2² = 4 modes)
3. **Magic numbers** — `1.1`, `0.95`, `0.9`, `100` have no names or explanation
4. **Bare `except`** — silently swallows all errors including `KeyboardInterrupt`
5. **Import inside function** — `import json` inside a loop-adjacent block
6. **Inconsistent output** — returns string OR list depending on `output_type`
7. **No input validation** — crashes on missing `id` key, wrong types, etc.
8. **Untestable** — you can't test fast-mode type-A logic without also exercising formatting

---

## Refactored Code

```python
# processing/models.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class ItemType(str, Enum):
    """
    Explicit enumeration of known item types.
    
    Using str-Enum means values compare equal to their string equivalents,
    which makes deserialization from JSON/dicts seamless without conversion.
    """
    A = "A"
    B = "B"
    UNKNOWN = "unknown"


class ProcessingStatus(str, Enum):
    """
    Every possible outcome status in one place.
    
    Centralizing statuses prevents typos like 'skiped' vs 'skipped' scattered
    across the codebase, and makes exhaustive matching possible in type checkers.
    """
    HIGH = "high"
    ADJUSTED = "adjusted"
    NORMAL = "normal"
    DISCOUNTED = "discounted"
    SKIPPED = "skip"
    VALIDATED = "validated"
    ERROR = "error"


@dataclass(frozen=True)
class RawItem:
    """
    Represents one unprocessed input record.
    
    frozen=True makes instances hashable and prevents accidental mutation —
    input data should never be modified, only transformed into new objects.
    """
    id...
```

### Grok 4.20

**Generation Time:** 7071ms
**Tokens:** 2414

```
**Refactored & Clean Code**

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Union
import json
from pathlib import Path


class ProcessingMode(Enum):
    FAST = "fast"
    CAREFUL = "careful"


class OutputFormat(Enum):
    RAW = "raw"
    JSON = "json"
    CSV = "csv"


class ItemType(Enum):
    A = "A"
    B = "B"
    UNKNOWN = "UNKNOWN"


class Status(Enum):
    HIGH = "high"
    NORMAL = "normal"
    ADJUSTED = "adjusted"
    DISCOUNTED = "discounted"
    VALIDATED = "validated"
    ERROR = "error"
    SKIPPED = "skip"


@dataclass(frozen=True)
class ProcessingConfig:
    """Immutable configuration for the processor."""
    mode: ProcessingMode
    flag1: bool = False
    flag2: bool = True
    output_format: OutputFormat = OutputFormat.JSON


@dataclass
class ProcessedItem:
    """Domain model for a processed item."""
    id: str
    val: float
    status: Status


class ItemProcessor:
    """Pure business logic for processing a single item."""

    def __init__(self, config: ProcessingConfig):
        self.config = config

    def process(self, item: Dict[str, Any]) -> ProcessedItem:
        if self.config.mode == ProcessingMode.FAST:
            return self._process_fast(item)
        else:  # CAREFUL
            return self._process_careful(item)

    def _process_fast(self, item: Dict[str, Any]) -> ProcessedItem:
        item_id = item.get("id", "unknown")
        item_type = ItemType(item.get("type") or ItemType.UNKNOWN.value)
        raw_value = item.get("value", 0)

        if item_type == ItemType.A:
            return self._process_type_a(item_id, raw_value)
        elif item_type == ItemType.B:
            return self._process_type_b(item_id, raw_value)
        else:
            return self._process_unknown_fast(item_id)

    def _process_type_a(self, item_id: str, raw_value: Any) -> ProcessedItem:
        multiplier = 1.1 if self.config.flag1 else 1.0
        val = float(raw_value) * multiplier

 ...
```

### DeepSeek V3

**Generation Time:** 112397ms
**Tokens:** 2172

```
I'll refactor this code into a clean, testable, and well-structured design. Here's the step-by-step approach:

### Key Problems in Original Code:
1. Deeply nested conditionals making logic hard to follow
2. Multiple responsibilities in one function (processing, validation, output formatting)
3. Magic numbers and hard-coded values
4. No clear separation of business rules from processing logic
5. Brittle error handling
6. Difficulty to test individual components

### Refactored Solution:

```python
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

class ProcessingStrategy(ABC):
    """Abstract base class for processing strategies"""
    @abstractmethod
    def process_item(self, item: Dict[str, Any], flags: Dict[str, bool]) -> Dict[str, Any]:
        pass

class FastProcessingStrategy(ProcessingStrategy):
    """Handles 'fast' mode processing rules"""
    TYPE_A_MULTIPLIER = 1.1
    TYPE_B_MULTIPLIER = 0.95
    ADJUSTMENT_MULTIPLIER = 0.9
    HIGH_VALUE_THRESHOLD = 100

    def process_item(self, item: Dict[str, Any], flags: Dict[str, bool]) -> Dict[str, Any]:
        item_type = item.get('type')
        value = item.get('value', 0)
        
        if item_type == 'A':
            return self._process_type_a(item, value, flags)
        elif item_type == 'B':
            return self._process_type_b(item, value)
        else:
            return self._process_other_type(item, flags)

    def _process_type_a(self, item: Dict[str, Any], value: float, flags: Dict[str, bool]) -> Dict[str, Any]:
        processed_value = value * self.TYPE_A_MULTIPLIER if flags['flag1'] else value
        
        if processed_value > self.HIGH_VALUE_THRESHOLD:
            if flags['flag2']:
                status = 'high'
            else:
                status = 'adjusted'
                processed_value *= self.ADJUSTMENT_MULTIPLIER
        else:
            status = 'normal'
            
        return {'id': item['id'], 'val': processed_value, 's...
```

### GPT-OSS-120B

**Generation Time:** 45611ms
**Tokens:** 2507

```
## 1.  What we are trying to achieve  

The original `process()` function mixes **four** different concerns:

| Concern | What the code does | Why it hurts maintainability |
|---------|--------------------|------------------------------|
| **Business logic** | “fast” vs “careful” handling of each `item` and the flag‑driven calculations | A single long `if/elif` block is hard to read, extend or test in isolation |
| **Result construction** | Building dictionaries with different keys/values | Tightly coupled to the logic – any change forces the whole function to be edited |
| **Formatting / serialization** | JSON, CSV or raw Python list | The `if output_type …` is an ad‑hoc switch that makes the function do I/O‑style work |
| **Error handling** | A blanket `except:` that swallows everything | Hard to reason about failures, impossible to unit‑test the error path reliably |

To make the code **clean, testable and extensible** we will:

1. **Separate each concern into its own class / function** (single‑responsibility principle).  
2. **Introduce explicit contracts** (type hints, `Enum`s, `dataclass`) so that callers and tests know exactly what is expected.  
3. **Replace “big if/else” with a strategy/registry pattern** – adding a new mode never touches existing code (open‑closed principle).  
4. **Make formatting a pluggable component** – we can add XML, protobuf, etc. without touching the core processor.  
5. **Avoid catching generic exceptions** – raise a domain‑specific error (`ProcessingError`) and let the caller decide how to surface it.  
6. **Inject dependencies** (mode handler, formatter) – makes unit tests deterministic and eliminates hidden imports.  

Below is a complete, production‑ready refactor that follows the above decisions, followed by a short test‑suite and a discussion of each design choice.

---

## 2.  Refactored implementation  

```python
# ──────────────────────────────────────────────────────────────────────
# processing.py
# ───────────────────...
```

### Gemini 3 Flash Preview

**Generation Time:** 8382ms
**Tokens:** 1860

```
To refactor this code, we need to move away from "Procedural Spaghetti" (nested `if/else`) and toward a **Strategy Pattern** or **Registry-based** approach.

### The Refactored Code

```python
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

# --- Domain Models ---

class ProcessingStrategy(ABC):
    """Abstract base class for different processing modes."""
    @abstractmethod
    def process_item(self, item: Dict[str, Any], flag1: bool, flag2: bool) -> Union[Dict, None]:
        pass

# --- Strategies ---

class FastStrategy(ProcessingStrategy):
    def process_item(self, item: Dict[str, Any], flag1: bool, flag2: bool) -> Union[Dict, None]:
        item_type = item.get('type')
        val = item.get('value', 0)
        
        if item_type == 'A':
            return self._handle_type_a(item['id'], val, flag1, flag2)
        if item_type == 'B':
            return {'id': item['id'], 'val': val * 0.95, 'status': 'discounted'}
        if flag1 and flag2:
            return {'id': item['id'], 'val': 0, 'status': 'skip'}
        return None

    def _handle_type_a(self, item_id: str, val: float, flag1: bool, flag2: bool) -> Dict:
        adjusted_val = val * 1.1 if flag1 else val
        if adjusted_val > 100:
            if flag2:
                return {'id': item_id, 'val': adjusted_val, 'status': 'high'}
            return {'id': item_id, 'val': adjusted_val * 0.9, 'status': 'adjusted'}
        return {'id': item_id, 'val': adjusted_val, 'status': 'normal'}

class CarefulStrategy(ProcessingStrategy):
    def process_item(self, item: Dict[str, Any], flag1: bool, flag2: bool) -> Dict:
        try:
            val = float(item.get('value', 0))
            if val < 0:
                raise ValueError("Negative value")
            return {'id': item['id'], 'val': val, 'status': 'validated'}
        except (ValueError, TypeError, KeyError):
            return {'id': item['id'], 'val': 0, 'status': 'error'}

# --- Formatters ---

...
```

### MiniMax M2.5

**Generation Time:** 86123ms
**Tokens:** 2488

```

```

### MiMo-V2-Flash

**Generation Time:** 19574ms
**Tokens:** 2491

```
Here is the refactored code, followed by a detailed explanation of the design decisions.

### Refactored Code

```python
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any, Dict, Optional

# --- Domain Models ---

@dataclass
class Item:
    """Represents the raw input data item."""
    id: str
    value: Any
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            value=data.get('value'),
            type=data.get('type')
        )

@dataclass
class ProcessedResult:
    """Represents the processed output data item."""
    id: str
    val: float
    status: str

# --- Strategy Interfaces ---

class ProcessingStrategy(ABC):
    """Abstract base class for processing modes."""
    
    @abstractmethod
    def process(self, item: Item) -> ProcessedResult:
        """Process a single item and return a result."""
        pass

# --- Concrete Strategies ---

class FastProcessingStrategy(ProcessingStrategy):
    """Strategy for 'fast' mode logic."""
    
    def __init__(self, flag1: bool, flag2: bool):
        self.flag1 = flag1
        self.flag2 = flag2

    def process(self, item: Item) -> Optional[ProcessedResult]:
        if item.type == 'A':
            return self._process_type_a(item)
        elif item.type == 'B':
            return self._process_type_b(item)
        else:
            return self._process_type_other(item)

    def _process_type_a(self, item: Item) -> ProcessedResult:
        val = item.value * 1.1 if self.flag1 else item.value
        
        if val > 100:
            status = 'high' if self.flag2 else 'adjusted'
            val = val if self.flag2 else val * 0.9
        else:
            status = 'normal'
            
        return ProcessedResult(id=item.id, val=val, status=status)

    def _process_type_b(self, item: Item) -> ProcessedResult:
        val = item.value * 0.95
        return Proces...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*