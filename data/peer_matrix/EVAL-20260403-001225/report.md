# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-001225
**Timestamp:** 2026-04-03T00:12:25.866312
**Category:** Communication & Writing
**Model Pool:** 10 communication-optimized models

## Question

Explain recursion by starting with the solution and working backwards to the concept. Begin with a working recursive function, show what it does step by step, then explain why this approach exists and when to use it (and when NOT to). The reader should understand recursion by the end without ever seeing a formal definition until the last paragraph.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Sonnet 4.6 | 9.41 | 8.65 | 10.00 | 0.53 |
| 2 | GPT-5.4 | 9.13 | 8.40 | 10.00 | 0.44 |
| 3 | MiMo-V2-Flash | 9.07 | 8.65 | 9.80 | 0.43 |
| 4 | Mistral Small Creative | 9.06 | 8.35 | 9.60 | 0.43 |
| 5 | Grok 4.20 | 9.04 | 8.60 | 9.80 | 0.48 |
| 6 | Claude Opus 4.6 | 8.78 | 6.85 | 9.80 | 0.89 |
| 7 | GPT-OSS-120B | 8.62 | 7.00 | 9.80 | 0.86 |
| 8 | Seed 1.6 Flash | 8.56 | 6.80 | 9.65 | 0.85 |
| 9 | DeepSeek V3 | 8.52 | 7.30 | 9.60 | 0.82 |
| 10 | Gemini 3.1 Pro | 7.43 | 4.75 | 9.45 | 1.36 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.78 |
| 2 | Claude Opus 4.6 | 8.37 |
| 3 | GPT-OSS-120B | 8.51 |
| 4 | Seed 1.6 Flash | 8.58 |
| 5 | Claude Sonnet 4.6 | 8.64 |
| 6 | Gemini 3.1 Pro | 8.82 |
| 7 | Grok 4.20 | 8.83 |
| 8 | MiMo-V2-Flash | 8.93 |
| 9 | DeepSeek V3 | 9.27 |
| 10 | Mistral Small Creative | 9.77 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** mistral_small_creative
**Total Judgments:** 100
**Valid Judgments:** 89

---

## Model Pool

Models selected for **Communication & Writing** evaluation:

1. **Claude Opus 4.6** (openrouter)
2. **GPT-5.4** (openrouter)
3. **Claude Sonnet 4.6** (openrouter)
4. **Gemini 3.1 Pro** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **MiMo-V2-Flash** (openrouter)
9. **Mistral Small Creative** (openrouter)
10. **Seed 1.6 Flash** (openrouter)

---

## Model Responses

### Claude Opus 4.6

**Generation Time:** 40042ms
**Tokens:** 2123

```
# Recursion: From Code to Concept

## Here's the Solution

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

That's it. That's the whole thing. Let's run it and watch what happens.

---

## What Does It Actually Do?

Let's call `factorial(5)` and trace every single step.

```
factorial(5)
│
│  Is 5 == 0?  No.
│  So return 5 * factorial(4)
│                │
│                │  Is 4 == 0?  No.
│                │  So return 4 * factorial(3)
│                │                │
│                │                │  Is 3 == 0?  No.
│                │                │  So return 3 * factorial(2)
│                │                │                │
│                │                │                │  Is 2 == 0?  No.
│                │                │                │  So return 2 * factorial(1)
│                │                │                │                │
│                │                │                │                │  Is 1 == 0?  No.
│                │                │                │                │  So return 1 * factorial(0)
│                │                │                │                │                │
│                │                │                │                │                │  Is 0 == 0?  YES.
│                │                │                │                │                │  Return 1.
│                │                │                │                │                │
│                │                │                │                │  Return 1 * 1 = 1
│                │                │                │                │
│                │                │                │  Return 2 * 1 = 2
│                │                │                │
│                │                │  Return 3 * 2 = 6
│                │                │
│                │  Return 4 * 6 = 24
│                │
│  Return 5 * 24 = 120

Result: 120
```

The function called **itself** five times. Each cal...
```

### GPT-5.4

**Generation Time:** 39412ms
**Tokens:** 2119

```
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

Let’s start here, with something that already works.

If you call:

```python
factorial(4)
```

you get:

```python
24
```

Why?

Let’s watch it happen.

---

### Step 1: What the function does

`factorial(4)` means:

```python
4 * 3 * 2 * 1
```

So the answer is:

```python
24
```

But this function doesn’t multiply all those numbers in one loop. Instead, it keeps turning the problem into a smaller version of itself.

Here’s the function again:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

Now let’s expand:

```python
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * (3 * (2 * (1 * factorial(0))))
= 4 * (3 * (2 * (1 * 1)))
= 4 * (3 * (2 * 1))
= 4 * (3 * 2)
= 4 * 6
= 24
```

So the function keeps saying:

- “I know how to solve this if I can solve a smaller version first.”
- “Eventually I’ll reach the smallest possible case.”
- “Then I’ll build the answer back up.”

That’s the whole trick.

---

### Step 2: The two parts that make it work

This function works because it has exactly two important pieces.

#### 1. A stopping point

```python
if n == 0:
    return 1
```

This is the point where the function does **not** keep going smaller.

Without this, it would keep calling itself forever:

```python
factorial(4)
factorial(3)
factorial(2)
factorial(1)
factorial(0)
factorial(-1)
factorial(-2)
...
```

So every working version of this pattern needs a clear “stop here” case.

#### 2. A smaller step

```python
return n * factorial(n - 1)
```

This line takes the current problem and turns it into a simpler one:

- `factorial(4)` becomes `4 * factorial(3)`
- `factorial(3)` becomes `3 * factorial(2)`

Each step moves closer to the stopping point.

So the shape is:

- solve the smallest case directly
- reduce bigger cases to smaller ones

---

### Step 3: Another example that feels mor...
```

### Claude Sonnet 4.6

**Generation Time:** 40067ms
**Tokens:** 1996

```
# Recursion: Starting With What It Does

---

## Here's the function. Just read it.

```python
def countdown(n):
    if n == 0:
        print("Go!")
        return
    print(n)
    countdown(n - 1)

countdown(3)
```

**Output:**
```
3
2
1
Go!
```

Don't analyze it yet. Just run it in your head. It prints 3, then 2, then 1, then "Go!". It works. Now let's figure out *why*.

---

## What actually happens when you run this

The computer doesn't see a clever abstraction. It does something embarrassingly literal:

```
countdown(3) runs:
  → prints 3
  → calls countdown(2)
      → prints 2
      → calls countdown(1)
          → prints 1
          → calls countdown(0)
              → prints "Go!"
              → returns
          ← back in countdown(1), which also returns
      ← back in countdown(2), which also returns
  ← back in countdown(3), which also returns
```

The function calls *itself*. Each call pauses, waits for the inner call to finish, then resumes. It's a stack of half-finished work, growing deeper until it hits the base case (`n == 0`), then unwinding back out.

That word — **base case** — is the thing that stops it from running forever. Every recursive function needs one. It's the moment the function says "I'm done, no more calling myself."

---

## A slightly more interesting example: factorial

```python
def factorial(n):
    if n == 0:        # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(4))  # 24
```

Watch what this actually computes:

```
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * (3 * (2 * (1 * factorial(0))))
= 4 * (3 * (2 * (1 * 1)))
= 4 * (3 * (2 * 1))
= 4 * (3 * 2)
= 4 * 6
= 24
```

Notice the shape of this. The problem **expands outward** until it hits something it knows (factorial of 0 is 1), then **collapses inward** doing the actual multiplication on the way back up.

The function never explicitly loops. It never says "do this 4 times." It ...
```

### Gemini 3.1 Pro

**Generation Time:** 33553ms
**Tokens:** 2110

```
Here is a working Python function. If we pass the number `3` into this function, it will output `6`. 

```python
def calculate_total(number):
    if number == 1:
        return 1
    else:
        return number + calculate_total(number - 1)
```

Look closely at the last line. Inside the `calculate_total` function, it uses the `calculate_total` function. 

To understand how this is even possible, we need to slow down time and look at exactly what the computer does when we ask it to run `calculate_total(3)`.

**Step 1:** The computer starts running `calculate_total(3)`. 
It checks: is 3 equal to 1? No. 
So, it goes to the `else` block. It is told to return `3 + calculate_total(2)`. 
But the computer has a problem. It knows what `3` is, and it knows what `+` means, but it doesn't know what `calculate_total(2)` is yet. So, it hits the "pause" button on Step 1, keeps the `3 + ` in its memory, and starts a brand new task to figure out `calculate_total(2)`.

**Step 2:** The computer starts running `calculate_total(2)`.
It checks: is 2 equal to 1? No.
It goes to the `else` block. It is told to return `2 + calculate_total(1)`.
Again, it doesn't know the answer to the second part yet. So it hits "pause" on Step 2, keeps the `2 + ` in its memory, and starts a brand new task to figure out `calculate_total(1)`.

**Step 3:** The computer starts running `calculate_total(1)`.
It checks: is 1 equal to 1? Yes! 
Because the condition is met, it simply returns the number `1`. No new tasks are needed. 

**The Rewind:**
Now that the computer finally has a concrete answer, it can unpause its previous tasks.
* It unpauses Step 2. It was waiting to solve `2 + calculate_total(1)`. It now knows the missing piece is `1`. So, `2 + 1 = 3`. It hands the number `3` backward to the previous step.
* It unpauses Step 1. It was waiting to solve `3 + calculate_total(2)`. It now knows the missing piece is `3`. So, `3 + 3 = 6`. 

The final answer is 6. The function worked by breaking a problem down into ...
```

### Grok 4.20

**Generation Time:** 5405ms
**Tokens:** 1056

```
**Let's start with a working recursive function.**

Here's a function that calculates the factorial of a number:

```python
def factorial(n):
    if n == 1:           # base case
        return 1
    else:
        return n * factorial(n-1)   # recursive case
```

Let's run `factorial(5)` and watch exactly what happens, step by step.

---

### Step-by-step execution of `factorial(5)`

```
factorial(5)
    → 5 * factorial(4)
          → 4 * factorial(3)
                → 3 * factorial(2)
                      → 2 * factorial(1)
                            → returns 1          ← base case stops the chain
                      ← returns 2 * 1 = 2
                ← returns 3 * 2 = 6
          ← returns 4 * 6 = 24
    ← returns 5 * 24 = 120
```

The function keeps calling *itself* with a smaller number until it hits `1`. Then it starts returning values back up the chain, multiplying as it goes.

You can literally watch the computer build up a stack of unfinished calls:

- `factorial(5)` is waiting for `factorial(4)`
- `factorial(4)` is waiting for `factorial(3)`
- ...
- `factorial(1)` finally returns 1

Then the answers ripple back up, multiplying at each level.

---

### Now let's look at what the function is actually doing

The mathematical definition of factorial is:

- 5! = 5 × 4 × 3 × 2 × 1
- But notice that 4! = 4 × 3 × 2 × 1
- So 5! = 5 × (4!)

That's exactly what the code is saying:

> "To compute n!, multiply n by the factorial of (n-1)"

And when you get to 1, you already know the answer: 1! = 1. That's the **base case** — the point where you stop asking the question and just return an answer.

---

### Why does this approach exist?

Because some problems have a very natural "self-similar" structure.

The problem of computing *n!* is made up of the *smaller but similar* problem of computing *(n-1)!*. The structure of the problem is the same at every level.

This pattern appears in many places:

- Traversing a file system (a folder contains files *and* other fold...
```

### DeepSeek V3

**Generation Time:** 29805ms
**Tokens:** 756

```
# Understanding Recursion Through a Working Example  

Let's start with a concrete recursive function and see it in action before diving into abstract definitions.  

## A Recursive Function: Calculating Factorials  

Here's a simple recursive function to compute the factorial of a number `n` (written as `n!`):  

```python
def factorial(n):
    if n == 0:  # Base case
        return 1
    else:       # Recursive case
        return n * factorial(n - 1)
```

### What Does It Do? Step-by-Step  

Let's trace `factorial(3)`:  

1. **First call:** `factorial(3)`  
   - `n` is `3`, not `0`, so it returns `3 * factorial(2)`  
   - But now we need to compute `factorial(2)`...  

2. **Second call:** `factorial(2)`  
   - `n` is `2`, not `0`, so it returns `2 * factorial(1)`  
   - Now we need `factorial(1)`...  

3. **Third call:** `factorial(1)`  
   - `n` is `1`, not `0`, so it returns `1 * factorial(0)`  
   - Now we need `factorial(0)`...  

4. **Fourth call:** `factorial(0)`  
   - `n` is `0`, so it **stops recursing** and returns `1` (the base case)  

Now, the function "unwinds" back up:  

- `factorial(1)` = `1 * factorial(0)` = `1 * 1` = `1`  
- `factorial(2)` = `2 * factorial(1)` = `2 * 1` = `2`  
- `factorial(3)` = `3 * factorial(2)` = `3 * 2` = `6`  

So, `factorial(3)` correctly returns **6**.  

### Why Does This Work?  

- **Base Case:** The function stops calling itself when `n == 0`, preventing infinite recursion.  
- **Recursive Case:** The function calls itself with a smaller problem (`n - 1`), breaking the problem down step by step.  

### When to Use Recursion  

Recursion is useful when:  
✅ A problem can be broken into smaller, identical subproblems (e.g., factorial, Fibonacci, tree traversals).  
✅ The solution is naturally expressed in terms of itself (e.g., "the factorial of `n` is `n` times the factorial of `n-1`").  

### When **Not** to Use Recursion  

Avoid recursion when:  
❌ The problem doesn't naturally divide into smaller identical problem...
```

### GPT-OSS-120B

**Generation Time:** 46095ms
**Tokens:** 2167

```
## 1. A “finished” piece of code

Below is a tiny, completely working function that computes the **sum of all the numbers in a list**.

```python
def sum_list(lst):
    # 1️⃣  The “stop” condition
    if not lst:                # empty list → nothing to add
        return 0

    # 2️⃣  Break the problem into a smaller one
    first, *rest = lst         # first = lst[0], rest = lst[1:]

    # 3️⃣  Solve the smaller problem and glue the answer together
    return first + sum_list(rest)
```

Running it looks ordinary:

```python
>>> sum_list([3, 7, 2, 9])
21
```

We have a *working* recursive function. Let’s **un‑wrap** what happens inside it, line by line, call by call, as if we were watching a magician pull the trick apart.

---

## 2. Step‑by‑step execution (the “backwards” view)

### 2.1 The first call

```
sum_list([3, 7, 2, 9])
```

| Step | What the code does | Why it matters |
|------|-------------------|----------------|
| 1️⃣   | `if not lst:` → `False` (the list isn’t empty) | The function *doesn’t* stop yet. |
| 2️⃣   | `first, *rest = lst` → `first = 3`, `rest = [7, 2, 9]` | We separate the *head* (the first element) from the *tail* (the rest). |
| 3️⃣   | `return first + sum_list(rest)` → `return 3 + sum_list([7, 2, 9])` | The answer will be “the first element plus the sum of the rest”. |

At this point the function **calls itself** with a *smaller* list: `[7, 2, 9]`. Nothing is returned yet – we have to wait for that inner call to finish.

---

### 2.2 The second call (still inside the first)

```
sum_list([7, 2, 9])
```

| Step | Action | Result |
|------|--------|--------|
| 1️⃣   | `if not lst:` → `False` | Continue |
| 2️⃣   | `first = 7`, `rest = [2, 9]` | Split again |
| 3️⃣   | `return 7 + sum_list([2, 9])` | We now need the sum of `[2, 9]` |

Again we pause and dive deeper.

---

### 2.3 The third call

```
sum_list([2, 9])
```

| Step | Action | Result |
|------|--------|--------|
| 1️⃣   | `if not lst:` → `False` | Continue |
| 2️⃣   | `first =...
```

### MiMo-V2-Flash

**Generation Time:** 11387ms
**Tokens:** 1384

```
Here is an explanation of recursion that starts with the code and ends with the definition.

### 1. The Solution: The Recursive Function

Let’s look at a working recursive function written in Python. Its job is to calculate the **factorial** of a number (e.g., $5! = 5 \times 4 \times 3 \times 2 \times 1$).

```python
def factorial(n):
    # Step 1: The Base Case (The Stop Sign)
    if n == 1:
        return 1
    
    # Step 2: The Recursive Step (The Action)
    else:
        return n * factorial(n - 1)
```

### 2. Step-by-Step Execution

To understand how this works, we don't look at the code from top to bottom. Instead, we watch it unfold and then fold back up.

Let’s say we call `factorial(3)`.

**The Unfolding (The Call Stack):**
1.  We ask: `factorial(3)`.
2.  The computer checks: Is $n$ equal to 1? No.
3.  The computer pauses `factorial(3)` to ask a new question: `factorial(2)`.
4.  It pauses that to ask: `factorial(1)`.
5.  Now, $n$ **is** equal to 1. The function hits the base case and returns **1**.

**The Folding Back (The Return):**
Now that the innermost function has a value, the pauses begin to resolve in reverse order.

1.  `factorial(1)` returns **1**.
2.  This value goes back to `factorial(2)`. The calculation was: `2 * factorial(1)`. Since it received 1, it calculates $2 \times 1 = \mathbf{2}$.
3.  This value (2) goes back to `factorial(3)`. The calculation was: `3 * factorial(2)`. Since it received 2, it calculates $3 \times 2 = \mathbf{6}$.
4.  The final result **6** is returned to the main program.

### 3. Working Backwards: Why This Approach?

You might ask: "Why write a function that calls itself? Why not just use a loop?"

To understand *why* recursion exists, we have to look at the structure of the problem.

**The Problem of Repetition:**
Calculating a factorial is a repetitive task. You multiply $n$ by the result of the previous number.
*   $5! = 5 \times 4!$
*   $4! = 4 \times 3!$
*   $3! = 3 \times 2!$
*   $2! = 2 \times 1!$
*   $1! = 1$ ...
```

### Mistral Small Creative

**Generation Time:** 20859ms
**Tokens:** 3195

```
### **Understanding Recursion: From Solution to Concept**

Let’s start with a **working recursive function** and reverse-engineer the idea of recursion by breaking it down step by step. By the end, you’ll understand *why* recursion exists, *when* to use it, and—just as importantly—*when to avoid it*.

---

## **1. The Working Example: Factorial Calculation**
Here’s a Python function that computes the **factorial** of a number (e.g., `5! = 5 × 4 × 3 × 2 × 1 = 120`):

```python
def factorial(n):
    if n == 0:  # Base case
        return 1
    else:
        return n * factorial(n - 1)  # Recursive case
```

### **What Does This Function Do?**
Let’s trace `factorial(3)` step by step:

1. **First Call (`factorial(3)`)**
   - `n = 3` (not `0`), so it returns `3 * factorial(2)`.
   - Now, the function *calls itself* with `n = 2`.

2. **Second Call (`factorial(2)`)**
   - `n = 2` (not `0`), so it returns `2 * factorial(1)`.
   - The function *calls itself again* with `n = 1`.

3. **Third Call (`factorial(1)`)**
   - `n = 1` (not `0`), so it returns `1 * factorial(0)`.
   - The function *calls itself once more* with `n = 0`.

4. **Base Case (`factorial(0)`)**
   - `n = 0` (matches the base case), so it returns `1` (without calling itself again).

5. **Unwinding the Calls**
   - Now, the returns "bubble up":
     - `factorial(1)` gets `1 * 1 = 1`.
     - `factorial(2)` gets `2 * 1 = 2`.
     - `factorial(3)` gets `3 * 2 = 6`.
   - **Final result:** `6`.

---
## **2. The Pattern: Breaking Down the Problem**
Notice something crucial:
- The function **solves a smaller version of the same problem** (`factorial(n-1)`) before combining it with the current step (`n * ...`).
- It **stops when it reaches a simple, known answer** (`factorial(0) = 1`).

This is the **core idea of recursion**:
> *"To solve a problem, break it into smaller instances of the same problem until you reach a simple case you know how to solve."*

---

## **3. Why Does This Work?**
Recursion works because:
1. *...
```

### Seed 1.6 Flash

**Generation Time:** 20140ms
**Tokens:** 3177

```
### Let's Start with a Problem: Counting Marbles in Nested Boxes  


Imagine you have a stack of nested boxes. The outermost box (Box A) contains 2 marbles, and inside it is Box B. Box B has 3 marbles and contains Box C. Box C has 4 marbles and contains... nothing but air (no more boxes). You want to find the **total number of marbles** in all boxes.  


### How Would You Solve This?  
Let's think step by step. You can't just count all marbles at once—they're nested. But here's a clever idea:  

- The total marbles in Box A is the marbles *in* Box A plus the marbles in the box *inside* Box A (Box B).  
- The total marbles in Box B is the marbles *in* Box B plus the marbles in the box *inside* Box B (Box C).  
- The total marbles in Box C is just the marbles *in* Box C (since there's no box inside it).  


### Let's Write This as a "Function"  
Let's call our "marble counter" function `count_marbles(box)`. It returns the total marbles in `box` and all boxes inside it.  

For Box C (no inner box):  
`count_marbles(Box C) = 4` (base case: we know this directly).  

For Box B (has 3 marbles and an inner box):  
`count_marbles(Box B) = 3 + count_marbles(Box C)`  

For Box A (has 2 marbles and an inner box):  
`count_marbles(Box A) = 2 + count_marbles(Box B)`  


### Let's Compute It Step by Step  
Let's plug in the numbers:  

1. Start with `count_marbles(Box C) = 4` (we know this).  
2. Now, `count_marbles(Box B) = 3 + 4 = 7`.  
3. Then, `count_marbles(Box A) = 2 + 7 = 9`.  

So total marbles = 9. That works!  


### What Just Happened?  
We solved the problem by **breaking it into smaller versions of itself**. Instead of trying to count all marbles at once, we solved the problem for the smallest box (base case) and built up the solution for the larger boxes by adding their marbles to the solution of the box inside them.  


### Another Example: Summing Numbers from 1 to n  
Let's try a simpler problem: sum the numbers 1 + 2 + 3 + ... + n.  

- `sum(5) = 5 + sum(4)`  
-...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*