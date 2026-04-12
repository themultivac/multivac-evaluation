# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-161904
**Timestamp:** 2026-03-18T16:19:04.487304
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

This SQL query takes 45 seconds on a table with 10M rows. Rewrite it to run in under 1 second. Explain your optimization strategy.

```sql
SELECT u.name, u.email,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
       (SELECT SUM(amount) FROM orders o WHERE o.user_id = u.id) as total_spent,
       (SELECT MAX(created_at) FROM orders o WHERE o.user_id = u.id) as last_order
FROM users u
WHERE u.created_at > '2024-01-01'
AND (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5
ORDER BY total_spent DESC
LIMIT 100;
```

Assume standard B-tree indexes on primary keys only. What indexes would you add?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.72 | 9.35 | 10.00 | 0.25 |
| 2 | Claude Sonnet 4.6 | 9.66 | 7.80 | 10.00 | 0.82 |
| 3 | MiniMax M1 | 9.39 | 7.20 | 10.00 | 0.99 |
| 4 | MiniMax M2.7 | 9.09 | 6.95 | 10.00 | 1.07 |
| 5 | MiniMax M2.5 | 8.96 | 7.00 | 10.00 | 0.99 |
| 6 | MiniMax-01 | 7.90 | 6.60 | 8.55 | 0.70 |
| 7 | MiniMax M2.1 | 7.04 | 5.20 | 8.60 | 1.29 |
| 8 | MiniMax M2 | 4.41 | 2.10 | 7.60 | 1.82 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.18 |
| 2 | Claude Sonnet 4.6 | 7.88 |
| 3 | MiniMax M2.1 | 8.27 |
| 4 | MiniMax M2.7 | 8.39 |
| 5 | MiniMax M2.5 | 8.39 |
| 6 | MiniMax M1 | 8.46 |
| 7 | MiniMax M2 | 9.29 |
| 8 | MiniMax-01 | 9.31 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_01
**Total Judgments:** 72
**Valid Judgments:** 56

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

**Generation Time:** 34253ms
**Tokens:** 1911

```
# SQL Query Optimization Analysis

## Problems with Current Query

Your query suffers from **4 correlated subqueries per row**, causing a **cartesian product of execution** against your 10M row table.

```
Current Execution Pattern:
For EACH user row:
  ├─ Execute: COUNT(*) FROM orders WHERE user_id = ?
  ├─ Execute: SUM(amount) FROM orders WHERE user_id = ?
  ├─ Execute: MAX(created_at) FROM orders WHERE user_id = ?
  └─ Execute: COUNT(*) FROM orders WHERE user_id = ? (for HAVING)

Result: ~40M+ subquery executions instead of 1 aggregation pass
```

---

## Optimized Query

```sql
SELECT 
    u.name, 
    u.email,
    o.order_count,
    o.total_spent,
    o.last_order_date
FROM users u
INNER JOIN (
    SELECT 
        user_id,
        COUNT(*)       AS order_count,
        SUM(amount)    AS total_spent,
        MAX(created_at) AS last_order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
  AND o.order_count > 5
ORDER BY o.total_spent DESC
LIMIT 100;
```

---

## Indexes to Add

```sql
-- Primary optimization: covers all aggregation operations
CREATE INDEX idx_orders_user_aggregation 
    ON orders (user_id, amount, created_at);

-- Speeds up WHERE clause on users table
CREATE INDEX idx_users_created_at 
    ON users (created_at);
```

### Index Strategy Explanation

| Index | Purpose |
|-------|---------|
| `orders(user_id)` | **Minimum required** - enables index-only scans for COUNT/SUM/MAX |
| `orders(user_id, amount)` | Allows SUM to use index without touching heap |
| `orders(user_id, created_at)` | Allows MAX to use index without touching heap |
| `users(created_at)` | Seeks directly to relevant users, avoids full scan |

> **Pro tip:** A covering index `(user_id, amount, created_at)` satisfies all three aggregations in a single index scan.

---

## Why This Works

```
BEFORE: Correlated Subqueries (O(n × m) complexity)
┌─────────────────────────────────────────────────────────┐
│  users ──► for each row ──► ...
```

### MiniMax M2.5

**Generation Time:** 41479ms
**Tokens:** 2256

```
**Why the original query is slow**

| Problem | What really happens |
|---------|----------------------|
| **Correlated sub‑queries** | For every user that survives the `WHERE u.created_at …` filter the engine runs **four** separate sub‑queries against `orders` (count, sum, max, and the extra count in the `WHERE` clause). With 10 M order rows this means scanning the `orders` table dozens of times. |
| **No index on `orders.user_id`** | The only indexes are the PKs, so every sub‑query does a full table scan (or a very expensive index‑seek followed by a huge number of random I/Os). |
| **No index on `users.created_at`** | The date filter also forces a full scan of the `users` table before any of the correlated sub‑queries can even start. |
| **Sorting on the fly** | `ORDER BY total_spent DESC` is computed after all the rows are fetched, because `total_spent` is the result of a scalar sub‑query. The optimizer cannot use an index for the sort. |

All of these together explain the 45‑second runtime.

---

## 1️⃣ Optimised query

The trick is to **aggregate the order data once**, then join the pre‑computed totals to the users.  This removes all correlated sub‑queries and lets the engine use indexes for the join, filter and sort.

```sql
/* CTE – compute all order stats per user once */
WITH user_order_stats AS (
    SELECT
        o.user_id,
        COUNT(*)        AS order_count,
        SUM(o.amount)  AS total_spent,
        MAX(o.created_at) AS last_order
    FROM orders o
    GROUP BY o.user_id
    HAVING COUNT(*) > 5          -- move the “> 5 orders” filter here
)

SELECT
    u.name,
    u.email,
    ios.order_count,
    ios.total_spent,
    ios.last_order
FROM users u
JOIN user_order_stats ios ON ios.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY ios.total_spent DESC
LIMIT 100;
```

### What changed?

| Original element | Optimised version |
|------------------|-------------------|
| 4 correlated sub‑queries per user | Single aggregation (`GROUP BY user_i...
```

### MiniMax M2.1

**Generation Time:** 21070ms
**Tokens:** 2261

```
# SQL Query Optimization

## Rewritten Query

```sql
SELECT u.name, u.email,
       o.order_count,
       o.total_spent,
       o.last_order
FROM users u
INNER JOIN (
    SELECT user_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent,
           MAX(created_at) as last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
) o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total_spent DESC
LIMIT 100;
```

## Optimization Strategy

### Problem Analysis
The original query uses **correlated subqueries** that execute once for each row in the `users` table that meets the date filter. With 10M rows, this means:

```

### MiniMax M2

**Generation Time:** 64091ms
**Tokens:** 2257

```
**Why the original query is slow**

| Problem | What actually happens | Cost |
|---------|-----------------------|------|
| **Correlated sub‑queries** – four of them (`COUNT(*)`, `SUM(amount)`, `MAX(created_at)`, and the duplicate `COUNT(*)` in the `WHERE`) run once for **every** row returned from `users`. With 10 M rows the engine executes ~40 M sub‑query iterations. | The inner tables (`orders`) are scanned (or looked up) repeatedly for the same `user_id`. | O(N·M) where N = users that survive the `
```

### MiniMax M1

**Generation Time:** 29985ms
**Tokens:** 2142

```
# SQL Query Optimization Analysis

## Problem Diagnosis

Your query has **four correlated subqueries** that execute once per user row, resulting in catastrophic performance:

```
10M user rows × 4 subqueries × avg orders per user scans = ~45 seconds
```

### Issues Identified:

| Issue | Impact |
|-------|--------|
| Correlated subqueries in SELECT | 4 full table scans per user |
| Correlated subquery in WHERE | Additional scan per user |
| No index on `orders.user_id` | Full orders table scan for each subquery |
| No index on `users.created_at` | Full users table scan |
| ORDER BY alias `total_spent` | May prevent sort optimization |

---

## Optimized Query

```sql
-- Pre-aggregate orders once, then join
SELECT u.name, u.email,
       o.order_count,
       o.total_spent,
       o.last_order
FROM users u
INNER JOIN (
    SELECT 
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent,
        MAX(created_at) AS last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
) o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total_spent DESC
LIMIT 100;
```

---

## Index Strategy

```sql
-- Primary optimization: index on foreign key with covering columns
CREATE INDEX idx_orders_user_id_agg 
    ON orders (user_id, amount, created_at);

-- Filter optimization for users table
CREATE INDEX idx_users_created_at 
    ON users (created_at);

-- Optional: covering index for users (avoids table access)
CREATE INDEX idx_users_covering 
    ON users (created_at, id, name, email);
```

---

## Execution Plan Comparison

```
BEFORE (Correlated Subqueries):
┌─────────────────────────────────────────────────────────────┐
│  Table Scan: users (10M rows)                               │
│    └─→ For each user:                                       │
│        ├─→ Subquery: COUNT(*) FROM orders (full scan)      │
│        ├─→ Subquery: SUM(amount) FROM orders (full scan)   │
│        ├─→ Subquery: MAX(created_at) FROM orders (full...
```

### MiniMax-01

**Generation Time:** 27816ms
**Tokens:** 2012

```
To optimize your SQL query and reduce the execution time from 45 seconds to under 1 second, we can employ several strategies, including **query restructuring**, **using JOINs instead of correlated subqueries**, and **adding appropriate indexes**. Here's a step-by-step approach to achieve this:

---

### **1. Problem Analysis**
The original query has the following issues:
- **Correlated Subqueries**: The subqueries in the `SELECT` clause and the `WHERE` clause are correlated with the `users` table, causing them to execute once per row. This results in a high number of scans on the `orders` table (10M rows), leading to poor performance.
- **Lack of Indexes**: The query relies solely on primary key indexes, which is insufficient for the join conditions and filters used.

---

### **2. Optimization Strategy**
To optimize the query, we will:
1. **Replace Correlated Subqueries with JOINs**: This allows the database to process the data more efficiently by leveraging set-based operations.
2. **Aggregate Data in a Single Pass**: Use aggregate functions with `GROUP BY` to compute `order_count`, `total_spent`, and `last_order` in one step.
3. **Add Appropriate Indexes**: Create indexes on columns used in `JOIN`, `WHERE`, and `ORDER BY` clauses to speed up data retrieval.

---

### **3. Rewritten Query**
Here is the optimized version of the query:

```sql
SELECT 
    u.name, 
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_spent,
    MAX(o.created_at) AS last_order
FROM 
    users u
LEFT JOIN 
    orders o 
    ON o.user_id = u.id
WHERE 
    u.created_at > '2024-01-01'
    AND o.id IS NOT NULL
GROUP BY 
    u.id, u.name, u.email
HAVING 
    COUNT(o.id) > 5
ORDER BY 
    total_spent DESC
LIMIT 100;
```

---

### **4. Explanation of Changes**
1. **JOIN Instead of Correlated Subqueries**:
   - The `LEFT JOIN` ensures that all users are included, even if they have no orders. The `o.id IS NOT NULL` condition ensures that only users with at least one order are...
```

### Claude Sonnet 4.6

**Generation Time:** 25952ms
**Tokens:** 1536

```
## Problem Analysis

The query has **4 critical performance killers**:

1. **Correlated subqueries** — Each executes once per row in `users`, so with 10M users filtered to say 500K post-2024, you get **2M+ individual subquery executions**
2. **Subquery in WHERE clause** — `COUNT(*)` subquery runs before filtering, can't use the result from SELECT
3. **No useful indexes** — `users.created_at` and `orders.user_id` are unindexed
4. **ORDER BY on computed column** — Forces full result materialization before sorting

---

## Optimized Query

```sql
-- Step 1: Aggregate orders ONCE, not per-user
WITH order_stats AS (
    SELECT 
        user_id,
        COUNT(*)        AS order_count,
        SUM(amount)     AS total_spent,
        MAX(created_at) AS last_order
    FROM orders
    GROUP BY user_id
    -- Pre-filter: only users with > 5 orders
    -- Eliminates rows before joining to users
    HAVING COUNT(*) > 5
)
SELECT 
    u.name,
    u.email,
    os.order_count,
    os.total_spent,
    os.last_order
FROM users u
    -- INNER JOIN implicitly filters users who have no matching order_stats
    INNER JOIN order_stats os ON os.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY os.total_spent DESC
LIMIT 100;
```

**Why this works:**
- `orders` is aggregated **once** (one full scan vs. millions of correlated lookups)
- `HAVING COUNT(*) > 5` eliminates low-order users *before* the join
- `INNER JOIN` replaces the correlated subquery in `WHERE`
- `total_spent` is now a real column the optimizer can sort efficiently

---

## Indexes to Add

```sql
-- Index 1: Filter users by date (WHERE clause)
-- Allows index range scan instead of full table scan
CREATE INDEX idx_users_created_at 
    ON users(created_at);

-- Index 2: The most critical index
-- Covers the entire aggregation in order_stats CTE
-- user_id    → GROUP BY / JOIN key
-- amount     → SUM() covered, no heap access needed  
-- created_at → MAX() covered, no heap access needed
CREATE INDEX idx_orders_user_coveri...
```

### GPT-5.4

**Generation Time:** 16829ms
**Tokens:** 1451

```
Use one pass over `orders`, not 4 correlated subqueries per user.

## Rewritten query

```sql
SELECT
    u.name,
    u.email,
    o.order_count,
    o.total_spent,
    o.last_order
FROM users u
JOIN (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent,
        MAX(created_at) AS last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
) o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total_spent DESC
LIMIT 100;
```

## Why the original is slow

Your original query does this for every qualifying user:

- `COUNT(*)` from `orders`
- `SUM(amount)` from `orders`
- `MAX(created_at)` from `orders`
- another `COUNT(*)` in the `WHERE`

That means repeated scans/lookups into `orders` for the same user. On 10M rows, that explodes.

So instead of:

- many repeated per-user subqueries

do:

- one aggregation of `orders`
- join the result to `users`

## Best index additions

### 1. On `orders(user_id)`
This is the most important one.

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

It helps with:

- grouping by `user_id`
- join from aggregated orders back to users
- any future per-user order lookups

### 2. On `users(created_at)`
Since you filter users by date:

```sql
CREATE INDEX idx_users_created_at ON users(created_at);
```

This helps avoid scanning all users.

---

## Even better covering index on orders

If your DB supports index-only scans effectively, use:

```sql
CREATE INDEX idx_orders_user_id_created_at_amount
ON orders(user_id, created_at, amount);
```

Why:

- `user_id` for grouping
- `created_at` for `MAX(created_at)`
- `amount` for `SUM(amount)`

This can reduce table reads substantially.

If I had to pick practical indexes:

```sql
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

If you want a more aggressive optimization:

```sql
CREATE INDEX idx_orders_user_id_created_amount
ON orders(user_id, created_at ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*