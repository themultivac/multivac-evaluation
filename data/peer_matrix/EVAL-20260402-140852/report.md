# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-140852
**Timestamp:** 2026-04-02T14:08:52.478798
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Write a Python function that parses unified diff format (the output of `git diff`) and returns a structured representation: files changed, lines added/removed/modified, hunks with context. Handle edge cases: binary files, renamed files, mode changes, and empty diffs. Include tests with real diff examples.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Gemini 3 Flash Preview | 8.03 | 6.80 | 9.00 | 0.69 |
| 2 | GPT-5.4 | 7.92 | 7.00 | 9.00 | 0.63 |
| 3 | Grok 4.20 | 7.39 | 6.00 | 9.15 | 1.05 |
| 4 | Claude Opus 4.6 | 6.53 | 2.25 | 9.00 | 2.24 |
| 5 | DeepSeek V3 | 6.46 | 5.00 | 8.15 | 1.03 |
| 6 | GPT-OSS-120B | 6.28 | 2.80 | 8.80 | 1.97 |
| 7 | Claude Sonnet 4.6 | 5.49 | 1.65 | 8.60 | 2.18 |
| 8 | MiMo-V2-Flash | 4.36 | 2.45 | 8.60 | 1.89 |
| 9 | Gemini 3.1 Pro | 1.62 | 0.20 | 4.00 | 1.35 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.45 |
| 2 | Claude Opus 4.6 | 5.12 |
| 3 | GPT-OSS-120B | 5.31 |
| 4 | Claude Sonnet 4.6 | 5.81 |
| 5 | Gemini 3.1 Pro | 5.86 |
| 6 | Grok 4.20 | 6.65 |
| 7 | MiniMax M2.5 | 6.69 |
| 8 | Gemini 3 Flash Preview | 7.04 |
| 9 | MiMo-V2-Flash | 7.33 |
| 10 | DeepSeek V3 | 8.03 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 74

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

**Generation Time:** 22877ms
**Tokens:** 2117

```
```python
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class DiffLine:
    kind: str  # 'context', 'add', 'del'
    content: str


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_header: str = ""
    lines: List[DiffLine] = field(default_factory=list)


@dataclass
class FileDiff:
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    a_path: Optional[str] = None
    b_path: Optional[str] = None
    is_binary: bool = False
    is_rename: bool = False
    rename_from: Optional[str] = None
    rename_to: Optional[str] = None
    old_mode: Optional[str] = None
    new_mode: Optional[str] = None
    new_file_mode: Optional[str] = None
    deleted_file_mode: Optional[str] = None
    index: Optional[str] = None
    hunks: List[Hunk] = field(default_factory=list)

    added_lines: int = 0
    removed_lines: int = 0
    modified_lines: int = 0  # computed as paired add/remove within hunks


@dataclass
class ParsedDiff:
    files: List[FileDiff] = field(default_factory=list)


_DIFF_GIT_RE = re.compile(r"^diff --git a/(.+?) b/(.+)$")
_HUNK_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@(?: (?P<section>.*))?$"
)


def _strip_prefix_path(line: str, prefix: str) -> str:
    if line.startswith(prefix):
        return line[len(prefix):]
    return line


def _compute_modified_lines(hunks: List[Hunk]) -> Tuple[int, int, int]:
    added = 0
    removed = 0
    modified = 0

    for hunk in hunks:
        i = 0
        lines = hunk.lines
        while i < len(lines):
            if lines[i].kind == "del":
                del_count = 0
                while i < len(lines) and lines[i].kind == "del":
                    del_count += 1
                    i += 1
                add_count = 0
                j = i
                while j < len(lines) and lines[j].kind ==...
```

### Claude Opus 4.6

**Generation Time:** 186599ms
**Tokens:** 2119

```


# Unified Diff Parser

A comprehensive parser for unified diff format (git diff output) with full support for edge cases.

```python
"""
Unified Diff Parser

Parses the output of `git diff` (unified diff format) into a structured representation.

Handles:
- Regular file changes (additions, deletions, modifications)
- Binary files
- Renamed/copied files
- Mode changes (permissions)
- Empty diffs
- No newline at end of file markers
- Multiple hunks per file
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class FileChangeType(Enum):
    ADDED = auto()
    DELETED = auto()
    MODIFIED = auto()
    RENAMED = auto()
    COPIED = auto()
    MODE_CHANGED = auto()


class LineChangeType(Enum):
    ADDITION = auto()
    DELETION = auto()
    CONTEXT = auto()


@dataclass
class DiffLine:
    """A single line within a hunk."""
    change_type: LineChangeType
    content: str
    old_line_number: Optional[int] = None  # Line number in the old file
    new_line_number: Optional[int] = None  # Line number in the new file
    no_newline_at_eof: bool = False  # True if followed by "\ No newline at end of file"

    def __repr__(self) -> str:
        prefix = {
            LineChangeType.ADDITION: "+",
            LineChangeType.DELETION: "-",
            LineChangeType.CONTEXT: " ",
        }[self.change_type]
        old = self.old_line_number or ""
        new = self.new_line_number or ""
        return f"DiffLine({prefix} old={old} new={new} {self.content!r})"


@dataclass
class Hunk:
    """A hunk within a file diff, representing a contiguous block of changes."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_header: str = ""  # Optional @@ ... @@ section header (e.g., function name)
    lines: list[DiffLine] = field(default_factory=list)

    @property
    def additions(self) -> list[DiffLine]:
        return [l for l in self.lines if...
```

### Gemini 3.1 Pro

**Generation Time:** 23262ms
**Tokens:** 2107

```
 tests (Real Diff Examples):**
    I need a comprehensive test suite covering:
    1.  Standard modification (context, additions, removals)
    2.  Empty diff
    3.  Binary file change
    4.  Renamed file
    5.  Mode change (permissions)
    6.  New file (--- /dev/null)
    7.
```

### Claude Sonnet 4.6

**Generation Time:** 24733ms
**Tokens:** 2119

```
```python
"""
Unified diff parser that handles git diff output format.
Parses diffs into structured representations with full edge case handling.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import unittest


# ─────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────

class LineType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    CONTEXT = "context"


@dataclass
class DiffLine:
    line_type: LineType
    content: str          # raw text without the leading +/-/space
    old_lineno: Optional[int]  # None for added lines
    new_lineno: Optional[int]  # None for removed lines

    def __repr__(self) -> str:
        prefix = {
            LineType.ADDED: "+",
            LineType.REMOVED: "-",
            LineType.CONTEXT: " ",
        }[self.line_type]
        return f"DiffLine({prefix!r}, old={self.old_lineno}, new={self.new_lineno}, {self.content!r})"


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_heading: str          # optional function/class name after @@
    lines: list[DiffLine] = field(default_factory=list)

    @property
    def added_count(self) -> int:
        return sum(1 for l in self.lines if l.line_type == LineType.ADDED)

    @property
    def removed_count(self) -> int:
        return sum(1 for l in self.lines if l.line_type == LineType.REMOVED)

    def __repr__(self) -> str:
        return (
            f"Hunk(old={self.old_start},{self.old_count} "
            f"new={self.new_start},{self.new_count} "
            f"+{self.added_count}/-{self.removed_count})"
        )


@dataclass
class FileDiff:
    # paths
    old_path: Optional[str]       # None for new files
    new_path: Optional[str]       # None for deleted files
    original_path: Optional[str]  # set when renamed/copied

    # flags
    is_new_file: bool = False
    is_deleted_file: bool = False
    is_binar...
```

### Grok 4.20

**Generation Time:** 21994ms
**Tokens:** 2232

```
**Here's a complete Python solution for parsing unified diff format:**

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import re
from pathlib import Path


@dataclass
class Hunk:
    """Represents a hunk in a unified diff."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    header: str
    lines: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.lines:
            self.lines = []


@dataclass
class FileDiff:
    """Represents changes to a single file."""
    filename: str
    status: str  # 'added', 'deleted', 'modified', 'renamed', 'copied'
    old_filename: Optional[str] = None
    mode_change: Optional[str] = None  # e.g. "100644..100755"
    is_binary: bool = False
    hunks: List[Hunk] = field(default_factory=list)
    added: int = 0
    removed: int = 0
    modified: int = 0


class DiffParser:
    """Parses unified diff output (git diff)."""
    
    def __init__(self):
        self.diff_header = re.compile(r'^diff --git a/(.+?) b/(.+)$')
        self.file_header = re.compile(r'^(---|\+\+\+)\s+(?:a/|b/)?(.+?)(?:\s+\(from\s+(.+?)\))?$')
        self.hunk_header = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: (.*))?$')
        self.binary_file = re.compile(r'^Binary files .* and .* differ$')
    
    def parse(self, diff_text: str) -> List[FileDiff]:
        """Parse unified diff text and return structured representation."""
        if not diff_text or not diff_text.strip():
            return []
            
        lines = diff_text.strip().splitlines()
        files = []
        current_file = None
        current_hunk = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # diff --git header
            if match := self.diff_header.match(line):
                if current_file:
                    files.append(current_file)
                
              ...
```

### DeepSeek V3

**Generation Time:** 111015ms
**Tokens:** 2116

```
# Unified Diff Parser in Python

Here's a comprehensive Python function that parses unified diff format (like git diff output) into a structured representation:

```python
import re
from typing import List, Dict, Optional, Union

class Hunk:
    def __init__(self, old_start: int, old_lines: int, new_start: int, new_lines: int, lines: List[str]):
        self.old_start = old_start
        self.old_lines = old_lines
        self.new_start = new_start
        self.new_lines = new_lines
        self.lines = lines  # List of lines with +, -, or ' ' prefixes
    
    def __repr__(self):
        return f"Hunk(old={self.old_start}-{self.old_start+self.old_lines-1}, new={self.new_start}-{self.new_start+self.new_lines-1}, lines={len(self.lines)})"

class FileDiff:
    def __init__(self):
        self.old_file: Optional[str] = None
        self.new_file: Optional[str] = None
        self.is_binary: bool = False
        self.is_rename: bool = False
        self.is_mode_change: bool = False
        self.hunks: List[Hunk] = []
        self.added_lines: int = 0
        self.removed_lines: int = 0
        self.modified_lines: int = 0
    
    def __repr__(self):
        return f"FileDiff(old={self.old_file}, new={self.new_file}, binary={self.is_binary}, hunks={len(self.hunks)})"

def parse_unified_diff(diff_text: str) -> List[FileDiff]:
    """
    Parses unified diff format text into structured FileDiff objects.
    
    Args:
        diff_text: String containing the unified diff output
        
    Returns:
        List of FileDiff objects representing each file in the diff
    """
    if not diff_text.strip():
        return []
    
    file_diffs = []
    current_file_diff = None
    current_hunk = None
    in_hunk = False
    
    # Regular expressions for matching diff components
    file_header_re = re.compile(r'^diff --git a/(.*) b/(.*)$')
    binary_file_re = re.compile(r'^Binary files (.+) and (.+) differ$')
    rename_from_re = re.compile(r'^rename from (.+)$')
    renam...
```

### GPT-OSS-120B

**Generation Time:** 18024ms
**Tokens:** 2183

```
Below is a **self‑contained** Python module that

* parses a unified diff (the exact output you get from `git diff`, `git show`, `git format-patch` …)  
* builds a rich, easy‑to‑navigate data structure describing the change set  
* gracefully handles the special cases you asked for (binary files, renames, mode changes, empty diffs)  
* ships with a small test‑suite that uses real‑world diff excerpts.

```python
"""
diff_parser.py

A tiny, dependency‑free parser for Git’s unified diff format.

Typical usage
-------------
>>> from diff_parser import parse_unified_diff
>>> changes = parse_unified_diff(diff_text)
>>> for f in changes:
...     print(f['change_type'], f['old_path'], '→', f['new_path'])
...     for h in f['hunks']:
...         print('  Hunk', h['old_start'], h['new_start'])
...         for line in h['lines']:
...             print('    ', line['type'], line['content'])
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import PurePath
from typing import List, Literal, Optional, Tuple


# --------------------------------------------------------------------------- #
#   Data model (dataclasses – makes the test output readable)
# --------------------------------------------------------------------------- #

LineType = Literal["context", "added", "removed"]
ChangeType = Literal[
    "added",
    "deleted",
    "modified",
    "renamed",
    "mode_changed",
    "binary",
    "unchanged",  # for an empty diff that touches no file
]


@dataclass
class DiffLine:
    """One line inside a hunk."""
    type: LineType
    content: str  # without the leading +/−/space


@dataclass
class Hunk:
    """A single hunk (the @@ … @@ header plus its lines)."""
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[DiffLine] = field(default_factory=list)

    @property
    def added(self) -> int:
        return sum(1 for l in self.lines if l.type == "added")

    @property
    def removed...
```

### Gemini 3 Flash Preview

**Generation Time:** 13404ms
**Tokens:** 2020

```
This implementation uses a state-machine approach to parse the unified diff format. It handles the specific metadata generated by `git diff`, including file renames, mode changes, and binary files.

### The Parser Implementation

```python
import re

class DiffParser:
    def __init__(self, diff_text):
        self.diff_text = diff_text
        self.files = []

    def parse(self):
        if not self.diff_text or not self.diff_text.strip():
            return []

        lines = self.diff_text.splitlines()
        current_file = None
        current_hunk = None
        i = 0

        while i < len(lines):
            line = lines[i]

            # Start of a new file
            if line.startswith('diff --git'):
                current_file = {
                    'old_path': None,
                    'new_path': None,
                    'status': 'modified', # default
                    'old_mode': None,
                    'new_mode': None,
                    'is_binary': False,
                    'hunks': []
                }
                self.files.append(current_file)
                
                # Extract paths from git diff a/path b/path
                match = re.match(r'^diff --git a/(.*) b/(.*)$', line)
                if match:
                    current_file['old_path'] = match.group(1)
                    current_file['new_path'] = match.group(2)
                i += 1
                continue

            # Metadata headers
            if line.startswith('old mode '):
                current_file['old_mode'] = line[9:]
            elif line.startswith('new mode '):
                current_file['new_mode'] = line[9:]
            elif line.startswith('new file mode '):
                current_file['status'] = 'added'
                current_file['new_mode'] = line[14:]
            elif line.startswith('deleted file mode '):
                current_file['status'] = 'deleted'
                current_file['old_mode'] = line[18:]
            eli...
```

### MiniMax M2.5

**Generation Time:** 21437ms
**Tokens:** 2149

```

```

### MiMo-V2-Flash

**Generation Time:** 19814ms
**Tokens:** 2147

```
Here is a robust Python function to parse unified diff format, along with a comprehensive test suite.

### Implementation

This implementation uses standard library modules (`re`, `collections`, `io`) to ensure no external dependencies are required.

```python
import re
import sys
from collections import namedtuple, defaultdict
from typing import List, Dict, Optional, Tuple, Iterator, Union

# Data structures for the output
FileChange = namedtuple('FileChange', [
    'old_path', 
    'new_path', 
    'status',  # 'added', 'removed', 'modified', 'renamed', 'binary'
    'stats',   # Dict: {'insertions': int, 'deletions': int}
    'hunks'    # List[Hunk]
])

Hunk = namedtuple('Hunk', [
    'old_start', 
    'old_lines', 
    'new_start', 
    'new_lines', 
    'content',   # List of lines including context and markers
    'changes'    # List[LineChange]
])

LineChange = namedtuple('LineChange', [
    'type',      # 'added', 'removed', 'context'
    'line_no_old', 
    'line_no_new', 
    'content'
])

class UnifiedDiffParser:
    """
    Parses unified diff format (standard git diff output) into structured data.
    """
    
    # Regex patterns for diff headers
    RE_HEADER = re.compile(r'^diff --git a/(?P<old>.*) b/(?P<new>.*)$')
    RE_SIMILARITY = re.compile(r'^similarity index (?P<percent>\d+)%$')
    RE_RENAME_FROM = re.compile(r'^rename from (?P<old>.*)$')
    RE_RENAME_TO = re.compile(r'^rename to (?P<new>.*)$')
    RE_OLD_MODE = re.compile(r'^old mode (?P<mode>\d+)$')
    RE_NEW_MODE = re.compile(r'^new mode (?P<mode>\d+)$')
    RE_BINARY = re.compile(r'^Binary files (?P<old>.*) and (?P<new>.*) differ$')
    
    # Regex for hunk header: @@ -old_start,old_lines +new_start,new_lines @@
    RE_HUNK_HEADER = re.compile(
        r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@'
    )

    def __init__(self):
        self.files: List[FileChange] = []

    def parse(self, diff_text: str) -> List[FileChange]:
        """
        Main entry point. Parses the full diff t...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*