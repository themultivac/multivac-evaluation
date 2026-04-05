# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-140137
**Timestamp:** 2026-04-02T14:01:37.830225
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
| 1 | GPT-5.4 | 9.18 | 8.80 | 9.80 | 0.36 |
| 2 | Gemini 3 Flash Preview | 8.96 | 7.95 | 9.80 | 0.59 |
| 3 | MiMo-V2-Flash | 8.50 | 6.15 | 9.80 | 1.10 |
| 4 | DeepSeek V3 | 8.46 | 6.30 | 9.80 | 0.98 |
| 5 | Claude Opus 4.6 | 8.02 | 4.25 | 10.00 | 1.83 |
| 6 | Claude Sonnet 4.6 | 7.99 | 4.80 | 10.00 | 1.80 |
| 7 | GPT-OSS-120B | 7.80 | 3.80 | 9.80 | 1.79 |
| 8 | Gemini 3.1 Pro | 6.36 | 2.05 | 8.60 | 2.40 |
| None | MiniMax M2.5 | 10.00 | 10.00 | 10.00 | 0.00 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.04 |
| 2 | MiniMax M2.5 | 7.42 |
| 3 | Gemini 3.1 Pro | 7.67 |
| 4 | GPT-OSS-120B | 7.74 |
| 5 | Claude Opus 4.6 | 8.03 |
| 6 | Grok 4.20 | 8.69 |
| 7 | Claude Sonnet 4.6 | 8.76 |
| 8 | MiMo-V2-Flash | 8.96 |
| 9 | Gemini 3 Flash Preview | 9.30 |
| 10 | DeepSeek V3 | 9.66 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 90
**Valid Judgments:** 69

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

**Generation Time:** 28860ms
**Tokens:** 2459

```
Below is a refactor that keeps the behavior essentially the same, but makes it:

- easier to read
- easier to test
- safer to change
- easier to extend with new modes/output formats

I’ll first show the refactored code, then explain every design decision in detail.

---

## Refactored code

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Iterable


class ProcessingMode(str, Enum):
    FAST = "fast"
    CAREFUL = "careful"


class OutputType(str, Enum):
    JSON = "json"
    CSV = "csv"
    RAW = "raw"


@dataclass(frozen=True)
class ProcessOptions:
    mode: ProcessingMode
    flag1: bool = False
    flag2: bool = True
    output_type: OutputType = OutputType.JSON


@dataclass(frozen=True)
class Result:
    id: Any
    val: float
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "val": self.val, "status": self.status}


def process(
    data: Iterable[dict[str, Any]],
    mode: str,
    flag1: bool = False,
    flag2: bool = True,
    output_type: str = "json",
) -> str | list[dict[str, Any]]:
    """
    Backward-compatible wrapper around the refactored implementation.
    """
    options = ProcessOptions(
        mode=ProcessingMode(mode),
        flag1=flag1,
        flag2=flag2,
        output_type=_parse_output_type(output_type),
    )
    return DataProcessor(options).process(data)


class DataProcessor:
    def __init__(self, options: ProcessOptions) -> None:
        self.options = options

    def process(self, data: Iterable[dict[str, Any]]) -> str | list[dict[str, Any]]:
        results = [result.to_dict() for result in self._process_items(data)]
        return self._format_output(results)

    def _process_items(self, data: Iterable[dict[str, Any]]) -> list[Result]:
        if self.options.mode == ProcessingMode.FAST:
            return self._process_fast(data)
        if self.options.mode == ProcessingMode.CAREFUL:
            ...
```

### Claude Opus 4.6

**Generation Time:** 191880ms
**Tokens:** 2552

```


# Refactoring: From Unmaintainable to Clean Architecture

## The Problems with the Original Code

Before diving into the solution, let me catalog every issue:

1. **God function** — one function handles processing logic, validation, business rules, AND output formatting
2. **Boolean flag arguments** — `flag1`, `flag2` are meaningless names that create hidden control flow
3. **Nested conditionals** — 5+ levels of nesting make logic nearly impossible to trace
4. **String-typed mode dispatch** — `mode == 'fast'` is fragile, no exhaustiveness checking
5. **Bare `except`** — swallows all exceptions silently, including `KeyboardInterrupt`
6. **Inline import** — `import json` buried inside the function
7. **Mixed concerns** — business logic and serialization are entangled
8. **Untestable** — you can't test item processing without also testing serialization
9. **Magic numbers** — `1.1`, `100`, `0.9`, `0.95` have no semantic meaning
10. **No type hints** — impossible to know expected shapes without reading every line

---

## The Refactored Code

```python
"""
Item processing pipeline with configurable strategies and output formatting.

Design philosophy:
- Each class/function does exactly ONE thing
- Business rules are named, isolated, and independently testable
- New processing modes and output formats are added without modifying existing code
- Configuration is explicit, not encoded in boolean flags
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ============================================================
# Domain Models
# ============================================================
# DECISION: Dataclasses instead of raw dicts.
# Why: Type safety, IDE support, self-documenting field names,
# and you can't silently misspell a field name.
# ============================================================

class Status(Enum):
    """All poss...
```

### Gemini 3.1 Pro

**Generation Time:** 33122ms
**Tokens:** 2499

```
Here is a comprehensive refactoring of the provided code. 

### The Code Smells in the Original Code
Before writing the new code, let's identify why the original is unmaintainable:
1. **Violates Single Responsibility Principle (SRP):** The function handles business logic, error handling, and output formatting all in one place.
2. **The Boolean Trap:** `flag1=False, flag2=True` makes calling the function unreadable. What does `process(data, 'fast', True, False)` mean?
3. **Arrow Anti-Pattern:** Deeply nested `if/else` blocks make the code hard to read and test.
4. **Bare `except:`:** Catching all exceptions hides bugs (like `KeyError` or `KeyboardInterrupt`) and makes debugging nightmares.
5. **Magic Strings:** Hardcoded strings like `'A'`, `'fast'`, `'json'`, and `'discounted'` are prone to typos.
6. **Hidden Imports:** `import json` inside the function is a bad practice.

---

### The Refactored Code

```python
import json
from dataclasses import dataclass, asdict
from typing import Any, Callable, Iterable, Protocol
from enum import Enum

# --- 1. Data Models &
```

### Claude Sonnet 4.6

**Generation Time:** 38500ms
**Tokens:** 2552

```
# Refactored Code: From Unmaintainable to Production-Ready

## Problems with the Original Code

Before writing a single line, let's diagnose what's wrong:

1. **One function doing 5+ jobs**: parsing, validation, transformation, filtering, serialization
2. **Boolean flags as behavior switches**: `flag1`, `flag2` create 4 hidden code paths with no names
3. **Magic numbers scattered everywhere**: `1.1`, `0.95`, `0.9`, `100` with no explanation
4. **Bare `except` clause**: silently swallows all errors including `KeyboardInterrupt`
5. **Import inside function**: `import json` runs on every call
6. **Inconsistent output**: returns `str`, `str`, or `list` depending on arguments
7. **Untestable**: you can't test transformation logic without also testing serialization

---

## The Refactored Solution

### File Structure
```
processor/
├── __init__.py
├── models.py          # Data structures
├── transformers.py    # Business logic (fast/careful modes)
├── serializers.py     # Output formatting
├── processor.py       # Orchestration
└── tests/
    ├── test_transformers.py
    ├── test_serializers.py
    └── test_processor.py
```

---

### `models.py` — Data Structures

```python
"""
Pure data structures with no behavior.

Design decisions:
- dataclasses give us __repr__, __eq__, type hints for free
- frozen=True makes results immutable — transformers produce new objects,
  never mutate input, making the system easier to reason about and test
- ProcessingResult is the single shared currency between all layers;
  every transformer returns it, every serializer consumes it
- Explicit status enum prevents typos like 'hgih' or 'skiip' that a
  bare string would silently accept
"""

from dataclasses import dataclass
from enum import Enum, auto


class ItemStatus(Enum):
    HIGH       = "high"
    ADJUSTED   = "adjusted"
    NORMAL     = "normal"
    DISCOUNTED = "discounted"
    SKIPPED    = "skip"
    VALIDATED  = "validated"
    ERROR      = "error"


@dataclass(frozen=True)
class ...
```

### DeepSeek V3

**Generation Time:** 72042ms
**Tokens:** 2135

```
# Refactored Code with Design Decisions

Here's the refactored version of the code with explanations for each design decision:

```python
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional

class DataProcessor(ABC):
    """Abstract base class for different processing strategies."""
    @abstractmethod
    def process_item(self, item: Dict) -> Dict:
        pass

class FastModeProcessor(DataProcessor):
    """Processor for 'fast' mode with specific business rules."""
    def __init__(self, flag1: bool = False, flag2: bool = True):
        self.flag1 = flag1
        self.flag2 = flag2

    def process_item(self, item: Dict) -> Dict:
        """Process individual item according to fast mode rules."""
        if item.get('type') == 'A':
            return self._process_type_a(item)
        elif item.get('type') == 'B':
            return self._process_type_b(item)
        else:
            return self._process_other_type(item)

    def _process_type_a(self, item: Dict) -> Dict:
        """Handle processing for type A items."""
        value = item['value'] * 1.1 if self.flag1 else item['value']
        
        if value > 100:
            if self.flag2:
                return {'id': item['id'], 'val': value, 'status': 'high'}
            else:
                return {'id': item['id'], 'val': value * 0.9, 'status': 'adjusted'}
        else:
            return {'id': item['id'], 'val': value, 'status': 'normal'}

    def _process_type_b(self, item: Dict) -> Dict:
        """Handle processing for type B items."""
        value = item['value'] * 0.95
        return {'id': item['id'], 'val': value, 'status': 'discounted'}

    def _process_other_type(self, item: Dict) -> Dict:
        """Handle processing for other item types."""
        if self.flag1 and self.flag2:
            return {'id': item['id'], 'val': 0, 'status': 'skip'}
        raise ValueError(f"Unprocessable item type: {item.get('type')}")

class CarefulModeProcessor(...
```

### GPT-OSS-120B

**Generation Time:** 24095ms
**Tokens:** 2520

```
## 1️⃣  What was wrong with the original implementation?

| Problem | Why it hurts maintainability / testability |
|--------|--------------------------------------------|
| **One huge function** (`process`) does *everything*: iteration, business rules, validation, output formatting. | Hard to read, impossible to unit‑test a single rule in isolation. |
| **Magic strings & booleans** (`mode='fast'`, `flag1`, `flag2`, `output_type='json'`). | No compile‑time safety, typo‑prone, no discoverable API. |
| **Nested `if/else` ladders** with duplicated dictionary construction. | Adds cognitive load, easy to miss a branch, difficult to extend. |
| **Inline imports** (`import json` inside the function). | Makes the function do I/O‑side‑effects on every call. |
| **Broad `except:`** catches *any* exception, hiding bugs. | Tests may pass while a real error is silently swallowed. |
| **No type information** – everything is `dict`/`list`/`str`. | IDEs, static analysers, and readers cannot infer the shape of data. |
| **Hard‑coded numbers** (`1.1`, `0.95`, `100`). | Business rules are buried in the code; a change requires hunting the numbers. |
| **Result format is built ad‑hoc** (`{'id':…, 'val':…, 'status':…}`). | No guarantee that every branch returns the same keys; a typo creates a silent bug. |

---

## 2️⃣  Design goals for the refactor

1. **Single‑responsibility** – each function / class does one thing.
2. **Explicit, discoverable API** – use `Enum`s, `dataclass`es, and type hints.
3. **Pluggable behaviour** – “mode” and “output format” are strategies that can be swapped without touching the core loop.
4. **Testability** – pure functions (no I/O) that can be exercised independently.
5. **Extensibility** – adding a new mode or output format should not require editing the existing code.
6. **Readability** – clear naming, small functions, and docstrings.

---

## 3️⃣  High‑level architecture

```
process.py
│
├─ enums.py                # Mode, OutputType
├─ models.py          ...
```

### Gemini 3 Flash Preview

**Generation Time:** 15989ms
**Tokens:** 2077

```
This refactor transforms the "spaghetti" code into a modular, object-oriented, and testable system. We will use the **Strategy Pattern** for processing logic and **Factory Pattern** for formatting.

### The Refactored Code

```python
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

# --- 1. Domain Models ---

class ProcessedItem:
    """Standardized output structure."""
    def __init__(self, id: str, val: float, status: str):
        self.id = id
        self.val = val
        self.status = status

    def to_dict(self):
        return {"id": self.id, "val": self.val, "status": self.status}

# --- 2. Processing Strategies ---

class ProcessingStrategy(ABC):
    @abstractmethod
    def process_item(self, item: Dict[str, Any]) -> Union[ProcessedItem, None]:
        pass

class FastStrategy(ProcessingStrategy):
    def __init__(self, apply_bonus: bool = False, enable_high_status: bool = True):
        self.apply_bonus = apply_bonus
        self.enable_high_status = enable_high_status

    def process_item(self, item: Dict[str, Any]) -> Union[ProcessedItem, None]:
        item_type = item.get('type')
        value = item.get('value', 0)

        if item_type == 'A':
            return self._handle_type_a(item['id'], value)
        if item_type == 'B':
            return ProcessedItem(item['id'], value * 0.95, 'discounted')
        if self.apply_bonus and self.enable_high_status:
            return ProcessedItem(item['id'], 0, 'skip')
        return None

    def _handle_type_a(self, item_id: str, value: float) -> ProcessedItem:
        val = value * 1.1 if self.apply_bonus else value
        if val > 100:
            if self.enable_high_status:
                return ProcessedItem(item_id, val, 'high')
            return ProcessedItem(item_id, val * 0.9, 'adjusted')
        return ProcessedItem(item_id, val, 'normal')

class CarefulStrategy(ProcessingStrategy):
    def process_item(self, item: Dict[str, Any]) -> ProcessedItem:
...
```

### MiniMax M2.5

**Generation Time:** 20094ms
**Tokens:** 2488

```

```

### MiMo-V2-Flash

**Generation Time:** 20075ms
**Tokens:** 2491

```
Of course. This is an excellent exercise. The original code is a classic example of a "God Function" that violates several key software design principles.

Here is a breakdown of the problems, followed by the refactored code and a detailed explanation of the design decisions.

### Problems with the Original Code

1.  **God Function:** The single `process` function does everything: data validation, business logic for two different modes, and output formatting. This makes it long, complex, and hard to understand.
2.  **High Cyclomatic Complexity:** The nested `if/elif/else` blocks and `try/except` create a complex control flow. There are many possible execution paths, making it difficult to test every scenario.
3.  **Hard to Test:** To test the business logic for `mode='fast'`, you must provide an `output_type` that returns a Python object (e.g., not 'json' or 'csv'), or you have to parse the output string. To test the output formatting, you need to run the entire processing logic again. These concerns are tightly coupled.
4.  **Violates Single Responsibility Principle (SRP):** The function has multiple reasons to change. If the business logic for 'fast' mode changes, the function changes. If the CSV output format changes, the function changes.
5.  **Hardcoded Dependencies:** The function directly imports `json` inside its body, making it less flexible and harder to mock in tests.
6.  **Inconsistent Data Structures:** The 'careful' mode catches a generic `except` and returns `0` for `val`, while the 'fast' mode never handles potential `KeyError` or `TypeError` if `item['value']` is missing or not a number. This can lead to unpredictable crashes.

---

### Refactored Code

The refactoring is guided by the **Strategy** and **Factory** design patterns, and the principles of **SRP** and **Dependency Injection**.

```python
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Union, Optional

# --- 1....
```

---

*Generated by The Multivac V5*
*https://themultivac.com*