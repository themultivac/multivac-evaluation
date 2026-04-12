# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-123136
**Timestamp:** 2026-04-02T12:31:36.859098
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Write comprehensive unit tests for this function. Cover all edge cases, including boundary conditions, error cases, and typical usage.

```python
def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    
    Args:
        *streams: Variable number of sorted iterables
        max_items: Optional limit on total items to yield
    
    Yields:
        Items from all streams in sorted order
    
    Raises:
        ValueError: If any stream is not sorted
    """
    import heapq
    
    heap = []
    iterators = [iter(s) for s in streams]
    
    # Initialize heap with first item from each stream
    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass
    
    count = 0
    prev = None
    
    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)
        
        # Validate sorting
        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")
        
        yield item
        prev = item
        count += 1
        
        # Get next item from same stream
        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass
```

Use pytest. Include parametrized tests where appropriate.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.08 | 8.35 | 10.00 | 0.54 |
| 2 | DeepSeek V3 | 8.37 | 6.60 | 9.80 | 0.96 |
| 3 | Gemini 3 Flash Preview | 8.33 | 7.10 | 9.40 | 0.82 |
| 4 | Grok 4.20 | 7.78 | 5.35 | 9.60 | 1.50 |
| 5 | MiMo-V2-Flash | 7.56 | 4.45 | 9.15 | 1.33 |
| 6 | GPT-OSS-120B | 7.23 | 2.85 | 9.05 | 1.94 |
| 7 | Claude Opus 4.6 | 6.88 | 3.80 | 8.60 | 1.49 |
| 8 | Claude Sonnet 4.6 | 6.71 | 2.65 | 8.60 | 2.17 |
| 9 | MiniMax M2.5 | 6.61 | 2.65 | 9.60 | 2.04 |
| 10 | Gemini 3.1 Pro | 3.40 | 0.65 | 9.00 | 3.09 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.09 |
| 2 | Claude Opus 4.6 | 6.80 |
| 3 | MiniMax M2.5 | 7.02 |
| 4 | GPT-OSS-120B | 7.03 |
| 5 | Gemini 3.1 Pro | 7.12 |
| 6 | Grok 4.20 | 7.20 |
| 7 | Claude Sonnet 4.6 | 7.23 |
| 8 | Gemini 3 Flash Preview | 8.14 |
| 9 | MiMo-V2-Flash | 8.39 |
| 10 | DeepSeek V3 | 9.01 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 86

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

**Generation Time:** 26901ms
**Tokens:** 2382

```
```python
import pytest

from your_module import merge_sorted_streams


def collect(gen):
    return list(gen)


class TestMergeSortedStreams:
    @pytest.mark.parametrize(
        "streams, expected",
        [
            ([], []),
            ([[]], []),
            ([[], []], []),
            ([[1]], [1]),
            ([[1, 2, 3]], [1, 2, 3]),
            ([[1, 3, 5], [2, 4, 6]], [1, 2, 3, 4, 5, 6]),
            ([[1, 2], [1, 3], [2, 4]], [1, 1, 2, 2, 3, 4]),
            ([[-5, -1, 0], [-3, 2]], [-5, -3, -1, 0, 2]),
            ([[1, 1, 1], [1, 1]], [1, 1, 1, 1, 1]),
            ([[1, 2, 3], []], [1, 2, 3]),
            ([[], [1, 2, 3]], [1, 2, 3]),
            ([[1, 4, 7], [2, 5, 8], [3, 6, 9]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ],
    )
    def test_typical_and_edge_cases(self, streams, expected):
        result = list(merge_sorted_streams(*streams))
        assert result == expected

    @pytest.mark.parametrize(
        "streams,max_items,expected",
        [
            ([], None, []),
            ([], 0, []),
            ([[1, 2, 3]], None, [1, 2, 3]),
            ([[1, 2, 3]], 0, []),
            ([[1, 2, 3]], 1, [1]),
            ([[1, 2, 3]], 2, [1, 2]),
            ([[1, 2, 3]], 3, [1, 2, 3]),
            ([[1, 2, 3]], 10, [1, 2, 3]),
            ([[1, 3, 5], [2, 4, 6]], 4, [1, 2, 3, 4]),
            ([[1, 3, 5], [2, 4, 6]], 6, [1, 2, 3, 4, 5, 6]),
            ([[1, 3, 5], [2, 4, 6]], 7, [1, 2, 3, 4, 5, 6]),
        ],
    )
    def test_max_items_behavior(self, streams, max_items, expected):
        result = list(merge_sorted_streams(*streams, max_items=max_items))
        assert result == expected

    @pytest.mark.parametrize(
        "streams",
        [
            ([[1, 3, 2]]),
            ([[1, 2, 3], [0, 4, 5]]),
            ([[1, 4], [2, 3]]),
            ([[1, 2], [2, 1]]),
            ([[1, 1, 1], [0]]),
        ],
    )
    def test_raises_value_error_when_global_output_order_decreases(self, streams):
        with pytest.raises(ValueEr...
```

### Claude Opus 4.6

**Generation Time:** 80447ms
**Tokens:** 2455

```


```python
import pytest
from unittest.mock import MagicMock


def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    """
    import heapq

    heap = []
    iterators = [iter(s) for s in streams]

    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass

    count = 0
    prev = None

    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)

        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")

        yield item
        prev = item
        count += 1

        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass


# =============================================================================
# Basic functionality tests
# =============================================================================

class TestBasicMerge:
    """Tests for basic merging of sorted streams."""

    def test_two_sorted_lists(self):
        result = list(merge_sorted_streams([1, 3, 5], [2, 4, 6]))
        assert result == [1, 2, 3, 4, 5, 6]

    def test_three_sorted_lists(self):
        result = list(merge_sorted_streams([1, 4], [2, 5], [3, 6]))
        assert result == [1, 2, 3, 4, 5, 6]

    def test_single_stream(self):
        result = list(merge_sorted_streams([1, 2, 3]))
        assert result == [1, 2, 3]

    def test_output_is_sorted(self):
        result = list(merge_sorted_streams([1, 5, 9], [2, 3, 7], [4, 6, 8]))
        assert result == sorted(result)

    def test_preserves_all_items(self):
        s1, s2, s3 = [1, 4, 7], [2, 5, 8], [3, 6, 9]
        result = list(merge_sorted_streams(s1, s2, s3))
        assert len(result) == 9
        assert set(result) == {1, 2, 3, 4, 5,...
```

### Gemini 3.1 Pro

**Generation Time:** 39226ms
**Tokens:** 2429

```
Here is a comprehensive suite of unit tests using `pytest` for the `merge_sorted_streams` function. 

It covers typical usage, boundary conditions, edge cases, infinite streams, and error handling.

```python
import pytest
import itertools
from typing import Iterable

# Assuming the function is imported here. 
# For testing purposes, I'll include it directly or you
```

### Claude Sonnet 4.6

**Generation Time:** 23174ms
**Tokens:** 2455

```
```python
"""
Comprehensive unit tests for merge_sorted_streams function.
"""
import pytest
from typing import Iterator, List, Any


# Import or define the function under test
def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    """
    import heapq

    heap = []
    iterators = [iter(s) for s in streams]

    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass

    count = 0
    prev = None

    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)

        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")

        yield item
        prev = item
        count += 1

        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def collect(gen) -> list:
    """Fully materialise a generator into a list."""
    return list(gen)


def infinite_stream(start: int = 0, step: int = 1) -> Iterator[int]:
    """Yield integers indefinitely: start, start+step, start+2*step, …"""
    value = start
    while True:
        yield value
        value += step


# ─────────────────────────────────────────────────────────────────────────────
# 1. No-stream / empty-stream edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEmptyAndNoStreams:
    def test_no_streams_yields_nothing(self):
        assert collect(merge_sorted_streams()) == []

    def test_single_empty_stream(self):
        assert collect(merge_sorted_streams([])) == []

    def test_multiple_empty_streams(se...
```

### Grok 4.20

**Generation Time:** 13270ms
**Tokens:** 2495

```
**Here's a comprehensive set of pytest unit tests** covering all edge cases, boundary conditions, error cases, and typical usage:

```python
import pytest
from typing import Iterator, List, Any
from collections.abc import Iterable

# Import the function to test
# Assuming it's in a module named 'merge_streams'
from merge_streams import merge_sorted_streams


# ==================== HELPER FUNCTIONS ====================

def to_iterator(lst: List[Any]) -> Iterator:
    """Convert list to iterator for testing."""
    return iter(lst)


# ==================== TEST CASES ====================

class TestMergeSortedStreams:

    # ------------------- Basic Functionality -------------------

    def test_single_stream(self):
        """Test with a single sorted stream."""
        stream = [1, 3, 5, 7, 9]
        result = list(merge_sorted_streams(stream))
        assert result == stream

    def test_two_sorted_streams(self):
        """Test merging two sorted streams."""
        s1 = [1, 3, 5, 7]
        s2 = [2, 4, 6, 8]
        result = list(merge_sorted_streams(s1, s2))
        assert result == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_multiple_streams(self):
        """Test merging three sorted streams."""
        s1 = [1, 10, 20]
        s2 = [2, 5, 15]
        s3 = [3, 8, 12, 25]
        result = list(merge_sorted_streams(s1, s2, s3))
        assert result == [1, 2, 3, 5, 8, 10, 12, 15, 20, 25]

    def test_with_duplicates(self):
        """Test merging streams containing duplicate values."""
        s1 = [1, 2, 2, 3]
        s2 = [2, 2, 4, 5]
        result = list(merge_sorted_streams(s1, s2))
        assert result == [1, 2, 2, 2, 2, 3, 4, 5]

    # ------------------- Empty and None Cases -------------------

    def test_all_empty_streams(self):
        """Test with multiple empty streams."""
        result = list(merge_sorted_streams([], [], []))
        assert result == []

    def test_mixed_empty_and_nonempty(self):
        """Test with mix of empty and non-empt...
```

### DeepSeek V3

**Generation Time:** 85266ms
**Tokens:** 2000

```
Here's a comprehensive set of unit tests for the `merge_sorted_streams` function using pytest:

```python
import pytest
from merge_sorted_streams import merge_sorted_streams

def test_empty_streams():
    """Test with no input streams."""
    assert list(merge_sorted_streams()) == []

def test_single_empty_stream():
    """Test with a single empty stream."""
    assert list(merge_sorted_streams([])) == []

def test_multiple_empty_streams():
    """Test with multiple empty streams."""
    assert list(merge_sorted_streams([], [], [])) == []

def test_single_stream():
    """Test with a single non-empty stream."""
    stream = [1, 2, 3]
    assert list(merge_sorted_streams(stream)) == stream

def test_two_streams():
    """Test merging two simple sorted streams."""
    stream1 = [1, 3, 5]
    stream2 = [2, 4, 6]
    expected = [1, 2, 3, 4, 5, 6]
    assert list(merge_sorted_streams(stream1, stream2)) == expected

def test_three_streams():
    """Test merging three sorted streams."""
    stream1 = [1, 4, 7]
    stream2 = [2, 5, 8]
    stream3 = [3, 6, 9]
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(merge_sorted_streams(stream1, stream2, stream3)) == expected

def test_streams_of_different_lengths():
    """Test merging streams of different lengths."""
    stream1 = [1, 3, 5, 7, 9]
    stream2 = [2, 4]
    stream3 = [6, 8, 10]
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(merge_sorted_streams(stream1, stream2, stream3)) == expected

def test_with_max_items():
    """Test with max_items parameter limiting output."""
    stream1 = [1, 3, 5]
    stream2 = [2, 4, 6]
    assert list(merge_sorted_streams(stream1, stream2, max_items=3)) == [1, 2, 3]
    assert list(merge_sorted_streams(stream1, stream2, max_items=0)) == []

def test_with_max_items_larger_than_total():
    """Test when max_items is larger than total items."""
    stream1 = [1, 3]
    stream2 = [2]
    assert list(merge_sorted_streams(stream1, stream2, max_items=10)) == [1, 2, 3]

d...
```

### GPT-OSS-120B

**Generation Time:** 16213ms
**Tokens:** 2454

```
**`test_merge_sorted_streams.py`**

```python
import heapq
import itertools
import pytest
from typing import Iterable, List, Tuple

# The function under test – copy it here or import from the module where it lives.
def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    
    Args:
        *streams: Variable number of sorted iterables
        max_items: Optional limit on total items to yield
    
    Yields:
        Items from all streams in sorted order
    
    Raises:
        ValueError: If any stream is not sorted
    """
    import heapq
    
    heap = []
    iterators = [iter(s) for s in streams]
    
    # Initialize heap with first item from each stream
    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass
    
    count = 0
    prev = None
    
    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)
        
        # Validate sorting
        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")
        
        yield item
        prev = item
        count += 1
        
        # Get next item from same stream
        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def collect(gen: Iterable) -> List:
    """Collect a generator into a list (easier to read in asserts)."""
    return list(gen)


# ----------------------------------------------------------------------
# 1️⃣ Typical usage – merging sorted streams
# ----------------------------------------------------------------------
@pytest.mark.pa...
```

### Gemini 3 Flash Preview

**Generation Time:** 17347ms
**Tokens:** 1836

```
To test this function effectively, we need to cover standard merging logic, the `max_items` constraint, the custom `ValueError` for unsorted input, and edge cases like empty streams or single inputs.

I will use `pytest` with `pytest.mark.parametrize` to ensure clean, readable, and comprehensive coverage.

```python
import pytest
from your_module import merge_sorted_streams

# --- Typical Usage Tests ---

def test_merge_multiple_sorted_streams():
    """Test merging three sorted lists of different lengths."""
    s1 = [1, 4, 7]
    s2 = [2, 5, 8, 10]
    s3 = [3, 6, 9]
    result = list(merge_sorted_streams(s1, s2, s3))
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def test_merge_with_duplicates():
    """Test merging streams that contain overlapping and duplicate values."""
    s1 = [1, 2, 2, 5]
    s2 = [2, 3, 4]
    result = list(merge_sorted_streams(s1, s2))
    assert result == [1, 2, 2, 2, 3, 4, 5]

def test_handles_generators():
    """Verify it works with generator objects, not just lists."""
    s1 = (i for i in range(0, 10, 2))  # 0, 2, 4, 6, 8
    s2 = (i for i in range(1, 10, 2))  # 1, 3, 5, 7, 9
    result = list(merge_sorted_streams(s1, s2))
    assert result == list(range(10))

# --- Boundary Conditions & Limits ---

@pytest.mark.parametrize("max_items, expected", [
    (0, []),
    (1, [1]),
    (5, [1, 2, 3, 4, 5]),
    (100, [1, 2, 3, 4, 5, 6]), # max_items greater than total available
])
def test_max_items_limit(max_items, expected):
    """Verify the max_items parameter correctly truncates output."""
    s1 = [1, 3, 5]
    s2 = [2, 4, 6]
    result = list(merge_sorted_streams(s1, s2, max_items=max_items))
    assert result == expected

def test_empty_inputs():
    """Test behavior with various empty input scenarios."""
    # No streams provided
    assert list(merge_sorted_streams()) == []
    # Multiple empty streams
    assert list(merge_sorted_streams([], [], [])) == []
    # Mix of empty and non-empty
    assert list(merge_sorted_stre...
```

### MiniMax M2.5

**Generation Time:** 55158ms
**Tokens:** 2416

```
# Comprehensive Unit Tests for `merge_sorted_streams`

Here's a complete test suite covering all edge cases, boundary conditions, and error cases:

```python
import pytest
from itertools import chain, repeat
import heapq


# =============================================================================
# Function Under Test (included for completeness)
# =============================================================================

def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    
    Args:
        *streams: Variable number of sorted iterables
        max_items: Optional limit on total items to yield
    
    Yields:
        Items from all streams in sorted order
    
    Raises:
        ValueError: If any stream is not sorted
    """
    import heapq
    
    heap = []
    iterators = [iter(s) for s in streams]
    
    # Initialize heap with first item from each stream
    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass
    
    count = 0
    prev = None
    
    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)
        
        # Validate sorting
        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")
        
        yield item
        prev = item
        count += 1
        
        # Get next item from same stream
        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def empty_stream():
    """Returns an empty iterable."""
    return []


@pytest.fixture
...
```

### MiMo-V2-Flash

**Generation Time:** 20702ms
**Tokens:** 2406

```
Here are comprehensive unit tests for the `merge_sorted_streams` function using `pytest`.

I have organized the tests into logical classes to cover standard usage, edge cases, boundary conditions, and error handling.

### Prerequisites
You will need `pytest` installed:
```bash
pip install pytest
```

### The Test Suite

```python
import pytest
import heapq
from typing import List, Iterator

# The function under test (copy-pasted from your prompt)
def merge_sorted_streams(*streams, max_items=None):
    """
    Merge multiple sorted iterables into a single sorted output.
    
    Args:
        *streams: Variable number of sorted iterables
        max_items: Optional limit on total items to yield
    
    Yields:
        Items from all streams in sorted order
    
    Raises:
        ValueError: If any stream is not sorted
    """
    import heapq
    
    heap = []
    iterators = [iter(s) for s in streams]
    
    # Initialize heap with first item from each stream
    for i, it in enumerate(iterators):
        try:
            item = next(it)
            heapq.heappush(heap, (item, i))
        except StopIteration:
            pass
    
    count = 0
    prev = None
    
    while heap and (max_items is None or count < max_items):
        item, stream_idx = heapq.heappop(heap)
        
        # Validate sorting
        if prev is not None and item < prev:
            raise ValueError(f"Stream {stream_idx} is not sorted")
        
        yield item
        prev = item
        count += 1
        
        # Get next item from same stream
        try:
            next_item = next(iterators[stream_idx])
            heapq.heappush(heap, (next_item, stream_idx))
        except StopIteration:
            pass


# =========================================================
# Test Classes
# =========================================================

class TestStandardUsage:
    """Tests for typical, valid usage scenarios."""

    def test_merge_two_sorted_lists(self):
        ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*