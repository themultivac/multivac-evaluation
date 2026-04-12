# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-141157
**Timestamp:** 2026-02-07T14:11:57.324352
**Category:** Programming & Code
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
| 1 | Claude Opus 4.5 | 9.65 | 8.80 | 10.00 | 0.37 |
| 2 | Grok 3 (Direct) | 9.50 | 8.15 | 10.00 | 0.61 |
| 3 | Grok Code Fast 1 | 9.44 | 8.80 | 10.00 | 0.41 |
| 4 | Claude Sonnet 4.5 | 9.33 | 8.55 | 9.80 | 0.41 |
| 5 | GPT-5.2-Codex | 8.86 | 6.55 | 9.80 | 1.12 |
| 6 | Gemini 3 Flash Preview | 8.84 | 7.75 | 9.35 | 0.53 |
| 7 | DeepSeek V3.2 | 8.71 | 5.85 | 9.80 | 1.35 |
| 8 | MiniMax M2.1 | 8.68 | 7.45 | 9.80 | 0.87 |
| 9 | GLM 4.7 | 5.70 | 2.00 | 8.60 | 3.37 |
| 10 | Gemini 3 Pro Preview | 1.32 | 0.40 | 2.25 | 0.66 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.2-Codex | 7.23 |
| 2 | MiniMax M2.1 | 7.68 |
| 3 | Grok Code Fast 1 | 7.91 |
| 4 | Claude Opus 4.5 | 7.97 |
| 5 | Grok 3 (Direct) | 8.07 |
| 6 | Claude Sonnet 4.5 | 8.14 |
| 7 | DeepSeek V3.2 | 8.15 |
| 8 | GLM 4.7 | 8.54 |
| 9 | Gemini 3 Flash Preview | 8.86 |

**Strictest Judge:** gpt_codex
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 76

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

**Generation Time:** 9697ms
**Tokens:** 2720

```
```rust
use chrono::{DateTime, Utc};
use std::fmt;

/// A simple error type for task management operations.
#[derive(Debug)]
pub struct TaskError {
    message: String,
}

impl TaskError {
    fn new(message: &str) -> Self {
        TaskError {
            message: message.to_string(),
        }
    }
}

impl fmt::Display for TaskError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message)
    }
}

impl std::error::Error for TaskError {}

/// Represents a task with an ID, title, completion status, optional due date, and tags.
#[derive(Debug, Clone)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
}

/// Manages a collection of tasks, allowing addition, completion, and retrieval of overdue tasks.
#[derive(Debug)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    /// Creates a new TaskManager with an empty task list and ID starting at 1.
    pub fn new() -> Self {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task with the given title, optional due date, and tags.
    /// Returns the created Task or an error if the title is empty.
    pub fn add_task(
        &mut self,
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Vec<String>,
    ) -> Result<Task, TaskError> {
        if title.trim().is_empty() {
            return Err(TaskError::new("Task title cannot be empty"));
        }
        let task = Task {
            id: self.next_id,
            title,
            completed: false,
            due_date,
            tags,
        };
        self.tasks.push(task.clone());
        self.next_id += 1;
        Ok(task)
    }

    /// Marks the task with the given ID as completed.
    /// Returns true if the task was found and updated, false otherwise.
    pub fn complete_task(&mut self, tas...
```

### Claude Opus 4.5

**Generation Time:** 18859ms
**Tokens:** 2168

```
# Rust Implementation of TaskManager

Here's the idiomatic Rust conversion with proper error handling and best practices:

```rust
use chrono::{DateTime, Local};
use thiserror::Error;

/// Errors that can occur in TaskManager operations
#[derive(Error, Debug)]
pub enum TaskError {
    #[error("Task with id {0} not found")]
    TaskNotFound(u64),
}

/// Represents a task with associated metadata
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub id: u64,
    pub title: String,
    pub completed: bool,
    pub due_date: Option<DateTime<Local>>,
    pub tags: Vec<String>,
}

impl Task {
    /// Creates a new task with the given parameters
    fn new(
        id: u64,
        title: String,
        due_date: Option<DateTime<Local>>,
        tags: Vec<String>,
    ) -> Self {
        Self {
            id,
            title,
            completed: false,
            due_date,
            tags,
        }
    }
}

/// Manages a collection of tasks
#[derive(Debug, Default)]
pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u64,
}

impl TaskManager {
    /// Creates a new empty TaskManager
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task and returns a reference to it
    ///
    /// # Arguments
    /// * `title` - The title of the task
    /// * `due_date` - Optional due date for the task
    /// * `tags` - Optional tags associated with the task
    ///
    /// # Returns
    /// A reference to the newly created task
    pub fn add_task(
        &mut self,
        title: impl Into<String>,
        due_date: Option<DateTime<Local>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task::new(
            self.next_id,
            title.into(),
            due_date,
            tags.unwrap_or_default(),
        );
        self.tasks.push(task);
        self.next_id += 1;
        
        // Safe: we just pushed an element
        self.tasks.last(...
```

### Gemini 3 Flash Preview

**Generation Time:** 6644ms
**Tokens:** 1349

```
To convert this to idiomatic Rust, we use the `chrono` crate (the standard for date/time in Rust) and leverage Rust's ownership and error-handling patterns.

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
    /// Creates a new, empty TaskManager.
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task. 
    /// Takes ownership of title and tags (idiomatic for builders/constructors).
    pub fn add_task(
        &mut self, 
        title: String, 
        due_date: Option<DateTime<Utc>>, 
        tags: Option<Vec<String>>
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

    /// Marks a task as completed. 
    /// Returns true if the task was found and updated, false otherwise.
    pub fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            return true;
        }
        false
    }

    /// Returns a list of references to overdue, incomplete tasks.
    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|t| {
                !t.completed && t.due_date.map_or(false, |date| date < now)
            })
            .collect()
 ...
```

### Claude Sonnet 4.5

**Generation Time:** 16607ms
**Tokens:** 1648

```
```rust
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, PartialEq)]
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
    /// Creates a new TaskManager
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task and returns a reference to it
    pub fn add_task(
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
            tags: tags.unwrap_or_default(),
        };
        
        self.tasks.push(task);
        self.next_id += 1;
        
        // Safe to unwrap because we just pushed
        self.tasks.last().unwrap()
    }

    /// Marks a task as completed. Returns true if the task was found, false otherwise
    pub fn complete_task(&mut self, task_id: u32) -> bool {
        self.tasks
            .iter_mut()
            .find(|task| task.id == task_id)
            .map(|task| {
                task.completed = true;
            })
            .is_some()
    }

    /// Returns a vector of references to overdue, incomplete tasks
    pub fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|task| {
                if let Some(due_date) = task.due_date {
                    due_date < now && !task.completed
                } else {
                    false
                }
            })
            .collect()
    }

    /// Returns a reference to all tasks
    pub fn get_tasks(&self) -> &[Task] {
        &self.tasks
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Du...
```

### Gemini 3 Pro Preview

**Generation Time:** 20929ms
**Tokens:** 2385

```
Here is the idiomatic Rust equivalent of the Python code.

### Key Changes and Idioms
1.  **Dependencies**: We use the `chrono` crate, which is the standard for date and time in Rust.
2.  **Structs**: The `dataclass` becomes a `struct`. We derive traits like `Debug` and `Clone` for usability.
3.  
```

### MiniMax M2.1

**Generation Time:** 26599ms
**Tokens:** 1735

```
```rust
use chrono::{DateTime, Local, NaiveDateTime};
use std::fmt;

// Define Task struct
#[derive(Debug, Clone)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
    due_date: Option<NaiveDateTime>,
    tags: Vec<String>,
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Task {}: {} (completed: {}, due: {:?}, tags: {:?})",
            self.id, self.title, self.completed, self.due_date, self.tags
        )
    }
}

// Define TaskManager struct
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
        due_date: Option<NaiveDateTime>,
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

    fn complete_task(&mut self, task_id: u32) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == task_id) {
            task.completed = true;
            true
        } else {
            false
        }
    }

    fn get_overdue(&self) -> Vec<&Task> {
        let now = Local::now().naive_local();
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

fn main() {
    // Example usage
    let mut manager = TaskManager::new();
    
    let task1 = manager.add_task(
        "Learn Rust".to_string(),
        Some(Local::now().naive_local() - chrono::Duration::days(1)),
        Some(vec!["programming".to_string(), "...
```

### GLM 4.7

**Generation Time:** 135536ms
**Tokens:** 2330

```

```

### DeepSeek V3.2

**Generation Time:** 47311ms
**Tokens:** 1859

```
Here's an idiomatic Rust implementation of your Python code:

```rust
use chrono::{DateTime, Local, Utc};
use std::collections::HashMap;

#[derive(Debug, Clone)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
    due_date: Option<DateTime<Utc>>,
    tags: Vec<String>,
}

impl Task {
    fn new(id: u32, title: String, due_date: Option<DateTime<Utc>>, tags: Vec<String>) -> Self {
        Self {
            id,
            title,
            completed: false,
            due_date,
            tags,
        }
    }
}

#[derive(Debug)]
struct TaskManager {
    tasks: HashMap<u32, Task>,
    next_id: u32,
}

impl TaskManager {
    fn new() -> Self {
        Self {
            tasks: HashMap::new(),
            next_id: 1,
        }
    }

    fn add_task(
        &mut self,
        title: String,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task::new(self.next_id, title, due_date, tags.unwrap_or_default());
        self.tasks.insert(self.next_id, task);
        self.next_id += 1;
        self.tasks.get(&(self.next_id - 1)).unwrap()
    }

    fn complete_task(&mut self, task_id: u32) -> Result<(), String> {
        match self.tasks.get_mut(&task_id) {
            Some(task) => {
                task.completed = true;
                Ok(())
            }
            None => Err(format!("Task with id {} not found", task_id)),
        }
    }

    fn get_overdue(&self) -> Vec<&Task> {
        let now = Utc::now();
        self.tasks
            .values()
            .filter(|task| {
                task.due_date
                    .map(|due_date| due_date < now && !task.completed)
                    .unwrap_or(false)
            })
            .collect()
    }

    fn get_task(&self, task_id: u32) -> Option<&Task> {
        self.tasks.get(&task_id)
    }

    fn get_all_tasks(&self) -> Vec<&Task> {
        self.tasks.values().collect()
    }
}

fn main() -> Result<(), Box<dyn std::error:...
```

### GPT-5.2-Codex

**Generation Time:** 19995ms
**Tokens:** 1422

```
Below is an idiomatic Rust version of your Python code. It uses the `chrono` crate for date handling, `Option` for nullable fields, and follows Rust’s ownership and error‑handling conventions. The code compiles and is ready to use.

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
        self.next_id += 1;
        self.tasks.push(task.clone());
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

    pub fn get_overdue(&self) -> Vec<Task> {
        let now = Utc::now();
        self.tasks
            .iter()
            .filter(|t| {
                !t.completed
                    && t.due_date
                        .as_ref()
                        .map(|d| d < &now)
                        .unwrap_or(false)
            })
            .cloned()
            .collect()
    }
}
```

### Notes
- Uses `chrono::Utc` for timestamps (`DateTime<Utc>`).
- `Option<Vec<String>>` for tags allows defaulting to empty vector.
- `get_overdue` returns owned `Task` values (cloned) for convenience and safety.
- `complete_task` returns...
```

### Grok 3 (Direct)

**Generation Time:** 21326ms
**Tokens:** 1833

```
Here's the Rust equivalent of your Python code, following idiomatic Rust practices, proper error handling, and using the `chrono` crate for date/time handling. I've included comments to explain key decisions and added necessary dependencies in a `Cargo.toml` snippet.

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
use chrono::{DateTime, Utc};
use std::vec::Vec;

// Equivalent to Python's @dataclass for Task
#[derive(Debug, Clone)]
pub struct Task {
    id: u32, // Using u32 instead of i32 since IDs are typically positive
    title: String,
    completed: bool,
    due_date: Option<DateTime<Utc>>, // Using chrono::DateTime for datetime handling
    tags: Vec<String>,
}

impl Task {
    pub fn new(id: u32, title: String, due_date: Option<DateTime<Utc>>, tags: Vec<String>) -> Self {
        Task {
            id,
            title,
            completed: false,
            due_date,
            tags,
        }
    }
}

pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    /// Creates a new TaskManager instance.
    pub fn new() -> Self {
        TaskManager {
            tasks: Vec::new(),
            next_id: 1,
        }
    }

    /// Adds a new task with the given title, optional due date, and optional tags.
    /// Returns a reference to the newly created Task.
    pub fn add_task(
        &mut self,
        title: &str,
        due_date: Option<DateTime<Utc>>,
        tags: Option<Vec<String>>,
    ) -> &Task {
        let task = Task::new(
            self.next_id,
            title.to_string(),
            due_date,
            tags.unwrap_or_default(), // Equivalent to Python's `tags or []`
        );
        self.tasks.push(task);
        self.next_id += 1;
        // Return a reference to the last added task
        self.tasks.last().unwrap()
    }

    /// Marks a task as completed by its ID.
    /// Returns true if...
```

---

*Generated by The Multivac V5*
*https://multivac.com*