# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-135609
**Timestamp:** 2026-04-02T13:56:09.641336
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a Bloom filter from scratch (no libraries) with the following: configurable false positive rate, optimal hash function count calculation, serialization/deserialization, a counting variant that supports deletion, and memory usage statistics. Include mathematical proof of your false positive rate formula.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 8.68 | 7.20 | 9.80 | 0.90 |
| 2 | Gemini 3 Flash Preview | 8.03 | 6.75 | 8.80 | 0.69 |
| 3 | GPT-5.4 | 7.56 | 5.80 | 8.85 | 1.19 |
| 4 | GPT-OSS-120B | 7.42 | 4.05 | 9.45 | 1.78 |
| 5 | Claude Opus 4.6 | 7.31 | 3.90 | 9.60 | 1.86 |
| 6 | MiMo-V2-Flash | 7.16 | 4.20 | 9.45 | 1.47 |
| 7 | Claude Sonnet 4.6 | 6.98 | 4.60 | 8.60 | 1.43 |
| 8 | DeepSeek V3 | 5.56 | 4.15 | 6.60 | 1.00 |
| 9 | Gemini 3.1 Pro | 2.62 | 0.65 | 5.85 | 1.66 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.46 |
| 2 | Claude Opus 4.6 | 5.96 |
| 3 | GPT-OSS-120B | 6.43 |
| 4 | Gemini 3.1 Pro | 6.49 |
| 5 | Claude Sonnet 4.6 | 6.67 |
| 6 | Grok 4.20 | 7.20 |
| 7 | MiniMax M2.5 | 7.45 |
| 8 | MiMo-V2-Flash | 7.51 |
| 9 | Gemini 3 Flash Preview | 7.98 |
| 10 | DeepSeek V3 | 8.53 |

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

**Generation Time:** 29236ms
**Tokens:** 2105

```
Below is a complete from-scratch Bloom filter implementation in Python that includes:

- Configurable false positive rate
- Optimal number of hash functions calculation
- Serialization / deserialization
- A counting Bloom filter variant with deletion
- Memory usage statistics
- A mathematical proof of the false positive rate formula

No Bloom filter libraries are used.

---

# 1. Mathematical background

## 1.1 Standard Bloom filter

A Bloom filter consists of:

- an array of `m` bits, initially all `0`
- `k` hash functions
- after inserting `n` items, membership queries may return false positives but never false negatives

To insert an item:
- compute `k` hash values
- set those `k` bit positions to `1`

To query an item:
- compute the same `k` positions
- if any bit is `0`, the item is definitely not present
- if all are `1`, the item is probably present

---

## 1.2 False positive probability derivation

Let:

- `m` = number of bits
- `k` = number of hash functions
- `n` = number of inserted items

We assume each hash function maps uniformly and independently into the `m` bit positions.

### Step 1: Probability a particular bit remains 0 after one hash
A single hash sets one bit. The probability that a particular bit is **not** set by one hash is:

\[
1 - \frac{1}{m}
\]

### Step 2: Probability a particular bit remains 0 after inserting n items
Each item sets `k` bits, so there are `kn` hash placements total.

Thus, the probability a particular bit is still `0` after all insertions is:

\[
\left(1 - \frac{1}{m}\right)^{kn}
\]

Therefore, the probability that the bit is `1` is:

\[
1 - \left(1 - \frac{1}{m}\right)^{kn}
\]

### Step 3: False positive event
A false positive happens when querying an element not inserted, and all `k` positions checked happen to be `1`.

Assuming independence, the false positive probability is:

\[
p = \left(1 - \left(1 - \frac{1}{m}\right)^{kn}\right)^k
\]

This is the exact standard approximation model.

### Step 4: Exponential appro...
```

### Claude Opus 4.6

**Generation Time:** 43023ms
**Tokens:** 2112

```


# Bloom Filter Implementation from Scratch

## Mathematical Proof of False Positive Rate

Before the implementation, here's the rigorous mathematical derivation:

```
BLOOM FILTER FALSE POSITIVE RATE - MATHEMATICAL PROOF
======================================================

Given:
  m = number of bits in the filter
  n = expected number of elements
  k = number of hash functions

THEOREM: The optimal false positive rate is p = (1 - e^(-kn/m))^k,
minimized when k = (m/n) * ln(2).

PROOF:

Step 1: Probability a specific bit is NOT set by one hash function
  after inserting one element:
  
  P(bit = 0 | one hash, one element) = 1 - 1/m

Step 2: After inserting one element with k hash functions (assuming
  independence of hash positions):
  
  P(bit = 0 | k hashes, one element) = (1 - 1/m)^k

Step 3: After inserting n elements, each with k hash functions:
  
  P(bit = 0 | k hashes, n elements) = (1 - 1/m)^(kn)

Step 4: Using the limit identity lim_{m→∞} (1 - 1/m)^m = e^(-1):
  
  (1 - 1/m)^(kn) = ((1 - 1/m)^m)^(kn/m) ≈ e^(-kn/m)

Step 5: Probability a specific bit IS set:
  
  P(bit = 1) = 1 - e^(-kn/m)

Step 6: False positive occurs when ALL k hash positions are set for
  an element NOT in the set. Assuming bit independence:
  
  P(false positive) = (1 - e^(-kn/m))^k = p

Step 7: To find optimal k, minimize p. Take ln of both sides:
  
  ln(p) = k · ln(1 - e^(-kn/m))
  
  Let f = kn/m (the fill ratio). Then k = fm/n, and:
  
  ln(p) = (fm/n) · ln(1 - e^(-f))
  
  Substitute g(f) = ln(1 - e^(-f)):
  
  d/df [(f/n) · m · g(f)] = 0  →  g(f) + f · g'(f) = 0
  
  g'(f) = e^(-f) / (1 - e^(-f))
  
  ln(1 - e^(-f)) + f · e^(-f) / (1 - e^(-f)) = 0
  
  Let t = e^(-f), so f = -ln(t):
  
  ln(1-t) + (-ln(t)) · t/(1-t) = 0
  
  This is satisfied when t = 1/2, i.e., e^(-f) = 1/2, f = ln(2).
  
  Therefore: kn/m = ln(2)  →  k = (m/n) · ln(2)  ■

Step 8: Optimal bit array size given desired false positive rate p:
  
  From p = (1/2)^k = (1/2)^((m/n)ln2):
  
  ln(p) = -(m/n)(ln2)²...
```

### Gemini 3.1 Pro

**Generation Time:** 33505ms
**Tokens:** 2097

```
Here is a complete, from-scratch implementation of a Counting Bloom Filter in Python, using only the standard library. 

I will first provide the mathematical proof for the False Positive Rate (FPR) and optimal parameter calculations, followed by the complete, production-ready code.

---

### Part 1: Mathematical Proof of the False Positive Rate

Let:
*   $n$ =
```

### Claude Sonnet 4.6

**Generation Time:** 26223ms
**Tokens:** 2111

```
# Bloom Filter Implementation from Scratch

## Mathematical Foundation

Before implementation, let's prove the false positive rate formula.

**Proof of False Positive Rate Formula:**

Given:
- `n` = expected number of elements
- `m` = bit array size  
- `k` = number of hash functions

After inserting `n` elements, the probability a specific bit is still `0`:
```
P(bit = 0) = (1 - 1/m)^(kn) ≈ e^(-kn/m)
```

The probability of a false positive (all `k` bits set for non-member):
```
P(false positive) = (1 - P(bit = 0))^k = (1 - e^(-kn/m))^k
```

To find optimal `k`, minimize with respect to `k`:
```
∂/∂k [(1 - e^(-kn/m))^k] = 0

Let p = e^(-kn/m), then FPR = (1-p)^k

Taking ln: k·ln(1-p) where p = e^(-kn/m)
Setting derivative to 0 gives: k = (m/n)·ln(2)
```

Substituting optimal `k` back:
```
FPR_min = (1/2)^k = (1/2)^((m/n)·ln(2))
```

Solving for `m` given desired FPR `ε`:
```
ε = (1/2)^((m/n)·ln(2))
ln(ε) = -(m/n)·ln(2)²
m = -n·ln(ε) / ln(2)²  ≈  -1.4427·n·ln(ε)
```

---

```python
"""
Bloom Filter Implementation from Scratch
Includes: Standard, Counting, Serialization, Memory Stats
"""

import math
import struct
import json
import hashlib
import array
from typing import Any, Dict, Tuple, Optional
from dataclasses import dataclass, field


# ─────────────────────────────────────────────
# Hash Functions (no external libraries)
# ─────────────────────────────────────────────

def _to_bytes(item: Any) -> bytes:
    """Convert any item to bytes for hashing."""
    if isinstance(item, bytes):
        return item
    elif isinstance(item, str):
        return item.encode('utf-8')
    elif isinstance(item, (int, float)):
        return str(item).encode('utf-8')
    else:
        return str(item).encode('utf-8')


def _fnv1a_32(data: bytes, seed: int = 0) -> int:
    """FNV-1a 32-bit hash — fast, good distribution."""
    FNV_PRIME = 0x01000193
    FNV_OFFSET = 0x811C9DC5
    
    h = (FNV_OFFSET ^ seed) & 0xFFFFFFFF
    for byte in data:
        h ^= byte
        h = (h *...
```

### Grok 4.20

**Generation Time:** 9360ms
**Tokens:** 2221

```
**Bloom Filter Implementation (Python, from scratch)**

```python
import math
import hashlib
import pickle
import struct
from typing import List, Any, Tuple, Optional


class BloomFilter:
    """
    Standard Bloom Filter with:
      - Configurable false positive rate
      - Optimal number of hash functions (k)
      - Serialization / deserialization
      - Memory usage statistics
    """

    def __init__(self, capacity: int, false_positive_rate: float = 0.01):
        if capacity <= 0:
            raise ValueError("Capacity must be > 0")
        if not (0 < false_positive_rate < 1):
            raise ValueError("False positive rate must be in (0, 1)")

        self.capacity = capacity                    # expected number of elements
        self.p = false_positive_rate                # desired false positive probability
        self.m = self._optimal_size(capacity, self.p)   # bit array size
        self.k = self._optimal_hash_count(self.m, capacity)  # number of hash functions

        self.bit_array = bytearray((self.m + 7) // 8)  # packed bits
        self.n = 0                                      # number of elements inserted

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        """m = - (n ln p) / (ln 2)^2"""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hash_count(m: int, n: int) -> int:
        """k = (m/n) ln 2"""
        k = (m / n) * math.log(2)
        return max(1, round(k))

    def _hash(self, item: Any, seed: int) -> int:
        """Double hashing using SHA-256 + seed"""
        data = str(item).encode('utf-8')
        h1 = int.from_bytes(hashlib.sha256(data).digest(), 'big')
        h2 = int.from_bytes(hashlib.sha256(data + seed.to_bytes(4, 'big')).digest(), 'big')
        return (h1 + seed * h2) % self.m

    def add(self, item: Any) -> None:
        for i in range(self.k):
            bit = self._hash(item, i)
            byte_idx = bit // 8
            bit_idx = bit % 8
    ...
```

### DeepSeek V3

**Generation Time:** 55084ms
**Tokens:** 1518

```
# Bloom Filter Implementation

Below is a complete Python implementation of a Bloom filter with all the requested features.

```python
import math
import bitarray
import mmh3  # MurmurHash3 is a good non-cryptographic hash function
import pickle
from collections import defaultdict

class BloomFilter:
    """Bloom filter implementation with configurable false positive rate, serialization,
       and memory usage statistics."""
    
    def __init__(self, n_items, false_positive_rate=0.01):
        """
        Initialize the Bloom filter.
        
        Args:
            n_items: Expected number of items to be stored.
            false_positive_rate: Desired false positive probability (default 0.01).
        """
        self.n_items = n_items
        self.false_positive_rate = false_positive_rate
        
        # Calculate optimal number of hash functions and bit array size
        self.size = self._calculate_size(n_items, false_positive_rate)
        self.hash_count = self._calculate_hash_count(self.size, n_items)
        
        # Initialize bit array
        self.bit_array = bitarray.bitarray(self.size)
        self.bit_array.setall(0)
        
        # Track actual number of items inserted
        self.items_count = 0
        
    def _calculate_size(self, n_items, false_positive_rate):
        """Calculate the optimal size of the bit array."""
        size = - (n_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        return int(math.ceil(size))
    
    def _calculate_hash_count(self, size, n_items):
        """Calculate the optimal number of hash functions."""
        hash_count = (size / n_items) * math.log(2)
        return int(math.ceil(hash_count))
    
    def _get_hashes(self, item):
        """Generate multiple hash values for an item."""
        hashes = []
        for i in range(self.hash_count):
            # Use different seeds for each hash function
            hash_val = mmh3.hash(str(item), i) % self.size
            hashes.appen...
```

### GPT-OSS-120B

**Generation Time:** 128424ms
**Tokens:** 2166

```
Below is a **self‑contained Python implementation** of a Bloom filter and a counting Bloom filter (which adds delete support).  
All the required features are implemented **without using any third‑party libraries**:

* configurable false‑positive rate (`p`) and expected number of items (`n`);
* optimal size (`m`) and optimal number of hash functions (`k`) are computed automatically;
* a fast double‑hashing scheme that generates `k` independent hash values from two base hashes;
* serialization / deserialization to/from a compact binary representation (plus a JSON‑friendly dict);
* a counting variant that stores small counters instead of a single bit‑array, allowing deletions;
* memory‑usage statistics (bits, bytes, overhead, theoretical vs. actual memory).

The answer also contains a **short mathematical proof** of the classic Bloom‑filter false‑positive formula.

---

## 1️⃣  Theory – why the formulas are what they are

Let  

* `n` – number of distinct elements we expect to insert,  
* `m` – number of bits in the filter,  
* `k` – number of hash functions,  
* `p` – desired false‑positive probability.

When we insert an element we set `k` bits to **1**.  
After inserting `n` elements the probability that a particular bit is still **0** is

\[
\Pr[\text{bit}=0] = \left(1-\frac{1}{m}\right)^{kn}
\approx e^{-kn/m}                     \tag{1}
\]

(we used \((1-1/m)^{m}\to e^{-1}\) for large `m`).  
Consequently the probability that a given bit is **1** is

\[
\Pr[\text{bit}=1] = 1-e^{-kn/m}.      \tag{2}
\]

A false positive occurs when **all** `k` bits examined for a *new* element are already 1:

\[
p = \Pr[\text{FP}] = \bigl(1-e^{-kn/m}\bigr)^{k}.   \tag{3}
\]

---

### 1.1 Optimal number of hash functions `k`

Treat `m` as fixed and minimise (3) w.r.t. `k`.  
Differentiating the logarithm of (3) and setting the derivative to zero gives

\[
k_{\text{opt}} = \frac{m}{n}\ln 2.                     \tag{4}
\]

Rounded to the nearest integer this is the optimal number of ...
```

### Gemini 3 Flash Preview

**Generation Time:** 12763ms
**Tokens:** 1870

```
This implementation provides a high-performance **Counting Bloom Filter** in Python. It uses bit manipulation for the standard filter and an array for the counting variant to support deletions.

### 1. Mathematical Proof of False Positive Rate

To design the filter, we must relate the number of elements ($n$), the bit array size ($m$), and the number of hash functions ($k$).

**Assumption:** Hash functions are perfectly uniform.

1.  **Probability a bit is still 0:** After one hash insertion into a bit array of size $m$, the probability a specific bit is still $0$ is:
    $$P(\text{bit is } 0) = 1 - \frac{1}{m}$$
2.  **After $k$ hash functions:**
    $$P(\text{bit is } 0) = \left(1 - \frac{1}{m}\right)^k$$
3.  **After $n$ elements are inserted:**
    $$P(\text{bit is } 0) = \left(1 - \frac{1}{m}\right)^{nk} \approx e^{-kn/m}$$
4.  **Probability of a False Positive ($p$):** A false positive occurs if all $k$ bits for a new element are already set to $1$.
    $$p = (1 - P(\text{bit is } 0))^k = (1 - e^{-kn/m})^k$$
5.  **Optimizing $k$:** To find the $k$ that minimizes $p$, we take the derivative of the expression. The minimum occurs when:
    $$k = \frac{m}{n} \ln 2$$
6.  **Required $m$ for a target $p$:** Substituting the optimal $k$ back into the $p$ formula:
    $$m = -\frac{n \ln p}{(\ln 2)^2}$$

---

### 2. Implementation

We use `zlib.crc32` and `hashlib.sha256` combined with **Double Hashing** ($hash = h1 + i \cdot h2$) to simulate $k$ independent hash functions without the overhead of $k$ distinct algorithms.

```python
import math
import json
import hashlib
import zlib

class BloomFilter:
    def __init__(self, capacity, fp_rate):
        self.capacity = capacity
        self.fp_rate = fp_rate
        
        # 1. Calculate optimal m (bits) and k (hashes)
        self.m = int(- (capacity * math.log(fp_rate)) / (math.log(2)**2))
        self.k = max(1, int((self.m / capacity) * math.log(2)))
        
        # Initialize bit array (using a list for simplicity...
```

### MiniMax M2.5

**Generation Time:** 98362ms
**Tokens:** 2137

```

```

### MiMo-V2-Flash

**Generation Time:** 28052ms
**Tokens:** 2137

```
Here is a complete implementation of a Bloom filter from scratch in Python, satisfying all requirements.

### 1. Mathematical Proof of False Positive Rate

Before the code, let's derive the false positive probability formula.

**Definitions:**
*   $m$: Number of bits in the bit array.
*   $k$: Number of hash functions.
*   $n$: Number of items currently inserted.

**Step 1: Probability of a bit being 0 after insertion**
When we insert an item, we set $k$ bits to 1. The probability that a specific bit remains 0 after inserting a single item is:
$$ P(\text{bit}=0) = 1 - \frac{1}{m} $$

After inserting $n$ items, the probability that a specific bit is still 0 is:
$$ P(\text{bit}=0) = \left(1 - \frac{1}{m}\right)^{kn} $$

**Step 2: Probability of a bit being 1**
The probability that a specific bit is 1 (set by previous insertions) is:
$$ P(\text{bit}=1) = 1 - \left(1 - \frac{1}{m}\right)^{kn} $$

**Step 3: False Positive Probability**
A false positive occurs when we check for an item that wasn't inserted. We need all $k$ hash positions to be 1. Assuming the hash functions are independent and uniformly distributed:
$$ P(\text{false positive}) = \left[1 - \left(1 - \frac{1}{m}\right)^{kn}\right]^k $$

**Step 4: Approximation**
Since $m$ is large, we can use the limit approximation $\lim_{x \to \infty} (1 - 1/x)^x = 1/e$.
$$ \left(1 - \frac{1}{m}\right)^{kn} \approx e^{-kn/m} $$

Substituting this back:
$$ P \approx \left(1 - e^{-kn/m}\right)^k $$

This is the formula used to calculate the false positive rate.

---

### 2. Python Implementation

This implementation includes:
1.  **Standard Bloom Filter**: Space-efficient, fast lookups.
2.  **Counting Bloom Filter**: Uses counters instead of bits to support deletion.
3.  **Serialization**: Saves/Loads state to/from binary files or byte arrays.
4.  **Math & Stats**: Calculates optimal $k$ and reports memory usage.

```python
import math
import hashlib
import sys
import io

class BloomFilterBase:
    """
    Base class contai...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*