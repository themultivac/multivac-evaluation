# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-164320
**Timestamp:** 2026-03-18T16:43:20.928376
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

You will write a function, then critique it, then improve it. Three rounds. Each round must be strictly better than the last, and you must explain exactly what improved and why.

Task: Write a Python function that finds the k most frequent words in a text, handling: Unicode, punctuation stripping, case normalization, ties (alphabetical), stopword filtering, and streaming input (the text may be too large for memory).

Round 1: Write your first-draft implementation. Do not overthink it. Write what comes naturally.

Round 2: Now critique Round 1 ruthlessly. Identify every weakness: performance bottlenecks, edge cases missed, code style issues, memory problems with large input. Then write an improved version that fixes every issue you identified.

Round 3: Critique Round 2 with the same rigor. Find the remaining weaknesses. Write the final version. It must handle 10GB+ text files with constant memory usage.

After all 3 rounds: Score each version 1-10 on correctness, performance, and robustness. Explain what changed between each round and what principle drove the improvement. What would Round 4 improve if you had one more iteration?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 7.06 | 5.50 | 8.80 | 1.36 |
| 2 | MiniMax M2 | 6.92 | 4.35 | 8.60 | 1.47 |
| 3 | Claude Sonnet 4.6 | 6.66 | 4.80 | 8.20 | 1.13 |
| 4 | MiniMax-01 | 6.57 | 4.20 | 8.15 | 1.41 |
| 5 | MiniMax M2.7 | 5.96 | 2.45 | 7.95 | 2.00 |
| 6 | MiniMax M2.1 | 5.86 | 2.05 | 7.80 | 1.90 |
| 7 | MiniMax M1 | 5.41 | 3.50 | 7.60 | 1.42 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.56 |
| 2 | MiniMax M2.5 | 6.01 |
| 3 | MiniMax M2.1 | 6.23 |
| 4 | MiniMax M2 | 6.65 |
| 5 | MiniMax M1 | 6.79 |
| 6 | Claude Sonnet 4.6 | 6.92 |
| 7 | MiniMax M2.7 | 7.00 |
| 8 | MiniMax-01 | 7.69 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_01
**Total Judgments:** 72
**Valid Judgments:** 49

---

## Model Pool

Models selected for **Project MiniMax** evaluation:

1. **MiniMax M2.7** (openrouter)
2. **MiniMax M2.5** (openrouter)
3. **MiniMax M2.1** (openrouter)
4. **MiniMax M2** (openrouter)
5. **MiniMax M1** (openrouter)
6. **MiniMax-01** (openrouter)
7. **Claude Sonnet 4.6** (openrouter)
8. **GPT-5.4** (openrouter)
9. **Gemini 3.1 Pro** (openrouter)

---

## Model Responses

### MiniMax M2.7

**Generation Time:** 36831ms
**Tokens:** 2327

```
# Finding k Most Frequent Words - Three Rounds of Improvement

## Round 1: First Draft Implementation

```python
import re
from collections import defaultdict

STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
             'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be'}

def top_k_frequent_words(text, k):
    """
    Find the k most frequent words in text.
    """
    word_counts = defaultdict(int)
    
    # Normalize case and split on whitespace
    words = text.lower().split()
    
    # Remove punctuation using regex
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        if clean_word and clean_word not in STOPWORDS:
            word_counts[clean_word] += 1
    
    # Sort by count (descending), then alphabetically for ties
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    
    return [word for word, count in sorted_words[:k]]
```

### Issues with Round 1:

1. **Memory**: `text.lower().split()` loads entire text into memory
2. **Inefficiency**: Regex compilation on every word (should compile once)
3. **Unicode**: Basic `\w` might not handle all Unicode properly
4. **Ties**: Returns arbitrary order when count exceeds k but later words tie
5. **Streaming**: Doesn't support streaming at all
6. **Input type**: Only accepts string, not file handles or generators

---

## Round 2: Improved Implementation

```python
import re
from collections import defaultdict
from typing import Iterator, List, Tuple, TextIO
from pathlib import Path
import mmap

STOPWORDS = frozenset({
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'should', 'could', 'may', 'might', 'must', 'can', 'that',
    'this', 'these', 'those', 'it', 'its', 'i', 'you', 'he', 'she', 'we',
    'they', 'what', 'which', 'who', 'w...
```

### MiniMax M2.5

**Generation Time:** 43915ms
**Tokens:** 2327

```

```

### MiniMax M2.1

**Generation Time:** 31150ms
**Tokens:** 2329

```
# Finding k Most Frequent Words: Three Rounds of Improvement

I'll implement this function through three iterations, each improving upon the last with rigorous critique and refinement.

## Round 1: First-Draft Implementation

```python
import re
from collections import Counter

# Common English stopwords
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
    'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
    've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
    'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
    'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
    "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
    "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def top_k_words_v1(text, k=10):
    """
    Find the k most frequent words in a text.
    
    Args:
        text: Input text (string)
        k...
```

### MiniMax M2

**Generation Time:** 8944ms
**Tokens:** 1796

```
### Round 1: First Draft Implementation
```python
import re
from collections import Counter

def top_k_frequent_words(text, k, stopwords=None):
    # Normalize to lowercase and remove punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter stopwords if provided
    if stopwords:
        words = [word for word in words if word not in stopwords]
    # Count word frequencies
    word_counts = Counter(words)
    # Sort by frequency (descending) and then alphabetically (ascending)
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    # Return top k words
    return [word for word, count in sorted_words[:k]]
```

### Round 2: Critique and Improved Version
**Critique of Round 1:**
1. **Memory Inefficiency**: Reads entire text into memory as a string
2. **Punctuation Handling**: Simple regex may not handle all Unicode punctuation
3. **Case Normalization**: Only handles ASCII; fails for non-Latin scripts
4. **Stopwords**: No Unicode support; requires pre-loading entire stopword list
5. **Performance**: Uses Counter and sorting on full dataset
6. **Streaming**: No support for incremental processing

**Improved Version:**
```python
import re
from collections import Counter, defaultdict
import unicodedata

def top_k_frequent_words(text_stream, k, stopwords=None):
    # Initialize data structures
    word_counts = defaultdict(int)
    # Unicode-aware punctuation removal
    punctuation_pattern = re.compile(
        '[' + re.escape(''.join(chr(c) for c in range(0x2000, 0x2070) 
        if unicodedata.category(chr(c)).startswith('P')) + 
        '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') + ']'
    )
    
    # Process stream in chunks
    for chunk in text_stream:
        # Normalize Unicode and case
        normalized = unicodedata.normalize('NFC', chunk).lower()
        # Remove punctuation and extract words
        words = punctuation_pattern.sub(' ', normalized).split()
        
        # Filter stopwords
        if stopwords:
           ...
```

### MiniMax M1

**Generation Time:** 55934ms
**Tokens:** 2732

```
# Finding the K Most Frequent Words - Three Rounds

I'll work through this systematically with increasing rigor.

---

## Round 1: First-Draft Implementation

```python
import re
from collections import Counter

STOPWORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
             'should', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'for',
             'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'between', 'under', 'and', 'but',
             'or', 'nor', 'so', 'yet', 'both', 'either', 'neither', 'not', 'only',
             'own', 'same', 'than', 'too', 'very', 'just', 'if', 'then', 'because',
             'while', 'although', 'though', 'after', 'until', 'unless', 'that',
             'which', 'who', 'whom', 'whose', 'this', 'these', 'those', 'it'}

def find_k_most_frequent(text: str, k: int) -> list[tuple[str, int]]:
    """
    Find the k most frequent words in text.
    """
    # Strip punctuation and normalize case
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter stopwords and count
    filtered = [w for w in words if w not in STOPWORDS]
    counts = Counter(filtered)
    
    # Get top k, break ties alphabetically
    most_common = counts.most_common(k)
    most_common.sort(key=lambda x: (-x[1], x[0]))
    
    return most_common
```

---

## Round 2: Critique & Improved Version

### Critical Weaknesses in Round 1:

1. **Memory Catastrophe**: Loads entire text into memory - cannot handle 10GB files
2. **No Unicode Support**: `\w` in regex only matches ASCII; loses accented characters, Cyrillic, etc.
3. **Fixed Stopwords**: Only English stopwords; not configurable
4. **No Streaming**: No way to process file-like objects incrementally
5. **Inefficient Counting**: Collects all words in a list, then filters - wasteful
6. **Tie-Breaking Bug**: `most_common(k)` does...
```

### MiniMax-01

**Generation Time:** 48920ms
**Tokens:** 2901

```
### Round 1: First-Draft Implementation

**Implementation:**

```python
import string
from collections import Counter
from typing import List, Tuple

def find_k_most_frequent_words(text: str, k: int, stopwords: set) -> List[Tuple[str, int]]:
    # Normalize case and strip punctuation
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.lower().translate(translator)
    
    # Split into words
    words = cleaned_text.split()
    
    # Filter out stopwords
    filtered_words = [word for word in words if word not in stopwords]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Get the k most common words
    most_common = word_counts.most_common(k)
    
    return most_common
```

**Explanation:**

1. **Normalization:** The text is converted to lowercase, and punctuation is stripped using `str.translate`.
2. **Splitting:** The cleaned text is split into words based on whitespace.
3. **Stopword Filtering:** Words that are in the provided `stopwords` set are removed.
4. **Counting:** `Counter` from the `collections` module counts the frequency of each word.
5. **Selecting Top K:** The `most_common` method retrieves the top `k` frequent words.

### Round 2: Critique and Improvement

**Critique:**

1. **Memory Consumption:**
   - The entire text is loaded into memory, which is problematic for large texts (e.g., 10GB+ files).

2. **Stopword Handling:**
   - The function assumes that the `stopwords` set is provided. If not, it could lead to errors or unintended behavior.

3. **Punctuation Stripping:**
   - The use of `str.translate` is efficient but may not handle all Unicode punctuation characters.

4. **Code Style:**
   - The function lacks docstrings and type hints for better readability and maintainability.

5. **Error Handling:**
   - The function does not handle potential errors, such as non-string inputs or invalid `k` values.

**Improved Implementation:**

```python
import string
from collections imp...
```

### Claude Sonnet 4.6

**Generation Time:** 40775ms
**Tokens:** 2316

```
# Round 1: First Draft

```python
import re
from collections import Counter

def top_k_words(text, k, stopwords=None):
    """Find k most frequent words in text."""
    if stopwords is None:
        stopwords = set()
    
    # Normalize and tokenize
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter stopwords
    words = [w for w in words if w not in stopwords]
    
    # Count frequencies
    counts = Counter(words)
    
    # Get top k, with alphabetical tiebreaking
    top_k = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
    
    return top_k
```

**What this does:**
- Lowercases everything
- Extracts only ASCII alpha words (misses Unicode entirely)
- Filters stopwords
- Sorts by frequency descending, then alphabetically for ties
- Returns list of `(word, count)` tuples

---

# Round 1 → Round 2: Critique

**Problems identified:**

1. **Unicode is completely broken.** `[a-zA-Z]` misses `café`, `naïve`, `Ångström`, `日本語`. The task explicitly requires Unicode handling.

2. **Punctuation stripping is wrong.** `\b[a-zA-Z]+\b` fails on `"don't"` (splits into `don` and `t`), hyphenated words like `well-known`, and contractions. Need a smarter tokenization strategy.

3. **Entire text loaded into memory.** The function signature takes `text` as a string — impossible for 10GB files. No streaming whatsoever.

4. **`Counter.most_common(k)` not used.** The current sort is O(n log n) over all unique words. `most_common(k)` uses `heapq.nlargest` which is O(n log k) — strictly better when k << n.

5. **Tiebreaking is wrong.** `sorted(..., key=lambda x: (-x[1], x[0]))` does sort the full list, but since we only call `most_common`-style logic later, we need to be careful. Actually here it's fine, but it sorts ALL items then slices — wasteful.

6. **No input validation.** `k <= 0`, `k > vocabulary size`, `None` text — all unhandled.

7. **Stopwords type not enforced.** Passing a list causes O(n) lookup per word instead of O(1) for a set.

8. **No ...
```

### GPT-5.4

**Generation Time:** 32391ms
**Tokens:** 2294

```
Below are **3 rounds** of the same function, each followed by a **ruthless critique** and a strictly better revision.

---

# Round 1 — first draft

This is the “what comes naturally” version: simple, readable, but not optimized for very large inputs.

```python
import re
from collections import Counter
from typing import Iterable, List, Tuple, Optional, Set

WORD_RE = re.compile(r"\w+", re.UNICODE)

def top_k_frequent_words_v1(
    text: str,
    k: int,
    stopwords: Optional[Set[str]] = None,
) -> List[Tuple[str, int]]:
    """
    Return the k most frequent words in text.

    Features:
    - Unicode-aware word matching via \\w+
    - punctuation stripping by extracting words
    - case normalization via lower()
    - ties broken alphabetically
    - optional stopword filtering

    Returns:
        List of (word, count), sorted by:
        - descending frequency
        - alphabetical order for ties
    """
    if k <= 0:
        return []

    stopwords = {w.lower() for w in stopwords} if stopwords else set()

    words = WORD_RE.findall(text.lower())
    counts = Counter(w for w in words if w not in stopwords)

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
```

## Critique of Round 1

This works for many small/medium cases, but it has a lot of problems.

### Correctness / behavior issues
1. **Not actually streaming**  
   It takes a full `str`. If the text is 10GB, this is unusable.

2. **`lower()` instead of `casefold()`**  
   `lower()` is weaker for Unicode case normalization. `casefold()` is more correct for multilingual text.

3. **`\w+` is a sloppy definition of “word”**  
   - Includes digits and underscore.
   - Splits contractions/hyphenated words in a way that may or may not be desired.
   - Depends on regex semantics rather than explicit token rules.
   - May keep things like `"___"` as a token.

4. **Stopword normalization is incomplete**  
   Uses `lower()` rather than `casefold()`, so stopword matching can disagree with tok...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*