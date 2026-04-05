# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-082334
**Timestamp:** 2026-04-03T08:23:34.494663
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
| 1 | Claude Opus 4.6 | 8.91 | 5.55 | 9.80 | 1.30 |
| 2 | GPT-5.4 | 8.89 | 8.30 | 9.80 | 0.43 |
| 3 | Grok 4.20 | 8.59 | 6.80 | 9.80 | 0.90 |
| 4 | GPT-OSS-120B | 8.54 | 5.40 | 9.80 | 1.35 |
| 5 | Gemini 3 Flash Preview | 8.46 | 7.80 | 9.05 | 0.53 |
| 6 | Claude Sonnet 4.6 | 8.36 | 5.35 | 9.80 | 1.49 |
| 7 | MiMo-V2-Flash | 8.28 | 6.30 | 9.60 | 1.06 |
| 8 | DeepSeek V3 | 8.01 | 5.55 | 9.80 | 1.16 |
| 9 | Gemini 3.1 Pro | 3.18 | 1.65 | 7.60 | 1.97 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.69 |
| 2 | Claude Opus 4.6 | 7.16 |
| 3 | MiniMax M2.5 | 7.45 |
| 4 | Grok 4.20 | 7.81 |
| 5 | GPT-OSS-120B | 7.91 |
| 6 | Claude Sonnet 4.6 | 7.99 |
| 7 | Gemini 3.1 Pro | 8.03 |
| 8 | MiMo-V2-Flash | 8.34 |
| 9 | Gemini 3 Flash Preview | 8.88 |
| 10 | DeepSeek V3 | 9.22 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 84

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

**Generation Time:** 11434ms
**Tokens:** 1159

```
Here is an idiomatic Rust version that compiles, uses proper error handling, and follows common Rust conventions.

```rust
use chrono::{DateTime, Local};
use std::error::Error;
use std::fmt;

#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

#[derive(Debug)]
pub enum TaskError {
    TaskNotFound(u32),
    EmptyTitle,
}

impl fmt::Display for TaskError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TaskError::TaskNotFound(id) => write!(f, "task with id {} not found", id),
            TaskError::EmptyTitle => write!(f, "task title cannot be empty"),
        }
    }
}

impl Error for TaskError {}

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
    ) -> Result<&Task, TaskError> {
        let title = title.into();

        if title.trim().is_empty() {
            return Err(TaskError::EmptyTitle);
        }

        let task = Task {
            id: self.next_id,
            title,
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };

        self.tasks.push(task);
        self.next_id += 1;

        Ok(self.tasks.last().expect("task was just pushed"))
    }

    pub fn complete_task(&mut self, task_id: u32) -> Result<(), TaskError> {
        let task = self
            .tasks
            .iter_mut()
            .find(|task| task.id == task_id)
            .ok_or(TaskError::TaskNotFound(task_id))?;

        task.completed = true;
        Ok(())
    }

    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = ...
```

### Claude Opus 4.6

**Generation Time:** 69571ms
**Tokens:** 1663

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

**Generation Time:** 18819ms
**Tokens:** 2384

```
Here is the idiomatic Rust equivalent of your Python code. 

To handle dates and times in Rust, the standard practice is to use the `chrono` crate. I have also introduced a custom `TaskError` to handle the failure case in `complete_task` idiomatically, rather than just returning a boolean.

### `Cargo.toml`
You will need to add the `chrono`
```

### Claude Sonnet 4.6

**Generation Time:** 23538ms
**Tokens:** 2399

```
# Idiomatic Rust Task Manager

## Key Design Decisions

- Uses `chrono` for datetime handling (standard ecosystem choice)
- Returns `Result` types for fallible operations instead of bare booleans
- Uses `Option` for optional fields, matching Python's `Optional`
- Borrows data where possible to avoid unnecessary cloning
- Separates error types clearly

## `Cargo.toml`

```toml
[package]
name = "task_manager"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = { version = "0.4", features = ["serde"] }
thiserror = "1.0"
```

## `src/main.rs`

```rust
use chrono::{DateTime, Local};
use std::fmt;
use thiserror::Error;

// ── Error Types ──────────────────────────────────────────────────────────────

#[derive(Debug, Error)]
pub enum TaskError {
    #[error("Task with id {0} not found")]
    NotFound(u32),

    #[error("Task with id {0} is already completed")]
    AlreadyCompleted(u32),

    #[error("Title cannot be empty")]
    EmptyTitle,
}

// ── Domain Types ─────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

impl Task {
    /// Returns true if the task is past its due date and not yet completed.
    pub fn is_overdue(&self) -> bool {
        self.due_date
            .map(|due| !self.completed && due < Local::now())
            .unwrap_or(false)
    }
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let status = if self.completed { "✓" } else { "○" };
        let due = self
            .due_date
            .map(|d| d.format("%Y-%m-%d %H:%M").to_string())
            .unwrap_or_else(|| "no due date".to_string());

        write!(
            f,
            "[{}] #{} \"{}\" (due: {}, tags: [{}])",
            status,
            self.id,
            self.title,
            due,
            self.tags.join(", ")...
```

### Grok 4.20

**Generation Time:** 3337ms
**Tokens:** 1244

```
**Here's the idiomatic Rust equivalent:**

```rust
use chrono::{DateTime, Utc};
use std::fmt;

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

impl Task {
    pub fn new(id: u32, title: String, due_date: Option<DateTime<Utc>>, tags: Vec<String>) -> Self {
        Self {
            id,
            title,
            completed: false,
            due_date,
            tags,
        }
    }
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
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> Task {
        let task = Task::new(
            self.next_id,
            title,
            due_date,
            tags.unwrap_or_default(),
        );

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
                t.due_date
                    .map_or(false, |due| due < now && !t.completed)
            })
            .collect()
    }

    // Bonus: more idiomatic methods
    pub fn get_task(&self, id: u32) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }

    pub fn tasks(&self) -> &[Task] {
        &self.tasks
    }
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let status = if self...
```

### DeepSeek V3

**Generation Time:** 25578ms
**Tokens:** 1247

```
Here's the idiomatic Rust version of your Python code:

```rust
use chrono::{DateTime, Utc};
use std::collections::HashSet;

#[derive(Debug, Clone)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
    due_date: Option<DateTime<Utc>>,
    tags: HashSet<String>,
}

#[derive(Debug)]
struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    fn new() -> Self {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    fn add_task(
        &mut self,
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task {
            id: self.next_id,
            title,
            completed: false,
            due_date,
            tags: tags.map(|t| t.into_iter().collect()).unwrap_or_default(),
        };
        self.tasks.push(task);
        self.next_id += 1;
        // Safe to unwrap because we just pushed an item
        self.tasks.last().unwrap()
    }

    fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            true
        } else {
            false
        }
    }

    fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|t| {
                t.due_date
                    .map(|due| due < now && !t.completed)
                    .unwrap_or(false)
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{TimeZone, Utc};

    #[test]
    fn test_task_management() {
        let mut manager = TaskManager::new();
        
        // Test adding a task
        let task = manager.add_task(
            "Learn Rust".to_string(),
            Some(Utc.with_ymd_and_hms(2023, 1, 1, 0, 0, 0).unwrap()),
            Some(vec!["programming".to_string(), "rust".to_string()]),
        )...
```

### GPT-OSS-120B

**Generation Time:** 224312ms
**Tokens:** 2392

```
Below is a **complete, idiomatic Rust translation** of the Python snippet.  
It compiles with the stable 2021 edition, uses the popular **`chrono`** crate for date‑time handling and **`thiserror`** for ergonomic error types, and follows Rust best‑practice guidelines such as:

* explicit ownership/borrowing,
* `Result`‑based error handling,
* `#[derive]` for common traits,
* documentation comments,
* `Option` and `Vec` for optional and list fields,
* private fields with public accessor methods when appropriate.

---

## 1. `Cargo.toml`

```toml
[package]
name = "task_manager"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = { version = "0.4", features = ["serde"] }
thiserror = "1.0"
```

*`chrono`* provides `DateTime<Utc>` (the Rust analogue of Python’s `datetime`).  
*`thiserror`* makes defining error types concise.

---

## 2. `src/lib.rs`

```rust
//! A tiny in‑memory task manager.
//!
//! The API mirrors the behaviour of the original Python implementation
//! while embracing Rust’s safety and ergonomics.

use chrono::{DateTime, Utc};
use thiserror::Error;

/// A single to‑do item.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    /// Unique identifier (assigned by `TaskManager`).
    id: u32,
    /// Human‑readable title.
    title: String,
    /// Has the task been completed?
    completed: bool,
    /// Optional deadline.
    due_date: Option<DateTime<Utc>>,
    /// Arbitrary tags.
    tags: Vec<String>,
}

impl Task {
    /// Create a new `Task`. This is used internally by `TaskManager`.
    fn new(
        id: u32,
        title: impl Into<String>,
        due_date: Option<DateTime<Utc>>,
        tags: Vec<String>,
    ) -> Self {
        Self {
            id,
            title: title.into(),
            completed: false,
            due_date,
            tags,
        }
    }

    // -----------------------------------------------------------------
    // Public getters – the fields are kept private to keep the invariant
    // that `c...
```

### Gemini 3 Flash Preview

**Generation Time:** 8212ms
**Tokens:** 1318

```
To convert this to Rust idiomatically, we use the `chrono` crate for date/time handling (which is the industry standard in Rust). We also use `Option` for nullable fields and `Vec` for lists.

### `Cargo.toml` dependencies
```toml
[dependencies]
chrono = "0.4"
```

### Rust Implementation

```rust
use chrono::{DateTime, Local};

#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
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

    pub fn add_task(
        &mut self,
        title: String,
        due_date: Option<DateTime<Local>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task {
            id: self.next_id,
            title,
            completed: false,
            due_date,
            tags: tags.unwrap_or_default(),
        };

        self.tasks.push(task);
        self.next_id += 1;
        
        // Return a reference to the last inserted element
        self.tasks.last().unwrap()
    }

    pub fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            return true;
        }
        false
    }

    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Local::now();
        self.tasks
            .iter()
            .filter(|t| {
                !t.completed && t.due_date.map_or(false, |date| date < now)
            })
            .collect()
    }
}

fn main() {
    let mut manager = TaskManager::new();

    manager.add_task(
        "Finish Rust project".to_string(),
        Some(Local::now()), 
        Some(vec!["rust".to_string(), "coding".to_string()])
    );

    let success = manager.complete_task(1);
    println!("Task 1 c...
```

### MiniMax M2.5

**Generation Time:** 0ms
**Tokens:** 0

```

```

### MiMo-V2-Flash

**Generation Time:** 19082ms
**Tokens:** 2083

```
Here is the idiomatic Rust translation.

### Key Differences & Design Decisions

1.  **State Management (Ownership)**:
    *   **Python**: Uses mutable references (`self.tasks`) to modify objects in place.
    *   **Rust**: `Task` is defined as `pub` and `Clone`. The `TaskManager` owns the tasks. Methods that "modify" a task (like `complete_task`) actually find the task, clone it, update the clone, and replace the old one in the vector. This avoids complex mutable borrowing issues and keeps the API clean.
2.  **Time Handling**:
    *   **Python**: Uses the standard library `datetime`.
    *   **Rust**: Uses the `chrono` crate, the industry standard for date/time handling. It handles timezones and naive datetimes robustly.
3.  **Nullability**:
    *   **Python**: Uses `Optional[datetime]`.
    *   **Rust**: Uses `Option<DateTime<Utc>>`.
4.  **Error Handling**:
    *   **Python**: Returns `False` on failure.
    *   **Rust**: Returns `Result<(), Error>`. This allows the caller to handle the "Task not found" case explicitly using the `?` operator or pattern matching.

### Dependencies
Add this to your `Cargo.toml` to handle dates:
```toml
[dependencies]
chrono = { version = "0.4", features = ["serde"] }
serde = { version = "1.0", features = ["derive"] } # Optional, but good practice for structs
```

### Rust Code

```rust
use chrono::{DateTime, Utc};
use std::error::Error;
use std::fmt;

// 1. Define the Task Struct
// We derive Clone because we will replace tasks in the vector rather than mutating them in place.
// We derive Debug to allow printing/inspecting the struct.
#[derive(Debug, Clone, PartialEq)]
pub struct Task {
    pub id: u64,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
}

// 2. Define a custom Error type for better error handling
#[derive(Debug, PartialEq)]
pub enum TaskError {
    NotFound(u64),
}

impl fmt::Display for TaskError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fm...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*