# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-122714
**Timestamp:** 2026-04-02T12:27:14.022500
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Convert this Python code to idiomatic Rust. The code must compile, handle errors properly, and follow Rust best practices.

```python
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    completed: bool
    due_date: Optional[datetime]
    tags: List[str]

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title: str, due_date: Optional[datetime] = None, tags: List[str] = None) -> Task:
        task = Task(
            id=self.next_id,
            title=title,
            completed=False,
            due_date=due_date,
            tags=tags or []
        )
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                return True
        return False
    
    def get_overdue(self) -> List[Task]:
        now = datetime.now()
        return [t for t in self.tasks if t.due_date and t.due_date < now and not t.completed]
```

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Opus 4.6 | 8.94 | 7.55 | 9.80 | 0.75 |
| 2 | GPT-5.4 | 8.88 | 7.40 | 9.80 | 0.77 |
| 3 | Claude Sonnet 4.6 | 8.66 | 6.50 | 9.60 | 1.05 |
| 4 | Grok 4.20 | 8.38 | 7.00 | 9.80 | 0.84 |
| 5 | Gemini 3 Flash Preview | 8.26 | 6.20 | 9.15 | 1.01 |
| 6 | DeepSeek V3 | 7.75 | 6.35 | 9.55 | 1.08 |
| 7 | MiMo-V2-Flash | 7.47 | 5.20 | 9.80 | 1.37 |
| 8 | MiniMax M2.5 | 7.42 | 4.20 | 9.60 | 1.81 |
| 9 | Gemini 3.1 Pro | 3.51 | 0.45 | 9.80 | 3.95 |
| None | GPT-OSS-120B | 8.51 | 4.80 | 9.80 | 1.86 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.36 |
| 2 | MiniMax M2.5 | 6.61 |
| 3 | Grok 4.20 | 6.95 |
| 4 | Claude Opus 4.6 | 7.60 |
| 5 | Claude Sonnet 4.6 | 7.86 |
| 6 | GPT-OSS-120B | 8.09 |
| 7 | Gemini 3.1 Pro | 8.52 |
| 8 | MiMo-V2-Flash | 8.63 |
| 9 | DeepSeek V3 | 9.23 |
| 10 | Gemini 3 Flash Preview | 9.76 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 77

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

**Generation Time:** 11468ms
**Tokens:** 1240

```
Here is an idiomatic Rust version of your Python code. It uses `chrono` for date/time handling, returns `Result` where mutation can fail, and avoids unnecessary cloning where possible.

### `Cargo.toml`
```toml
[package]
name = "task_manager"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = "0.4"
```

### `src/main.rs`
```rust
use chrono::{DateTime, Local};
use std::error::Error;
use std::fmt;

/// A single task in the task manager.
#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

/// Errors that can occur when operating on the task manager.
#[derive(Debug)]
pub enum TaskManagerError {
    TaskNotFound(u32),
}

impl fmt::Display for TaskManagerError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TaskManagerError::TaskNotFound(id) => write!(f, "task with id {} not found", id),
        }
    }
}

impl Error for TaskManagerError {}

/// Manages a collection of tasks.
#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    /// Creates a new, empty task manager.
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a task and returns a reference to the newly created task.
    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Local>>,
        tags: Vec<String>,
    ) -> &Task {
        let task = Task {
            id: self.next_id,
            title: title.into(),
            completed: false,
            due_date,
            tags,
        };

        self.tasks.push(task);
        self.next_id += 1;

        self.tasks
            .last()
            .expect("task vector must contain the just-inserted task")
    }

    /// Marks a task as completed.
    pub fn complete_task(&mut self, task_id: u...
```

### Claude Opus 4.6

**Generation Time:** 47815ms
**Tokens:** 1668

```


```rust
use chrono::{DateTime, Local};
use std::fmt;

#[derive(Debug, Clone)]
pub struct Task {
    pub id: u64,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Task #{}: {} [{}]",
            self.id,
            self.title,
            if self.completed { "done" } else { "pending" }
        )
    }
}

#[derive(Debug, thiserror::Error)]
pub enum TaskManagerError {
    #[error("task with id {0} not found")]
    TaskNotFound(u64),
}

pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u64,
}

impl TaskManager {
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Local>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task {
            id: self.next_id,
            title: title.into(),
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };
        self.tasks.push(task);
        self.next_id += 1;
        self.tasks.last().expect("just pushed a task")
    }

    pub fn complete_task(&mut self, task_id: u64) -> Result<(), TaskManagerError> {
        let task = self
            .tasks
            .iter_mut()
            .find(|t| t.id == task_id)
            .ok_or(TaskManagerError::TaskNotFound(task_id))?;
        task.completed = true;
        Ok(())
    }

    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Local::now();
        self.tasks
            .iter()
            .filter(|t| {
                !t.completed
                    && t.due_date
                        .map(|due| due < now)
                        .unwrap_or(false)
            })
            .collect()
    }
}

impl Default for Tas...
```

### Gemini 3.1 Pro

**Generation Time:** 25742ms
**Tokens:** 2384

```
` blocks.
    *   `cfg(test)` block with a test or a `main` function showing usage.

8.  **Detailed Review against Prompt Requirements:**
    *   *Idiomatic Rust:* Yes, uses `Vec<&Task>`, `iter_mut()`, `Option`, `Result`, `chrono`.
    *   *Must compile:* Yes, standard safe Rust
```

### Claude Sonnet 4.6

**Generation Time:** 25151ms
**Tokens:** 2077

```
# Idiomatic Rust Task Manager

## Key Design Decisions

- Uses `chrono` for datetime handling (standard Rust datetime crate)
- Returns `Result` types for fallible operations instead of bare booleans
- Uses `Option<T>` for nullable fields
- Implements proper error handling with a custom error type
- Uses `Vec<&Task>` for non-owning views in queries

```toml
# Cargo.toml
[dependencies]
chrono = { version = "0.4", features = ["serde"] }
thiserror = "1.0"
```

```rust
use chrono::{DateTime, Local};
use thiserror::Error;

/// Errors that can occur during task management operations.
#[derive(Debug, Error)]
pub enum TaskError {
    #[error("Task with id {0} not found")]
    NotFound(u32),

    #[error("Task title cannot be empty")]
    EmptyTitle,
}

/// A single task with metadata.
#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

impl Task {
    /// Returns true if the task is overdue (past due date and not completed).
    pub fn is_overdue(&self) -> bool {
        self.due_date
            .map(|due| due < Local::now() && !self.completed)
            .unwrap_or(false)
    }
}

/// Manages a collection of tasks.
#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task and returns a reference to it.
    ///
    /// # Errors
    /// Returns [`TaskError::EmptyTitle`] if the title is blank.
    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Local>>,
        tags: Vec<String>,
    ) -> Result<&Task, TaskError> {
        let title = title.into();

        if title.trim().is_empty() {
            return Err(TaskError::EmptyTitle);
        }

        let task = Task {
            id: self.next_id,
       ...
```

### Grok 4.20

**Generation Time:** 3769ms
**Tokens:** 1126

```
**Here's the idiomatic Rust equivalent:**

```rust
use chrono::{DateTime, Utc};
use std::error::Error;

#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
}

#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> Task {
        let task = Task {
            id: self.next_id,
            title: title.into(),
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };

        self.tasks.push(task.clone());
        self.next_id += 1;

        task
    }

    pub fn complete_task(&mut self, task_id: u32) -> bool {
        for task in &mut self.tasks {
            if task.id == task_id {
                task.completed = true;
                return true;
            }
        }
        false
    }

    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|t| {
                t.due_date.is_some_and(|due| due < now) && !t.completed
            })
            .collect()
    }

    // Additional idiomatic methods
    pub fn get_task(&self, id: u32) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }

    pub fn get_all_tasks(&self) -> &[Task] {
        &self.tasks
    }

    pub fn remove_task(&mut self, id: u32) -> bool {
        if let Some(pos) = self.tasks.iter().position(|t| t.id == id) {
            self.tasks.remove(pos);
            true
        } else {
            false
        }
    }
}

impl Task {
    pub fn is_overdue(&self) -> bool {
        self.due_date.is_some_and(|d...
```

### DeepSeek V3

**Generation Time:** 27298ms
**Tokens:** 1253

```
Here's the idiomatic Rust version of your Python code. I've made several Rust-specific design choices to ensure it's safe, efficient, and follows best practices:

```rust
use chrono::{DateTime, Local, Utc};
use std::cmp::Ordering;

#[derive(Debug, Clone)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
    due_date: Option<DateTime<Utc>>,
    tags: Vec<String>,
}

struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    pub fn new() -> Self {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    pub fn add_task(
        &mut self,
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> Task {
        let task = Task {
            id: self.next_id,
            title,
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };

        self.tasks.push(task.clone());
        self.next_id += 1;
        task
    }

    pub fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            true
        } else {
            false
        }
    }

    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Local::now();
        self.tasks
            .iter()
            .filter(|t| {
                t.due_date
                    .map(|due_date| due_date < now)
                    .unwrap_or(false) && !t.completed
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn test_task_management() {
        let mut manager = TaskManager::new();
        
        // Test adding a task
        let task = manager.add_task("Test task".to_string(), None, None);
        assert_eq!(task.title, "Test task");
        assert_eq!(task.completed, false);
        assert_eq!(task.id, 1);
        
        // Test com...
```

### GPT-OSS-120B

**Generation Time:** 13996ms
**Tokens:** 2397

```
Below is a **complete, idiomatic Rust implementation** of the Python snippet you posted.  
It compiles, uses the standard Rust error‑handling patterns (`Result`/`Error`), and follows common best‑practice conventions (ownership, borrowing, `Option`, `Vec`, `chrono` for dates, etc.).

---  

## 1. Cargo project layout

```
task_manager/
├─ Cargo.toml
└─ src/
   └─ lib.rs          ← the library containing the core logic
   └─ main.rs         ← tiny demo / test harness
```

### `Cargo.toml`

```toml
[package]
name = "task_manager"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = { version = "0.4", features = ["serde"] }   # date‑time handling
thiserror = "1.0"                                   # ergonomic error types
```

*We use `chrono` for `DateTime<Utc>` (the analogue of Python’s `datetime`) and `thiserror` to create a clean error enum.*

---  

## 2. Core library – `src/lib.rs`

```rust
//! A tiny in‑memory task manager.
//!
//! The public API mirrors the Python version but uses Rust idioms:
//! * `Task` is an immutable data structure (`Clone` + `Debug`)
//! * `TaskManager` owns the collection of tasks and the next auto‑increment id.
//! * Errors are expressed with `Result<T, TaskError>`.
//! * Dates are handled with `chrono::DateTime<Utc>`.
//! * All public functions are documented and unit‑tested.

use chrono::{DateTime, Utc};
use std::collections::HashMap;
use thiserror::Error;

/// A single to‑do item.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    /// Unique identifier assigned by `TaskManager`.
    pub id: u32,
    /// Human‑readable title.
    pub title: String,
    /// Has the task been completed?
    pub completed: bool,
    /// Optional due date (UTC).
    pub due_date: Option<DateTime<Utc>>,
    /// Arbitrary tags for categorisation.
    pub tags: Vec<String>,
}

impl Task {
    /// Helper to create a new `Task`.  Called only by `TaskManager`.
    fn new(id: u32, title: impl Into<String>, due_date: Option<DateTime<Utc>>, tags: Ve...
```

### Gemini 3 Flash Preview

**Generation Time:** 6927ms
**Tokens:** 1290

```
To convert this to idiomatic Rust, we use the `chrono` crate for date/time handling (the standard library does not include a calendar-aware datetime type).

### `Cargo.toml` dependencies
```toml
[dependencies]
chrono = "0.4"
```

### Rust Implementation

```rust
use chrono::{DateTime, Utc};

#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
}

pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task. Using `Into<String>` allows passing both &str and String.
    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task {
            id: self.next_id,
            title: title.into(),
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };

        self.tasks.push(task);
        self.next_id += 1;
        
        // Return a reference to the last inserted element
        self.tasks.last().unwrap()
    }

    /// Marks a task as complete. Returns true if found, false otherwise.
    pub fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            return true;
        }
        false
    }

    /// Returns a list of references to overdue tasks.
    /// In Rust, returning references (Vec<&Task>) is more efficient than cloning.
    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|t| {
                !t.completed 
                && t.due_date.map_or(false, |date| date < now)
            })
            .collect()
...
```

### MiniMax M2.5

**Generation Time:** 68713ms
**Tokens:** 2364

```
# Rust Conversion of Task Manager

Here's the idiomatic Rust implementation:

```rust
use chrono::{DateTime, Utc};
use std::fmt;

// ============================================================================
// Task Struct
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
}

impl Task {
    pub fn new(
        id: u32,
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Vec<String>,
    ) -> Self {
        Task {
            id,
            title,
            completed: false,
            due_date,
            tags,
        }
    }

    /// Check if the task is overdue
    pub fn is_overdue(&self) -> bool {
        match self.due_date {
            Some(due) => due < Utc::now() && !self.completed,
            None => false,
        }
    }
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Task {}: {}", self.id, self.title)?;
        if self.completed {
            write!(f, " [COMPLETED]")?;
        }
        if let Some(due) = self.due_date {
            write!(f, " (due: {})", due.format("%Y-%m-%d %H:%M"))?;
        }
        if !self.tags.is_empty() {
            write!(f, " tags: {:?}", self.tags)?;
        }
        Ok(())
    }
}

// ============================================================================
// TaskManager Struct
// ============================================================================

#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    /// Create a new empty TaskManager
    pub fn new() -> Self {
        Self::default()
    }

    /// Add a new task and return it
    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<Dat...
```

### MiMo-V2-Flash

**Generation Time:** 18481ms
**Tokens:** 1929

```
Here is the idiomatic Rust translation of the provided Python code.

### Key Differences and Design Choices

1.  **Mutability vs. Immutability**:
    *   **Python**: Objects are mutable by default. The `TaskManager` modifies its internal `Task` objects in place (`task.completed = True`).
    *   **Rust**: Rust enforces strict aliasing rules. You generally cannot mutate an object while holding a shared reference to it (like in an iterator). To change a `Task`'s state, we typically need exclusive access (`&mut self`) to the `TaskManager`.
    *   **Solution**: The `complete_task` method takes `&mut self`. It finds the task by ID and toggles the boolean.

2.  **Time Handling (`chrono`)**:
    *   The Python code uses `datetime`. The standard equivalent in Rust is the `chrono` crate.
    *   `NaiveDateTime` is used here. It represents a date/time without a timezone, similar to how the Python script implicitly uses naive local time.

3.  **ID Generation**:
    *   **Python**: Uses a mutable integer on the instance.
    *   **Rust**: We use a `u64` for the ID and increment it. Since `next_id` starts at 1, we use `checked_add(1)` to handle the theoretical case of integer overflow gracefully (panicking is often preferred in Rust for logic errors like ID exhaustion, but `unwrap()` is used here for simplicity in a direct translation).

4.  **Return Types**:
    *   `add_task`: Returns a `Result` because allocating memory (pushing to a vector) can fail (OOM).
    *   `complete_task`: Returns `bool` (like the Python version), but takes `&mut self`.
    *   `get_overdue`: Returns a `Vec<Task>`. Since we need to filter based on the current time (`Utc::now()`), we clone the tasks that match the criteria to return them. This avoids lifetime issues associated with returning references to internal data.

### Dependencies

To run this code, you need to add `chrono` to your `Cargo.toml`:

```toml
[dependencies]
chrono = "0.4"
```

### Rust Implementation

```rust
use chrono::{DateTime,...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*