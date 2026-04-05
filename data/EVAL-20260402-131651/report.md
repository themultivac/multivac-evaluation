# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-131651
**Timestamp:** 2026-04-02T13:16:51.002972
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

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
| 1 | Claude Opus 4.6 | 9.29 | 8.55 | 10.00 | 0.48 |
| 2 | GPT-5.4 | 9.06 | 7.20 | 9.80 | 0.86 |
| 3 | Gemini 3 Flash Preview | 8.51 | 7.75 | 9.35 | 0.52 |
| 4 | MiMo-V2-Flash | 8.45 | 6.25 | 9.55 | 1.19 |
| 5 | DeepSeek V3 | 7.09 | 4.65 | 8.00 | 1.20 |
| 6 | Gemini 3.1 Pro | 1.08 | 0.20 | 2.45 | 0.73 |
| None | Claude Sonnet 4.6 | 9.16 | 8.40 | 10.00 | 0.56 |
| None | GPT-OSS-120B | 8.82 | 7.75 | 9.80 | 0.87 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.42 |
| 2 | Grok 4.20 | 6.75 |
| 3 | Claude Opus 4.6 | 7.56 |
| 4 | MiMo-V2-Flash | 7.66 |
| 5 | Claude Sonnet 4.6 | 7.81 |
| 6 | MiniMax M2.5 | 7.83 |
| 7 | Gemini 3.1 Pro | 8.00 |
| 8 | Gemini 3 Flash Preview | 8.37 |
| 9 | GPT-OSS-120B | 8.60 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gpt_oss_120b
**Total Judgments:** 90
**Valid Judgments:** 54

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

**Generation Time:** 53231ms
**Tokens:** 1565

```
Use one pass over `orders`, not 4 correlated subqueries per user.

## Rewritten query

```sql
SELECT
    u.name,
    u.email,
    agg.order_count,
    agg.total_spent,
    agg.last_order
FROM users u
JOIN (
    SELECT
        o.user_id,
        COUNT(*) AS order_count,
        SUM(o.amount) AS total_spent,
        MAX(o.created_at) AS last_order
    FROM orders o
    GROUP BY o.user_id
    HAVING COUNT(*) > 5
) agg ON agg.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY agg.total_spent DESC
LIMIT 100;
```

## Why the original is slow

Your original query does this for each qualifying user:

- `COUNT(*)` from `orders`
- `SUM(amount)` from `orders`
- `MAX(created_at)` from `orders`
- another `COUNT(*)` in the `WHERE`

That means repeated scans/lookups into `orders` for every user row. On a 10M-row `orders` table, this becomes very expensive.

## Optimization strategy

### 1. Replace correlated subqueries with one aggregation
Instead of re-reading `orders` multiple times per user, aggregate once:

- `COUNT(*)`
- `SUM(amount)`
- `MAX(created_at)`

grouped by `user_id`.

This turns many repeated operations into a single grouped pass over `orders`.

### 2. Filter aggregated users early with `HAVING`
The condition:

```sql
(SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5
```

becomes:

```sql
HAVING COUNT(*) > 5
```

This removes low-activity users before joining back to `users`.

### 3. Join only the needed users
After aggregation, join to `users` and apply:

```sql
u.created_at > '2024-01-01'
```

### 4. Sort only aggregated result set
Sorting by `total_spent` now happens on the reduced grouped result, not after executing many subqueries.

---

# Indexes to add

With only PK indexes, the database likely has:

- `users(id)`
- `orders(id)`

That is not enough.

## Recommended indexes

### On `orders`
Most important:

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

Better if your database can benefit from covering/grouped access:

```sql
C...
```

### Claude Opus 4.6

**Generation Time:** 36386ms
**Tokens:** 1860

```


# SQL Query Optimization: From 45s to <1s

## Why the Original Query is Catastrophically Slow

The original query has **four correlated subqueries** — each one executes once **per row** in the `users` table. With 10M rows, that's potentially **40M+ sequential scans** of the `orders` table.

```
For each user row (millions after date filter):
  → Scan orders table for COUNT(*)      ← subquery 1
  → Scan orders table for SUM(amount)   ← subquery 2
  → Scan orders table for MAX(created)  ← subquery 3
  → Scan orders table for COUNT(*) > 5  ← subquery 4 (duplicate!)
```

## The Optimized Query

```sql
SELECT u.name,
       u.email,
       o_agg.order_count,
       o_agg.total_spent,
       o_agg.last_order
FROM users u
INNER JOIN (
    -- Pre-aggregate ALL order stats in a single pass
    SELECT user_id,
           COUNT(*)        AS order_count,
           SUM(amount)     AS total_spent,
           MAX(created_at) AS last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5          -- Filter early: eliminates users with ≤5 orders
) o_agg ON o_agg.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY o_agg.total_spent DESC
LIMIT 100;
```

## Required Indexes

```sql
-- Index 1: Accelerate the user date filter + cover the SELECT columns
CREATE INDEX idx_users_created_covering
    ON users (created_at)
    INCLUDE (name, email);           -- Covering index avoids heap lookups

-- Index 2: Accelerate the GROUP BY on orders + cover aggregation columns
CREATE INDEX idx_orders_user_covering
    ON orders (user_id)
    INCLUDE (amount, created_at);    -- Index-only scan for the aggregation
```

## Optimization Strategy Breakdown

### 1. Eliminate Correlated Subqueries → Single JOIN

```
BEFORE: 4 subqueries × N rows = O(4N) table scans
AFTER:  1 aggregation pass     = O(1) table scan of orders

┌──────────────────────────────────────────────────────┐
│  BEFORE (Row-by-Row)          AFTER (Set-Based)      │
│                                                 ...
```

### Gemini 3.1 Pro

**Generation Time:** 33316ms
**Tokens:** 2253

```
 5` orders.
    *   *Aggregation:* `COUNT(*)` vs `COUNT(o.id)`. `COUNT(*)` is fine and often slightly faster/optimized by the engine. I'll use `COUNT(*)` or `COUNT(o.id)` interchangeably, but `COUNT(o.id)` makes it explicit we are counting joined rows. Let's stick to
```

### Claude Sonnet 4.6

**Generation Time:** 38084ms
**Tokens:** 1472

```
## Problem Analysis

The query has **4 critical performance killers**:

1. **Correlated subqueries** — executes once per row in `users` (potentially millions of times)
2. **Subquery in WHERE clause** — can't use the aggregated result, forces re-computation
3. **No index on `users.created_at`** — full table scan on 10M rows
4. **No index on `orders.user_id`** — each subquery does a full `orders` table scan

---

## Optimized Query

```sql
-- Step 1: Aggregate orders ONCE, not per-user
WITH order_stats AS (
    SELECT 
        user_id,
        COUNT(*)         AS order_count,
        SUM(amount)      AS total_spent,
        MAX(created_at)  AS last_order
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
INNER JOIN order_stats os ON os.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY os.total_spent DESC
LIMIT 100;
```

---

## Required Indexes

```sql
-- 1. Filter users by date (eliminates full table scan on users)
CREATE INDEX idx_users_created_at 
    ON users(created_at);

-- 2. Core fix: allows GROUP BY user_id without full orders scan
--    Covers the JOIN, COUNT, SUM, and MAX in one index
CREATE INDEX idx_orders_user_id_amount_created 
    ON orders(user_id, amount, created_at);
```

### Why a covering index on orders?

```
Query needs:  user_id  ✓  (GROUP BY / JOIN)
              amount   ✓  (SUM)
              created_at ✓ (MAX)

Without it:  Index scan → heap fetch per row  (random I/O, catastrophic at scale)
With it:     Index-only scan                  (sequential, no heap access)
```

---

## Execution Plan Comparison

```
BEFORE (correlated subqueries):
─────────────────────────────────────────────────────────
Nested Loop
  → Seq Scan on users          (10M rows, no index)
    → Seq Scan on orders       (runs 10M times!)
      filter: user_i...
```

### DeepSeek V3

**Generation Time:** 18919ms
**Tokens:** 478

```
# SQL Query Optimization

The current query is inefficient because it performs correlated subqueries for each user row, resulting in multiple full table scans of the orders table. Here's an optimized version:

```sql
WITH user_orders AS (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spent,
        MAX(created_at) as last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
)

SELECT 
    u.name, 
    u.email, 
    o.order_count,
    o.total_spent,
    o.last_order
FROM users u
JOIN user_orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total_spent DESC
LIMIT 100;
```

## Optimization Strategy

1. **Eliminate correlated subqueries**: Instead of running subqueries for each user row, we pre-aggregate order data in a CTE.

2. **Apply filter early**: The `HAVING COUNT(*) > 5` condition is moved into the CTE to filter before joining.

3. **Use a single join**: This replaces multiple subqueries with one efficient join operation.

## Recommended Indexes

To further optimize performance, add these indexes:

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_created_at
```

### GPT-OSS-120B

**Generation Time:** 11898ms
**Tokens:** 2299

```
## 1.  Why the original query is slow  

| Problem | What it does | Cost |
|---------|--------------|------|
| **Scalar sub‑queries in the SELECT list** | For every row in `users` the engine runs three separate scans of the `orders` table (COUNT, SUM, MAX). With 10 M users this means millions of extra scans. | O(#users × #orders) |
| **Repeated sub‑query in the WHERE clause** | The same `COUNT(*)` is executed again to test `> 5`. That’s a fourth full scan per user. | O(#users × #orders) |
| **No filtering on `orders`** | The engine cannot prune rows early because `orders` is never joined; it must read the whole table for each sub‑query. | Full table scans |
| **Missing supporting indexes** | Only PKs exist, so the engine cannot jump directly to a user’s orders. | No index‑seek, only full scans |
| **ORDER BY on a computed column** | `total_spent` is produced by a sub‑query, so the DB cannot sort using an index. | Sort after materialisation |

All of the above pushes the planner into a *nested‑loop* style execution that touches `orders` many times → ≈ 45 s.

---

## 2.  The optimisation strategy  

1. **Turn the scalar sub‑queries into a single aggregate query** that reads `orders` **once** and produces all three metrics (`order_count`, `total_spent`, `last_order`).  
2. **Filter early** – keep only users that have more than 5 orders (`HAVING COUNT(*) > 5`).  
3. **Join the aggregated result to `users`** instead of scanning `orders` per row.  
4. **Push the date filter (`users.created_at > …`) down to the `users` side** so the join touches only the relevant users.  
5. **Add covering B‑tree indexes** that let the DB:  
   * locate the relevant users quickly (`users(created_at)`)  
   * retrieve all needed order columns without touching the heap (`orders(user_id, amount, created_at)`).  
6. **Sort on the already‑computed `total_spent`** – the planner can use the index on the aggregate (or an in‑memory sort on a much smaller result set).  

The resulting plan is a **si...
```

### Gemini 3 Flash Preview

**Generation Time:** 18816ms
**Tokens:** 954

```
To optimize this query, we need to address the **"N+1" subquery problem**. In your original query, the database engine is performing up to four separate scans of the `orders` table for every single user that matches the date criteria. On a 10M row table, this results in millions of redundant lookups.

### 1. The Optimized SQL Rewrite

We will use a **Common Table Expression (CTE)** or a **JOIN** to aggregate the `orders` data once, then join it to the filtered `users` table.

```sql
SELECT 
    u.name, 
    u.email, 
    o.order_count, 
    o.total_spent, 
    o.last_order
FROM users u
JOIN (
    -- Aggregate orders first to avoid multiple subqueries per row
    SELECT 
        user_id, 
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

---

### 2. Optimization Strategy

1.  **Eliminate Correlated Subqueries:** The original query runs the subqueries in the `SELECT` and `WHERE` clauses for every candidate row. By moving these into a single `GROUP BY` block, we scan the `orders` table once (or use an index) rather than millions of times.
2.  **Filter Early:** The `HAVING` clause filters out users with $\le 5$ orders before joining with the `users` table, reducing the number of joins performed.
3.  **Index Leveraging:** With the correct indexes (listed below), the database can perform an **Index Only Scan** for the aggregations, meaning it never has to touch the actual table data on disk for the `orders` calculations.

---

### 3. Required Indexes

To bring this under 1 second, you must add these specific indexes:

#### For the `users` table:
```sql
CREATE INDEX idx_users_created_at ON users(created_at);
```
*   **Why:** This allows the engine to instantly find only the users created after '2024-01-01' instead of scanning all 10M rows.

#### For the `...
```

### MiniMax M2.5

**Generation Time:** 40468ms
**Tokens:** 2260

```

```

### MiMo-V2-Flash

**Generation Time:** 15161ms
**Tokens:** 1397

```
Here is the optimized query and the explanation of the strategy.

### Optimized Query

```sql
SELECT u.name, u.email, 
       COUNT(o.id) as order_count,
       COALESCE(SUM(o.amount), 0) as total_spent,
       MAX(o.created_at) as last_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 100;
```

---

### Optimization Strategy

The original query suffers from the **"N+1 Select Problem"** using correlated subqueries. For every user created after 2024-01-01, the database executes three separate subqueries against the `orders` table. If there are 1 million such users, the database performs 3 million lookups, even before sorting and limiting.

Here is the step-by-step optimization breakdown:

#### 1. Replace Correlated Subqueries with a `LEFT JOIN`
Instead of running separate subqueries for every row in `users`, we join the `orders` table once. This allows the database to scan both tables efficiently and aggregate the data in a single pass.
*   **Old:** 3 subqueries per user (Scanning `orders` index 3 times per user).
*   **New:** 1 join (Scanning `orders` index once per user).

#### 2. Use `LEFT JOIN` instead of `INNER JOIN`
We use `LEFT JOIN` to ensure we include users who might have zero orders (though the `HAVING` clause later filters them out). This syntax is safer if the filtering logic changes later.

#### 3. Move Filter Logic to `HAVING`
The original query filtered by `COUNT(*) > 5` in the `WHERE` clause. Since this calculation depends on the aggregate of the joined `orders` table, it must be moved to the `HAVING` clause. This is executed after the join and grouping, which is more efficient than re-running a subquery in the `WHERE` clause.

#### 4. Use `COALESCE` for Sums
When using a `LEFT JOIN`, users with no orders will have `NULL` amounts. `SUM(NULL)` returns `NULL`. `COALESCE(SUM(o.amount), 0)` ensures the result is `0` rather than ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*