# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-141537
**Timestamp:** 2026-02-07T14:15:37.647932
**Category:** Programming & Code
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
| 1 | Grok Code Fast 1 | 9.12 | 8.00 | 9.80 | 0.60 |
| 2 | Gemini 3 Flash Preview | 9.07 | 8.60 | 9.80 | 0.52 |
| 3 | Grok 3 (Direct) | 8.48 | 7.40 | 9.80 | 0.79 |
| 4 | Claude Opus 4.5 | 7.53 | 4.45 | 9.25 | 1.85 |
| 5 | Claude Sonnet 4.5 | 7.46 | 5.65 | 8.60 | 1.22 |
| 6 | DeepSeek V3.2 | 7.30 | 3.80 | 9.80 | 1.92 |
| 7 | MiniMax M2.1 | 7.09 | 3.00 | 9.40 | 2.38 |
| 8 | GLM 4.7 | 6.10 | 0.70 | 9.80 | 3.89 |
| 9 | GPT-5.2-Codex | 3.78 | 0.45 | 7.65 | 2.17 |
| 10 | Gemini 3 Pro Preview | 2.45 | 1.00 | 5.85 | 1.71 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Gemini 3 Pro Preview | 0.45 |
| 2 | GPT-5.2-Codex | 4.95 |
| 3 | GLM 4.7 | 5.81 |
| 4 | Claude Sonnet 4.5 | 6.02 |
| 5 | MiniMax M2.1 | 6.04 |
| 6 | Claude Opus 4.5 | 6.08 |
| 7 | Grok Code Fast 1 | 7.13 |
| 8 | Gemini 3 Flash Preview | 7.67 |
| 9 | Grok 3 (Direct) | 7.77 |
| 10 | DeepSeek V3.2 | 8.61 |

**Strictest Judge:** gemini_3_pro
**Most Lenient Judge:** deepseek_v3
**Total Judgments:** 100
**Valid Judgments:** 75

---

## Model Pool

Models selected for **Programming & Code** evaluation:

1. **Grok Code Fast 1** (openrouter)
2. **Claude Opus 4.5** (openrouter)
3. **Gemini 3 Flash Preview** (openrouter)
4. **Claude Sonnet 4.5** (openrouter)
5. **Gemini 3 Pro Preview** (openrouter)
6. **MiniMax M2.1** (openrouter)
7. **GLM 4.7** (openrouter)
8. **DeepSeek V3.2** (openrouter)
9. **GPT-5.2-Codex** (openrouter)
10. **Grok 3 (Direct)** (xai)

---

## Model Responses

### Grok Code Fast 1

**Generation Time:** 12170ms
**Tokens:** 3097

```
```python
import pytest
import heapq
from typing import List, Any

# Assuming the function is defined in the same file or imported
from your_module import merge_sorted_streams  # Replace with actual import if needed

class TestMergeSortedStreams:
    
    @pytest.mark.parametrize("streams, expected", [
        # Empty cases
        ([], []),
        ([[]], []),
        ([[], []], []),
        ([[], [1, 2]], [1, 2]),
        ([[1, 2], []], [1, 2]),
        
        # Single stream
        ([[1, 2, 3]], [1, 2, 3]),
        ([(1, 2, 3)], [1, 2, 3]),  # Tuple iterable
        
        # Multiple streams
        ([[1, 3, 5], [2, 4, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 1, 2], [1, 3]], [1, 1, 1, 2, 3]),  # With duplicates
        ([[0], [1], [2]], [0, 1, 2]),  # Single elements
        
        # Generators (using lambda for iterables)
        ([iter([1, 2]), iter([3, 4])], [1, 2, 3, 4]),
    ])
    def test_typical_usage(self, streams, expected):
        result = list(merge_sorted_streams(*streams))
        assert result == expected
        # Verify output is sorted
        assert result == sorted(result)
    
    @pytest.mark.parametrize("streams, max_items, expected", [
        # max_items None
        ([[1, 2, 3], [4, 5]], None, [1, 2, 3, 4, 5]),
        
        # max_items 0
        ([[1, 2], [3, 4]], 0, []),
        
        # max_items less than total
        ([[1, 2, 3], [4, 5, 6]], 3, [1, 2, 3]),
        ([[1, 2], [3, 4]], 2, [1, 2]),
        
        # max_items equal to total
        ([[1, 2], [3, 4]], 4, [1, 2, 3, 4]),
        
        # max_items greater than total
        ([[1, 2], [3]], 5, [1, 2, 3]),
        
        # With empty streams
        ([], 1, []),
        ([[], [1, 2]], 1, [1]),
    ])
    def test_max_items(self, streams, max_items, expected):
        result = list(merge_sorted_streams(*streams, max_items=max_items))
        assert result == expected
        # Ensure length does not exc...
```

### Claude Opus 4.5

**Generation Time:** 20188ms
**Tokens:** 2455

```
# Comprehensive Unit Tests for `merge_sorted_streams`

```python
import pytest
from typing import Iterator, List, Any
from itertools import count, islice


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
# Test Fixtures and Helpers
# =============================================================================

@pytest.fixture
def empty_stream():
    """Return an empty iterable."""
    return []


@pytest.fixture
def single_item_stream():
    """Return a stream with a single item."""
    return [42]


def infinite_counter(start=0, step=1):
    """Generate an infinite sorted stream of integers."""
    current = start
    while True:
        yield current
        current += ste...
```

### Gemini 3 Flash Preview

**Generation Time:** 9508ms
**Tokens:** 1943

```
Here are comprehensive unit tests for the `merge_sorted_streams` function using `pytest`.

```python
import pytest
from your_module import merge_sorted_streams  # Replace with actual module name

# --- Typical Usage Tests ---

def test_merge_basic_functionality():
    """Test merging multiple sorted lists into one."""
    s1 = [1, 3, 5]
    s2 = [2, 4, 6]
    s3 = [0, 7, 8]
    result = list(merge_sorted_streams(s1, s2, s3))
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8]

def test_merge_different_lengths():
    """Test streams with significantly different lengths."""
    s1 = [1, 10, 100]
    s2 = [2]
    s3 = [3, 4, 5, 6]
    result = list(merge_sorted_streams(s1, s2, s3))
    assert result == [1, 2, 3, 4, 5, 6, 10, 100]

def test_merge_with_duplicates():
    """Test that duplicate values across streams are handled correctly."""
    s1 = [1, 2, 2]
    s2 = [2, 3, 4]
    result = list(merge_sorted_streams(s1, s2))
    assert result == [1, 2, 2, 2, 3, 4]

# --- Boundary Conditions ---

def test_empty_input():
    """Test calling with no streams."""
    assert list(merge_sorted_streams()) == []

def test_empty_streams():
    """Test calling with multiple empty iterables."""
    assert list(merge_sorted_streams([], [], [])) == []

def test_mixed_empty_and_full_streams():
    """Test a mix of empty and populated streams."""
    assert list(merge_sorted_streams([], [1, 2], [])) == [1, 2]

def test_single_stream():
    """Test merging a single stream."""
    assert list(merge_sorted_streams([1, 2, 3])) == [1, 2, 3]

# --- max_items Constraint ---

@pytest.mark.parametrize("max_val, expected", [
    (0, []),
    (1, [0]),
    (5, [0, 1, 2, 3, 4]),
    (100, [0, 1, 2, 3, 4, 5]), # max_items > total items
])
def test_max_items_limit(max_val, expected):
    """Test the max_items parameter at various thresholds."""
    s1 = [0, 2, 4]
    s2 = [1, 3, 5]
    result = list(merge_sorted_streams(s1, s2, max_items=max_val))
    assert result == expected

# --- Error Handling & Val...
```

### Claude Sonnet 4.5

**Generation Time:** 19917ms
**Tokens:** 2455

```
```python
import pytest
from typing import List, Any


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


class TestMergeSortedStreams:
    """Comprehensive test suite for merge_sorted_streams function."""
    
    # ========== Basic Functionality Tests ==========
    
    def test_merge_two_simple_streams(self):
        """Test merging two basic sorted streams."""
        stream1 = [1, 3, 5]
        stream2 = [2, 4, 6]
        result = list(merge_sorted_streams(stream1, stream2))
        assert result == [1, 2, 3, 4, 5, 6]
    
    def test_merge_three_streams(self):
        """Test merging three sorted streams."""
        stream1 = [1, 4, 7]
        stream2 = [2, 5, 8]
        stream3 = [3, 6, 9]
        result = list(merge_sorted_streams(stream1, stream2...
```

### Gemini 3 Pro Preview

**Generation Time:** 20561ms
**Tokens:** 2430

```
Here are comprehensive unit tests for the `merge_sorted_streams` function using the `pytest` framework.

These tests cover:
1.  **Happy Paths**: Standard merging of integers, strings, and floats.
2.  **Boundary Conditions**: Empty streams, no arguments, single items.
3.  **`max_items` Logic**: Limits matching length, exceeding length, and zero limits.
4.
```

### MiniMax M2.1

**Generation Time:** 26561ms
**Tokens:** 2421

```
```python
import pytest
import heapq
from typing import List, Iterator


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


class TestMergeSortedStreamsBasic:
    """Test basic functionality with typical inputs"""
    
    def test_single_stream(self):
        """Test merging a single sorted stream"""
        result = list(merge_sorted_streams([1, 2, 3, 4, 5]))
        assert result == [1, 2, 3, 4, 5]
    
    def test_two_streams_same_length(self):
        """Test merging two streams of equal length"""
        result = list(merge_sorted_streams([1, 3, 5], [2, 4, 6]))
        assert result == [1, 2, 3, 4, 5, 6]
    
    def test_two_streams_different_lengths(self):
        """Test merging two streams of different lengths"""
        result = list(merge_sorted_streams([1, 2, 3], [...
```

### GLM 4.7

**Generation Time:** 100455ms
**Tokens:** 2374

```

```

### DeepSeek V3.2

**Generation Time:** 80805ms
**Tokens:** 2385

```
Here's a comprehensive test suite for the `merge_sorted_streams` function:

```python
import pytest
from typing import List, Generator, Iterator
from itertools import islice

# Function to test (imported from your module)
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


# Test Fixtures and Helper Functions
def list_to_stream(lst: List) -> Generator:
    """Helper to convert list to generator stream."""
    yield from lst


def infinite_stream(start=0, step=1) -> Generator:
    """Create an infinite sorted stream."""
    i = start
    while True:
        yield i
        i += step


# Test Cases
class TestMergeSortedStreams:
    """Test suite for merge_sorted_streams function."""
    
    # Test 1: Basic functionality tests
    def test_empty_streams(self):...
```

### GPT-5.2-Codex

**Generation Time:** 36949ms
**Tokens:** 2382

```
Below is a comprehensive pytest suite for `merge_sorted_streams`, covering typical usage, boundary conditions, empty inputs, limits, and error cases. It also includes a test demonstrating that an unsorted part of a stream is not detected if `max_items` stops early.

```python
import pytest

from your_module import merge_sorted_streams  # replace with actual import


@pytest.mark.parametrize(
    "streams, expected",
    [
        (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
        (([1, 2, 2], [2, 3]), [1, 2, 2, 2, 3]),
        (([], [1, 2]), [1, 2]),
        (([], []), []),
    ],
)
def test_merge_basic
```

### Grok 3 (Direct)

**Generation Time:** 20697ms
**Tokens:** 1838

```
Here's a comprehensive test suite for the `merge_sorted_streams` function using pytest. The tests cover typical usage, edge cases, boundary conditions, and error scenarios.

```python
import pytest
from merge_sorted_streams import merge_sorted_streams

# Test typical usage scenarios
def test_basic_merge():
    stream1 = [1, 3, 5]
    stream2 = [2, 4, 6]
    result = list(merge_sorted_streams(stream1, stream2))
    assert result == [1, 2, 3, 4, 5, 6]

def test_uneven_streams():
    stream1 = [1, 4, 7]
    stream2 = [2, 5]
    stream3 = [3, 6, 8, 9]
    result = list(merge_sorted_streams(stream1, stream2, stream3))
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Test empty and single stream cases
def test_empty_streams():
    result = list(merge_sorted_streams())
    assert result == []

def test_single_stream():
    stream = [1, 2, 3]
    result = list(merge_sorted_streams(stream))
    assert result == [1, 2, 3]

def test_some_empty_streams():
    stream1 = []
    stream2 = [1, 2, 3]
    stream3 = []
    result = list(merge_sorted_streams(stream1, stream2, stream3))
    assert result == [1, 2, 3]

# Test max_items parameter
@pytest.mark.parametrize("max_items, expected", [
    (1, [1]),
    (3, [1, 2, 3]),
    (5, [1, 2, 3, 4, 5]),
    (10, [1, 2, 3, 4, 5, 6])
])
def test_max_items(max_items, expected):
    stream1 = [1, 3, 5]
    stream2 = [2, 4, 6]
    result = list(merge_sorted_streams(stream1, stream2, max_items=max_items))
    assert result == expected

def test_max_items_zero():
    result = list(merge_sorted_streams([1, 2, 3], max_items=0))
    assert result == []

# Test boundary conditions with duplicate values
def test_duplicate_values():
    stream1 = [1, 2, 2, 5]
    stream2 = [2, 3, 4]
    result = list(merge_sorted_streams(stream1, stream2))
    assert result == [1, 2, 2, 2, 3, 4, 5]

# Test error cases
def test_unsorted_stream():
    stream1 = [1, 3, 2]
    stream2 = [4, 5, 6]
    with pytest.raises(ValueError, match="Stream 0 is not sorted"):
    ...
```

---

*Generated by The Multivac V5*
*https://multivac.com*