# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-121519
**Timestamp:** 2026-04-02T12:15:19.299169
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Write a Python function that parses deeply nested JSON with the following requirements:
1. Handle missing keys gracefully (return None, don't crash)
2. Support a path syntax like "user.profile.settings.theme"
3. Handle arrays with index syntax like "users[0].name"
4. Return a typed result with proper error messages for debugging
5. Handle circular reference detection

Include type hints and comprehensive docstrings.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.13 | 8.80 | 9.80 | 0.39 |
| 2 | GPT-OSS-120B | 8.86 | 7.65 | 9.80 | 0.72 |
| 3 | MiMo-V2-Flash | 8.52 | 6.75 | 9.80 | 1.05 |
| 4 | DeepSeek V3 | 8.16 | 6.75 | 9.80 | 0.88 |
| 5 | Grok 4.20 | 7.87 | 6.00 | 9.60 | 1.32 |
| 6 | Gemini 3 Flash Preview | 7.58 | 6.30 | 9.20 | 0.90 |
| 7 | Claude Opus 4.6 | 7.26 | 3.35 | 9.60 | 1.92 |
| 8 | Claude Sonnet 4.6 | 6.06 | 3.25 | 9.35 | 2.04 |
| 9 | MiniMax M2.5 | 6.01 | 2.85 | 9.00 | 2.14 |
| 10 | Gemini 3.1 Pro | 2.75 | 0.60 | 6.85 | 2.04 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.49 |
| 2 | GPT-OSS-120B | 6.63 |
| 3 | Claude Opus 4.6 | 6.75 |
| 4 | Gemini 3.1 Pro | 6.85 |
| 5 | Grok 4.20 | 7.17 |
| 6 | Claude Sonnet 4.6 | 7.21 |
| 7 | MiniMax M2.5 | 7.31 |
| 8 | MiMo-V2-Flash | 7.80 |
| 9 | Gemini 3 Flash Preview | 8.84 |
| 10 | DeepSeek V3 | 9.30 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 24856ms
**Tokens:** 2137

```
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, List, Optional, Type, TypeVar, Union, get_args, get_origin
import re


T = TypeVar("T")


@dataclass
class ParseResult(Generic[T]):
    """
    Result object returned by `get_json_path`.

    Attributes:
        value:
            The extracted value if parsing succeeded, otherwise None.

        found:
            True if the full path was successfully resolved, False otherwise.

        error:
            A human-readable error message useful for debugging. This is None
            when parsing succeeds.

        path:
            The original path expression that was requested.

        resolved_path:
            A normalized representation of the path segments that were
            successfully resolved before success/failure.
    """
    value: Optional[T]
    found: bool
    error: Optional[str]
    path: str
    resolved_path: str


_PATH_TOKEN_RE = re.compile(r"""
    ([^. \[\]]+)      # key name
    |                 # or
    \[(\d+)\]         # array index, e.g. [0]
""", re.VERBOSE)


def _tokenize_path(path: str) -> List[Union[str, int]]:
    """
    Convert a path like 'users[0].profile.name' into tokens.

    Args:
        path:
            Dot/bracket path expression.

    Returns:
        A list of tokens where object keys are strings and array indices are ints.

    Raises:
        ValueError:
            If the path is empty or malformed.
    """
    if not path or not path.strip():
        raise ValueError("Path cannot be empty.")

    tokens: List[Union[str, int]] = []
    pos = 0

    while pos < len(path):
        if path[pos] == ".":
            pos += 1
            continue

        match = _PATH_TOKEN_RE.match(path, pos)
        if not match:
            raise ValueError(f"Invalid path syntax near: {path[pos:]!r}")

        key, index = match.groups()
        if key is not None:
            tokens.append(key)
        elif index is ...
```

### Claude Opus 4.6

**Generation Time:** 29989ms
**Tokens:** 2149

```


```python
"""
A robust deeply nested JSON parser with path syntax support,
circular reference detection, and comprehensive error handling.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union


class ParseStatus(Enum):
    """Status codes for parse results."""
    SUCCESS = "success"
    KEY_NOT_FOUND = "key_not_found"
    INDEX_OUT_OF_RANGE = "index_out_of_range"
    INVALID_INDEX = "invalid_index"
    TYPE_ERROR = "type_error"
    CIRCULAR_REFERENCE = "circular_reference"
    INVALID_PATH = "invalid_path"
    INVALID_JSON = "invalid_json"


@dataclass
class ParseResult:
    """
    Container for the result of a JSON path parse operation.

    Attributes:
        value: The extracted value, or None if extraction failed.
        status: A ParseStatus enum indicating success or the type of failure.
        path: The original path that was queried.
        error_message: A human-readable description of what went wrong (if anything).
        partial_path: The portion of the path that was successfully traversed
                      before failure occurred.
    """
    value: Any = None
    status: ParseStatus = ParseStatus.SUCCESS
    path: str = ""
    error_message: str = ""
    partial_path: str = ""

    @property
    def is_success(self) -> bool:
        """Check if the parse operation was successful."""
        return self.status == ParseStatus.SUCCESS

    def __repr__(self) -> str:
        if self.is_success:
            return f"ParseResult(value={self.value!r}, status={self.status.value})"
        return (
            f"ParseResult(status={self.status.value}, "
            f"error_message={self.error_message!r}, "
            f"partial_path={self.partial_path!r})"
        )


@dataclass
class _TraversalState:
    """
    Internal state tracker for traversal, including circular reference detection.

    Attributes:
        visited_ids: Set of Python object ...
```

### Gemini 3.1 Pro

**Generation Time:** 31074ms
**Tokens:** 2137

```
Here is a robust, fully-typed Python solution that meets all your requirements. 

It uses a generic `dataclass` to return structured, typed results, employs regex to cleanly parse the path syntax, and keeps a memory of visited object IDs to detect circular references.

### The Code

```python
import re
from typing import Any, TypeVar, Generic, Optional, Union, Type
```

### Claude Sonnet 4.6

**Generation Time:** 32083ms
**Tokens:** 2149

```
```python
"""
Deeply nested JSON parser with robust error handling and circular reference detection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional, Union


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ParseResult:
    """
    Typed container returned by every ``get_nested`` call.

    Attributes
    ----------
    value:
        The extracted value, or ``None`` when the path could not be resolved.
    success:
        ``True`` when the path was resolved without errors.
    error:
        Human-readable explanation of what went wrong (empty string on success).
    path:
        The path string that was used for the lookup.
    resolved_path:
        The portion of the path that was successfully resolved before any error.
    """

    value: Any
    success: bool
    error: str
    path: str
    resolved_path: str = field(default="")

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def unwrap(self) -> Any:
        """Return the value or raise ``ValueError`` on failure."""
        if not self.success:
            raise ValueError(f"ParseResult error at '{self.path}': {self.error}")
        return self.value

    def unwrap_or(self, default: Any) -> Any:
        """Return the value on success, otherwise *default*."""
        return self.value if self.success else default

    def __repr__(self) -> str:  # pragma: no cover
        status = "OK" if self.success else "ERR"
        return (
            f"ParseResult({status}, path={self.path!r}, "
            f"value={self.value!r}, error={self.error!r})"
        )


# ---------------------------------------------------------------------------
# Path tokeniser
# -----------------...
```

### Grok 4.20

**Generation Time:** 7867ms
**Tokens:** 1788

```
**Here's a robust Python function that meets all your requirements:**

```python
from typing import Any, Dict, List, Optional, Union, TypeVar, cast
import json
from functools import lru_cache
import re

T = TypeVar('T')

def parse_nested_json(
    data: Union[Dict[str, Any], List[Any], str],
    path: str,
    default: Any = None
) -> Optional[Any]:
    """
    Safely parse deeply nested JSON data using dot and bracket notation.
    
    Args:
        data: JSON data as dict, list, or JSON string
        path: Path to the desired value using dot and bracket notation.
              Examples: "user.profile.settings.theme", "users[0].name", 
                       "data[2].items[0].value"
        default: Value to return if the path doesn't exist (default: None)
    
    Returns:
        The value at the specified path, or default if not found.
        Returns None for missing keys/values (unless default is specified).
    
    Raises:
        ValueError: If the JSON string is invalid or path syntax is malformed.
        TypeError: If data is not a valid JSON structure.
    
    Examples:
        >>> data = {"user": {"profile": {"settings": {"theme": "dark"}}}}
        >>> parse_nested_json(data, "user.profile.settings.theme")
        'dark'
        
        >>> parse_nested_json(data, "user.missing.key")
        None
        
        >>> data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        >>> parse_nested_json(data, "users[1].name")
        'Bob'
    """
    
    # Convert JSON string to Python object if needed
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}") from e
    
    if not isinstance(data, (dict, list)):
        raise TypeError(f"Expected dict or list, got {type(data).__name__}")
    
    if not path or not isinstance(path, str):
        return default
    
    # Circular reference detection setup
    seen_ids = set()
  ...
```

### DeepSeek V3

**Generation Time:** 45018ms
**Tokens:** 1701

```
Here's a Python function that meets all your requirements for parsing deeply nested JSON with path syntax support, graceful error handling, and circular reference detection:

```python
from typing import Any, Optional, Union, Dict, List, Tuple, TypeVar
import json

T = TypeVar('T')

class NestedJSONParserError(Exception):
    """Base class for parsing errors."""
    pass

class CircularReferenceError(NestedJSONParserError):
    """Raised when a circular reference is detected."""
    pass

class InvalidPathError(NestedJSONParserError):
    """Raised when the path syntax is invalid."""
    pass

class ArrayIndexError(NestedJSONParserError):
    """Raised when an array index is out of bounds or invalid."""
    pass

def parse_nested_json(
    data: Union[Dict[str, Any], List[Any], str],
    path: str,
    default: Optional[T] = None,
    *,
    _visited: Optional[List[int]] = None
) -> Tuple[Optional[T], Optional[str]]:
    """
    Parses deeply nested JSON data using a path syntax.
    
    Args:
        data: The JSON data to parse (can be dict, list, or JSON string)
        path: The path to the value in dot notation (e.g., "user.profile.settings.theme")
        default: Default value to return if path not found or error occurs
        _visited: Internal use only - tracks visited objects for circular reference detection
        
    Returns:
        A tuple containing:
        - The parsed value (or default if not found/error)
        - An error message if something went wrong (None if successful)
        
    Examples:
        >>> data = {'user': {'profile': {'settings': {'theme': 'dark'}}}}
        >>> parse_nested_json(data, 'user.profile.settings.theme')
        ('dark', None)
        
        >>> data = {'users': [{'name': 'Alice'}, {'name': 'Bob'}]}
        >>> parse_nested_json(data, 'users[1].name')
        ('Bob', None)
        
        >>> parse_nested_json(data, 'nonexistent.path', 'default')
        ('default', "Key 'nonexistent' not found")
    """
    ...
```

### GPT-OSS-120B

**Generation Time:** 115421ms
**Tokens:** 2702

```
```python
"""
json_path.py
------------

Utility for extracting values from deeply‑nested JSON‑like structures.

Features
~~~~~~~~
1. **Graceful handling of missing keys / indices** – the function never raises a
   ``KeyError`` or ``IndexError``; it simply returns ``None``.
2. **Dot‑notation with array indexing** – a path such as
   ``"users[0].profile.settings.theme"`` is parsed and followed automatically.
3. **Typed result** – the return type is inferred from the caller via a generic
   type variable, while a custom ``JsonPathError`` carries a detailed, human‑
   readable diagnostic message.
4. **Circular‑reference detection** – if the input object graph contains a
   reference loop (e.g. ``a = {}; a["self"] = a``) the function aborts with a
   clear error instead of recursing forever.

Typical usage
~~~~~~~~~~~~~

>>> from json_path import get_json_path, JsonPathError
>>> data = {
...     "users": [
...         {"name": "Alice", "profile": {"settings": {"theme": "dark"}}},
...         {"name": "Bob"}
...     ]
... }
>>> get_json_path(data, "users[0].profile.settings.theme")
'dark'
>>> get_json_path(data, "users[1].profile.settings.theme") is None
True
>>> get_json_path(data, "users[2].name") is None
True
>>> # circular reference detection
>>> a = {}
>>> a["self"] = a
>>> get_json_path(a, "self.self")   # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
json_path.JsonPathError: Circular reference detected at path 'self.self'
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, TypeVar, Union, overload, Set

# --------------------------------------------------------------------------- #
# Types
# --------------------------------------------------------------------------- #

JSONType = Union[
    Dict[str, Any],
    List[Any],
    str,
    int,
    float,
    bool,
    None,
]

_T = TypeVar("_T")  # Generic return type


# --------------------------------------------------------------------------- #...
```

### Gemini 3 Flash Preview

**Generation Time:** 8213ms
**Tokens:** 1355

```
To handle deeply nested JSON with support for both object keys and array indices, we can use a recursive approach combined with Regular Expressions to parse the path segments.

The following solution uses `typing` for type safety and includes a custom exception for clear debugging.

```python
import re
from typing import Any, Union, Optional, List, Dict

class JSONPathError(Exception):
    """Custom exception for path parsing errors."""
    pass

def get_nested_value(
    data: Union[Dict, List], 
    path: str, 
    default: Any = None
) -> Any:
    """
    Parses a deeply nested dictionary/list using a dot and bracket notation.
    
    Args:
        data: The JSON-like structure (dict or list) to traverse.
        path: A string path like "users[0].profile.settings.theme".
        default: The value to return if the path is not found.

    Returns:
        The value at the specified path, or the default value (None).

    Example:
        >>> data = {"users": [{"name": "Alice"}]}
        >>> get_nested_value(data, "users[0].name")
        'Alice'
    """
    if not path:
        return data

    # Regex to split by dots, but handle array brackets: "users[0]" -> ["users", "0"]
    # This matches alphanumeric keys or digits inside brackets
    tokens = re.findall(r'[^.\[\]]+', path)
    
    # To handle circular references, we track the identity of objects visited
    # in the current resolution chain.
    visited_ids = set()

    def _resolve(current: Any, remaining_tokens: List[str]) -> Any:
        if not remaining_tokens:
            return current
        
        # Circular Reference Detection
        # Note: We only check containers (dict/list)
        if isinstance(current, (dict, list)):
            if id(current) in visited_ids:
                return default # Found circularity, return default instead of infinite loop
            visited_ids.add(id(current))

        token = remaining_tokens[0]
        rest = remaining_tokens[1:]

        try:
          ...
```

### MiniMax M2.5

**Generation Time:** 78192ms
**Tokens:** 2169

```
# Deeply Nested JSON Parser

Here's a comprehensive Python solution with all the requested features:

```python
"""
Deeply Nested JSON Parser

A robust JSON parsing utility that supports dot-notation path traversal
with array indexing, graceful error handling, and circular reference detection.
"""

from typing import Any, Optional, Union, Dict, List, Set
from dataclasses import dataclass, field
from enum import Enum
import re


class ParseErrorType(Enum):
    """Enumeration of possible parsing error types."""
    MISSING_KEY = "missing_key"
    INVALID_INDEX = "invalid_index"
    TYPE_ERROR = "type_error"
    CIRCULAR_REFERENCE = "circular_reference"
    INVALID_PATH = "invalid_path"
    EMPTY_PATH = "empty_path"


@dataclass
class ParseResult:
    """
    Typed result container for JSON path parsing.
    
    Attributes:
        success: Whether the parsing was successful
        value: The parsed value if successful, None otherwise
        error_type: Type of error if parsing failed
        error_message: Human-readable error description
        path_traversed: List of path segments successfully traversed
        visited_ids: Set of object IDs visited (for circular reference detection)
    """
    success: bool
    value: Any = None
    error_type: Optional[ParseErrorType] = None
    error_message: Optional[str] = None
    path_traversed: List[str] = field(default_factory=list)
    visited_ids: Set[int] = field(default_factory=set)
    
    def __repr__(self) -> str:
        if self.success:
            return f"<ParseResult success=True, value={self.value!r}>"
        return (
            f"<ParseResult success=False, error={self.error_type}, "
            f"message={self.error_message!r}>"
        )


class CircularReferenceError(Exception):
    """Raised when a circular reference is detected in the JSON structure."""
    pass


class JSONPathParser:
    """
    Parser for deeply nested JSON structures using dot-notation paths.
    
    Supports:
        - Dot n...
```

### MiMo-V2-Flash

**Generation Time:** 17564ms
**Tokens:** 2169

```
Here is a robust Python function that meets all your requirements. It includes type hints, comprehensive docstrings, support for bracket notation, circular reference detection, and detailed error handling.

```python
import json
import re
from typing import Any, Dict, List, Optional, Union, Tuple

# Type alias for JSON data structures
JSONData = Union[Dict[str, Any], List[Any], Any]

class PathResolutionError(Exception):
    """Custom exception for path resolution failures."""
    pass

def get_nested_value(
    data: JSONData, 
    path: str, 
    default: Any = None, 
    max_depth: int = 1000
) -> Tuple[Any, Optional[str]]:
    """
    Parses deeply nested JSON data using a dot-notation path with array indexing.

    This function safely traverses dictionaries and lists, handling missing keys 
    or indices by returning a default value. It includes protection against 
    circular references and stack overflows.

    Args:
        data (JSONData): The JSON object (dict, list, or scalar) to traverse.
        path (str): The path to the target value. 
            Syntax examples:
            - "user.profile.theme"
            - "users[0].name"
            - "data.items[1].tags[2]"
        default (Any, optional): The value to return if the path is not found 
            or an error occurs. Defaults to None.
        max_depth (int, optional): Safety limit for recursion depth to prevent 
            stack overflow on circular references. Defaults to 1000.

    Returns:
        Tuple[Any, Optional[str]]:
            - A tuple containing (value, error_message).
            - If successful, returns (value, None).
            - If an error occurs, returns (default, error_message).

    Raises:
        PathResolutionError: Only raised if internal logic fails unexpectedly 
            (e.g., recursion depth exceeded).
    
    Example:
        >>> data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        >>> value, error = get_nested_value(data, "users[1].name")
    ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*