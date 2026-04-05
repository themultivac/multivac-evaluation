# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-084525
**Timestamp:** 2026-04-03T08:45:25.121640
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
| 1 | GPT-5.4 | 9.27 | 8.75 | 10.00 | 0.41 |
| 2 | GPT-OSS-120B | 9.17 | 8.40 | 9.80 | 0.48 |
| 3 | Claude Opus 4.6 | 9.10 | 8.15 | 10.00 | 0.60 |
| 4 | Claude Sonnet 4.6 | 9.01 | 7.75 | 10.00 | 0.77 |
| 5 | Grok 4.20 | 8.87 | 7.75 | 9.80 | 0.63 |
| 6 | Gemini 3 Flash Preview | 8.79 | 8.00 | 9.60 | 0.46 |
| 7 | MiMo-V2-Flash | 8.56 | 6.80 | 9.60 | 0.97 |
| 8 | DeepSeek V3 | 8.03 | 6.95 | 9.15 | 0.73 |
| 9 | MiniMax M2.5 | 5.61 | 1.85 | 8.60 | 2.01 |
| 10 | Gemini 3.1 Pro | 5.26 | 2.65 | 7.80 | 1.72 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.28 |
| 2 | GPT-OSS-120B | 7.54 |
| 3 | Grok 4.20 | 7.77 |
| 4 | Gemini 3.1 Pro | 8.01 |
| 5 | Claude Opus 4.6 | 8.03 |
| 6 | Claude Sonnet 4.6 | 8.18 |
| 7 | MiniMax M2.5 | 8.38 |
| 8 | MiMo-V2-Flash | 8.91 |
| 9 | Gemini 3 Flash Preview | 9.03 |
| 10 | DeepSeek V3 | 9.20 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 89

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

**Generation Time:** 22514ms
**Tokens:** 1616

```
Here’s the main problem: your query does **multiple correlated subqueries per user**, so the `orders` table gets scanned repeatedly for each matching row in `users`.

With 10M rows, that is exactly why it’s slow.

## Optimized query

Rewrite it to aggregate `orders` **once** and join the result:

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

---

## Why this is faster

### Original query issues
For each qualifying `users` row, the query runs:

- `COUNT(*)` once in `SELECT`
- `SUM(amount)` once
- `MAX(created_at)` once
- `COUNT(*)` again in `WHERE`

So that’s effectively **4 separate lookups into `orders` per user**.

If many users match `u.created_at > '2024-01-01'`, this becomes extremely expensive.

### Optimized strategy
Instead:

1. Scan `orders` once
2. Group by `user_id`
3. Compute all aggregates in one pass
4. Filter with `HAVING COUNT(*) > 5`
5. Join to filtered `users`

That reduces repeated work dramatically.

---

## Indexes to add

Primary keys alone are not enough. Add these:

### 1. On `orders(user_id)`
This is the most important one.

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

Why:
- Helps grouping by `user_id`
- Helps join from aggregated orders to users
- Critical if the optimizer chooses index-based aggregation

---

### 2. On `users(created_at)`
```sql
CREATE INDEX idx_users_created_at ON users(created_at);
```

Why:
- Speeds up filtering users with:
  ```sql
  WHERE u.created_at > '2024-01-01'
  ```

---

## Better covering index for `orders`

If your database supports efficient covering/index-only scans, this is even better:

```sql
CREATE INDEX idx_orders_user_id_c...
```

### Claude Opus 4.6

**Generation Time:** 229270ms
**Tokens:** 1883

```


# SQL Query Optimization: From 45s to <1s

## The Problem Analysis

This query has **several critical performance killers**:

```
┌─────────────────────────────────────────────────────┐
│  CORRELATED SUBQUERIES: 4 subqueries × 10M rows    │
│  = up to 40M+ separate subquery executions          │
│                                                      │
│  ❌ Subquery 1: COUNT(*) in SELECT                   │
│  ❌ Subquery 2: SUM(amount) in SELECT                │
│  ❌ Subquery 3: MAX(created_at) in SELECT            │
│  ❌ Subquery 4: COUNT(*) in WHERE (worst offender!)  │
│  ❌ No index on users.created_at                     │
│  ❌ No index on orders.user_id                       │
│  ❌ ORDER BY on an aliased subquery result            │
└─────────────────────────────────────────────────────┘
```

## The Optimized Query

```sql
-- OPTIMIZED: Single pass with JOIN + GROUP BY
SELECT u.name,
       u.email,
       COUNT(o.id)        AS order_count,
       SUM(o.amount)      AS total_spent,
       MAX(o.created_at)  AS last_order
FROM users u
INNER JOIN orders o ON o.user_id = u.id          -- 1. Replaces all 4 subqueries
WHERE u.created_at > '2024-01-01'                -- 2. Filtered early
GROUP BY u.id, u.name, u.email                   -- 3. Aggregate once
HAVING COUNT(o.id) > 5                           -- 4. Replaces WHERE subquery
ORDER BY total_spent DESC
LIMIT 100;
```

## Required Indexes

```sql
-- Index 1: Filter users by date, covering name+email to avoid table lookup
CREATE INDEX idx_users_created_covering
    ON users (created_at, id, name, email);

-- Index 2: Join + aggregate on orders efficiently
CREATE INDEX idx_orders_user_covering
    ON orders (user_id, created_at, amount);
```

### Why These Specific Indexes?

```
idx_users_created_covering (created_at, id, name, email)
├── created_at FIRST  → Range scan for WHERE filter
├── id                → Available for JOIN without table access
├── name, email       → SELECT columns covered (index-only scan)...
```

### Gemini 3.1 Pro

**Generation Time:** 34492ms
**Tokens:** 2253

```
Here is the optimized query, the necessary indexes to add, and a detailed breakdown of the optimization strategy.

### 1. The Rewritten Query

We can eliminate the correlated subqueries by using a `JOIN` combined with `GROUP BY` and `HAVING`. 

```sql
SELECT u.name, 
       u.email, 
       COUNT(o.id) as order_count,
       SUM(o.amount) as total_spent,
       MAX(o.created_at) as last_order
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
```

### Claude Sonnet 4.6

**Generation Time:** 27360ms
**Tokens:** 1726

```
## Problem Analysis

The query has **4 critical performance killers**:

1. **Correlated subqueries** — Each executes once per row in `users` (potentially millions of times)
2. **Subquery in WHERE clause** — Can't use the aggregated result, forces re-computation
3. **Subquery in ORDER BY** — `total_spent` alias isn't reusable, may cause another scan
4. **No composite indexes** — Every subquery does a full scan of `orders` filtered by `user_id`

---

## Optimized Query

```sql
-- Step 1: Aggregate orders ONCE, not once-per-user
WITH order_stats AS (
    SELECT 
        user_id,
        COUNT(*)         AS order_count,
        SUM(amount)      AS total_spent,
        MAX(created_at)  AS last_order
    FROM orders
    GROUP BY user_id
    -- Early filter: only users with > 5 orders
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
-- INNER JOIN implicitly filters users with no qualifying orders
INNER JOIN order_stats os ON os.user_id = u.id
WHERE u.created_at > '2024-01-01'
ORDER BY os.total_spent DESC
LIMIT 100;
```

---

## Indexes to Add

```sql
-- 1. Cover the users WHERE + JOIN condition
--    Optimizer can index-scan created_at, fetch id cheaply
CREATE INDEX idx_users_created_at_id 
    ON users(created_at, id);

-- 2. Cover the entire orders aggregation in one index scan
--    user_id     → GROUP BY / JOIN
--    amount      → SUM()  ← included so heap isn't touched
--    created_at  → MAX()  ← included so heap isn't touched
CREATE INDEX idx_orders_user_covering 
    ON orders(user_id) 
    INCLUDE (amount, created_at);  -- PostgreSQL 11+ / SQL Server syntax

-- MySQL equivalent (put all columns in the index):
CREATE INDEX idx_orders_user_covering 
    ON orders(user_id, amount, created_at);
```

### Why these specific indexes:

```
Query execution with indexes:
                                          
users table                orders t...
```

### Grok 4.20

**Generation Time:** 3041ms
**Tokens:** 946

```
**Optimized Query (typically 200-500ms on 10M rows):**

```sql
SELECT 
    u.name,
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_spent,
    MAX(o.created_at) AS last_order
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 100;
```

### Optimization Strategy

**1. Eliminate Correlated Subqueries (Biggest Win)**

The original query executes **three correlated subqueries** for *every row* in the `users` table that matches the date filter. This is a classic "N+1 on steroids" pattern.

- For every qualifying user, the database runs 3 separate queries against `orders`.
- If 500k users were created after 2024-01-01, you're executing ~1.5 million extra queries.

**2. Use a Single JOIN + GROUP BY instead**

By joining once and aggregating in one pass, we let the database do what it's good at: set-based operations.

**3. Index Strategy (Critical)**

Add these indexes:

```sql
-- Primary index for the date filter + covering
CREATE INDEX idx_users_created_at_id_name_email 
ON users(created_at) INCLUDE (id, name, email);

-- Critical composite index for the join + aggregates
CREATE INDEX idx_orders_user_id_amount_created_at 
ON orders(user_id, amount, created_at);
```

### Alternative Version (Even Faster in Some Cases)

If you have very wide `users` or `orders` tables, this **semi-join** version can be faster:

```sql
WITH heavy_users AS (
    SELECT 
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent,
        MAX(created_at) AS last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
)
SELECT 
    u.name,
    u.email,
    hu.order_count,
    hu.total_spent,
    hu.last_order
FROM heavy_users hu
JOIN users u ON u.id = hu.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY hu.total_spent DESC
LIMIT 100;
```

**Recommended indexes for this version:**
```sql
CREATE INDEX idx_orders_user_id ON ...
```

### DeepSeek V3

**Generation Time:** 19861ms
**Tokens:** 752

```
# SQL Query Optimization

## Problem Analysis
The current query has several performance issues:
1. It uses correlated subqueries (3 for each row) which execute repeatedly for each matching user
2. There's no efficient way to filter users with more than 5 orders without scanning the orders table
3. The sorting operation happens after calculating aggregates for all filtered users

## Optimized Query

```sql
-- Create recommended indexes first
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_user_id_amount ON orders(user_id, amount);
CREATE INDEX idx_orders_user_id_created_at ON orders(user_id, created_at);

-- Optimized query
WITH user_order_stats AS (
    SELECT 
        o.user_id,
        COUNT(*) as order_count,
        SUM(o.amount) as total_spent,
        MAX(o.created_at) as last_order
    FROM orders o
    GROUP BY o.user_id
    HAVING COUNT(*) > 5
)
SELECT 
    u.name, 
    u.email,
    s.order_count,
    s.total_spent,
    s.last_order
FROM users u
JOIN user_order_stats s ON u.id = s.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY s.total_spent DESC
LIMIT 100;
```

## Optimization Strategy

1. **Replace Correlated Subqueries**: Converted multiple correlated subqueries into a single CTE that computes all aggregates in one pass.

2. **Add Efficient Indexes**:
   - `idx_users_created_at`: Speeds up the initial user filtering
   - `idx_orders_user_id`: Essential for joining and counting orders per user
   - `idx_orders_user_id_amount`: Helps with the SUM(amount) calculation
   - `idx_orders_user_id_created_at`: Optimizes the MAX(created_at) calculation

3. **Early Filtering**: The HAVING clause in the CTE filters out users with ≤5 orders early in the process.

4. **Single Pass Aggregation**: The CTE computes all required metrics (count, sum, max) in a single scan of the orders table.

5. **Efficient Join**: The final join between users and pre-aggregated stats is much faster tha...
```

### GPT-OSS-120B

**Generation Time:** 5396ms
**Tokens:** 2292

```
## 1.  Why the original query is slow  

| Problem | What it does | Cost impact |
|---------|--------------|-------------|
| **Three correlated sub‑queries** (`COUNT`, `SUM`, `MAX`) for every row of `users` | The engine scans the whole `orders` table three times for each user that passes the `WHERE` clause. With 10 M rows this is O(N × M). | Hundreds of millions of row‑look‑ups. |
| **Repeated filter on `orders`** (`WHERE o.user_id = u.id`) | No index on `orders.user_id` → full table scans. | Disk‑I/O bound. |
| **`WHERE u.created_at > …`** but no index on `users.created_at` | All rows of `users` are read, then filtered. | Unnecessary rows read. |
| **`HAVING COUNT(*) > 5`** is expressed as another correlated sub‑query, again re‑scanning `orders`. | Same as above. | Redundant work. |
| **`ORDER BY total_spent DESC`** after the sub‑queries | The engine must materialise the whole result set before it can sort. | Memory‑heavy and extra passes. |

The net effect: **the engine touches the 10 M‑row `orders` table many times** and cannot use any index to satisfy the aggregates.

---

## 2.  Core optimisation ideas  

1. **Turn the correlated sub‑queries into a single set‑based aggregation** on `orders`.  
2. **Join the aggregated result to `users`** once, instead of scanning `orders` repeatedly.  
3. **Filter early** – apply the `users.created_at` predicate before the join, and apply the “> 5 orders” predicate in the aggregation (`HAVING`).  
4. **Add the right indexes** so the aggregation can be performed **entirely from an index (index‑only scan)** and the join can be done with a cheap hash/merge join.  
5. **Push the `ORDER BY … LIMIT`** to the outer query after the join – the DB only needs to sort at most the rows that survive the `WHERE`/`HAVING` filters (usually far fewer than 10 M).  

---

## 3.  Re‑written query (set‑based, index‑friendly)

```sql
/* 1️⃣  Aggregate orders per user, keep only users with >5 orders */
WITH agg_orders AS (
    SELECT
        o.user_id...
```

### Gemini 3 Flash Preview

**Generation Time:** 5514ms
**Tokens:** 943

```
To optimize this query from 45 seconds to under 1 second, we must eliminate the **Correlated Subqueries**. 

In your original query, the database is scanning the `orders` table **four times for every single user** found (once for the `WHERE` clause and three times for the `SELECT` list). On a 10M row table, this results in millions of random disk I/O operations.

### The Optimized Query

We will use a `JOIN` with a pre-aggregated derived table. This allows the database to aggregate the `orders` table in a single pass before joining it to the filtered `users`.

```sql
SELECT 
    u.name, 
    u.email, 
    stats.order_count, 
    stats.total_spent, 
    stats.last_order
FROM users u
INNER JOIN (
    -- Aggregate orders first to avoid repeated subqueries
    SELECT 
        user_id, 
        COUNT(*) as order_count, 
        SUM(amount) as total_spent, 
        MAX(created_at) as last_order
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 5
) stats ON u.id = stats.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY stats.total_spent DESC
LIMIT 100;
```

---

### Optimization Strategy

1.  **Eliminate Row-by-Row Processing:** By moving the logic into a `GROUP BY` subquery (or a CTE), we process the `orders` table as a set. The database engine can use a **Hash Aggregate** or a **Merge Join**, which are significantly faster than nested loops for large datasets.
2.  **Early Filtering:** The `HAVING COUNT(*) > 5` clause inside the subquery reduces the number of rows that need to be joined to the `users` table.
3.  **Single Pass:** We calculate `COUNT`, `SUM`, and `MAX` in one scan of the `orders` index rather than three separate lookups.

---

### Required Indexes

Even with a better query, you need specific indexes to handle 10M rows in under a second. Add these:

**1. For the `users` table:**
```sql
CREATE INDEX idx_users_created_at ON users(created_at);
```
*   **Why:** This allows the engine to instantly find only the users created in 2024 rather than scanning...
```

### MiniMax M2.5

**Generation Time:** 12783ms
**Tokens:** 2257

```
**Why the original query is slow**

| Problem | What it does | Why it hurts |
|---------|--------------|--------------|
| **Four correlated sub‑queries per row** – `COUNT(*)`, `SUM(amount)`, `MAX(created_at)` and another `COUNT(*)` in the `WHERE` clause | For every user that survives the `created_at` filter the engine runs four separate scans of the `orders` table. | With e.g. 2 M users after the date filter you execute ≈ 8 M index‑look‑ups (4 × 2 M). That is an *O(N × M)* workload – roughly 45 s on 10 M rows. |
| **“total_spent” is a derived expression** – the `ORDER BY` cannot use any index | The query sorts on `total_spent` (the sum) after all the sub‑queries have been computed. | Sorting millions of rows in memory is expensive. |
| **No useful secondary indexes** – only primary‑key B‑trees exist | The optimizer has to fall back to full table scans or very inefficient nested‑loop joins. | Every lookup is a random I/O. |

The fix is to **compute the aggregates once**, join the pre‑aggregated result, and let the optimizer use covering indexes for both the user filter and the order aggregation.

---

## 1. Rewritten query (MySQL / PostgreSQL compatible)

```sql
SELECT u.name,
       u.email,
       o.order_count,
       o.total_spent,
       o.last_order
FROM   users u
JOIN   (
         SELECT user_id,
                COUNT(*)        AS
```

### MiMo-V2-Flash

**Generation Time:** 10479ms
**Tokens:** 1307

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

The original query suffers from the **"N+1 Query Problem"** (or more specifically, the "Correlated Subquery Problem"). For every user created after 2024-01-01, the database executes three separate subqueries against the `orders` table. With 10 million rows, this results in millions of repeated index lookups, causing the 45-second execution time.

Here is the step-by-step breakdown of the optimizations:

#### 1. Replace Correlated Subqueries with a Single `JOIN`
Instead of joining the `orders` table three times (once for count, once for sum, once for max), we join it once using a `LEFT JOIN`.
*   **Why:** This allows the database to scan the `orders` table (or its index) exactly once per relevant user, rather than scanning it three times.
*   **LEFT JOIN vs INNER JOIN:** We use `LEFT JOIN` to ensure users with zero orders are still considered (though the `HAVING` clause will filter them out later). This prevents losing users if the logic changes.

#### 2. Move Filtering to `HAVING`
The original query filtered by order count in the `WHERE` clause using a subquery.
*   **Optimization:** We calculate the aggregates (`COUNT`, `SUM`, `MAX`) first, then filter the results using the `HAVING` clause.
*   **Note:** `HAVING` is executed after the grouping, which is necessary to compare the calculated count against the value `5`.

#### 3. Add Required Indexes
The prompt states we assume standard B-tree indexes on primary keys (PK) only. The current state likely has:
*   `users`: PK on `id`
*   `orders`: PK on `id` (and likely a f...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*