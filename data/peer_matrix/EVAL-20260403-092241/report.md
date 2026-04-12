# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-092241
**Timestamp:** 2026-04-03T09:22:41.079882
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Write a database migration that adds a NOT NULL column with a default value to a table with 50 million rows in PostgreSQL — without locking the table or causing downtime. Explain the step-by-step process, why naive ALTER TABLE fails at scale, and how to verify data integrity after migration.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.16 | 8.40 | 10.00 | 0.51 |
| 2 | Gemini 3 Flash Preview | 8.67 | 7.00 | 9.60 | 0.76 |
| 3 | Claude Sonnet 4.6 | 8.27 | 6.85 | 10.00 | 1.21 |
| 4 | MiMo-V2-Flash | 8.24 | 6.75 | 9.80 | 1.08 |
| 5 | GPT-OSS-120B | 8.22 | 5.00 | 10.00 | 1.88 |
| 6 | Claude Opus 4.6 | 8.11 | 6.25 | 9.35 | 1.05 |
| 7 | Grok 4.20 | 7.74 | 5.00 | 9.60 | 1.53 |
| 8 | DeepSeek V3 | 7.45 | 5.40 | 9.15 | 1.32 |
| 9 | Gemini 3.1 Pro | 7.27 | 4.05 | 9.05 | 1.58 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.34 |
| 2 | Gemini 3.1 Pro | 6.47 |
| 3 | Claude Opus 4.6 | 7.71 |
| 4 | GPT-OSS-120B | 8.01 |
| 5 | Grok 4.20 | 8.04 |
| 6 | MiniMax M2.5 | 8.29 |
| 7 | Claude Sonnet 4.6 | 8.36 |
| 8 | MiMo-V2-Flash | 8.97 |
| 9 | Gemini 3 Flash Preview | 9.51 |
| 10 | DeepSeek V3 | 9.53 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 81

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

**Generation Time:** 31441ms
**Tokens:** 2112

```
Below is the standard zero-downtime pattern for adding a `NOT NULL` column with a default to a very large PostgreSQL table.

---

# Goal

Add a new column to a table with ~50 million rows:

- with a default value
- eventually `NOT NULL`
- without long table locks
- without downtime

Assume:

```sql
ALTER TABLE orders
ADD COLUMN status text NOT NULL DEFAULT 'pending';
```

This is what we want logically, but **not** how we should do it on a large hot table.

---

# Why the naive `ALTER TABLE` is risky at scale

A one-shot migration like:

```sql
ALTER TABLE orders
ADD COLUMN status text NOT NULL DEFAULT 'pending';
```

can be problematic because:

1. **Long-lived lock risk**
   - `ALTER TABLE` takes an `ACCESS EXCLUSIVE` lock.
   - Even if PostgreSQL can optimize parts of the operation, that lock can block reads/writes or wait behind existing transactions.
   - On a busy table, lock acquisition alone can cause outages.

2. **Table rewrite risk on older PostgreSQL versions**
   - In PostgreSQL versions before the “fast default” optimization, adding a column with a non-NULL default could rewrite the whole table.
   - Rewriting 50 million rows means huge I/O, WAL generation, replication lag, and long lock times.

3. **Setting `NOT NULL` immediately can force a full scan**
   - PostgreSQL must ensure no row violates the constraint.
   - On a huge table, validating this in one step can be expensive and disruptive.

So even though the SQL is simple, the operational impact can be severe.

---

# Safe zero-downtime migration strategy

Use a **multi-step migration**:

1. Add the column as nullable, with no default.
2. Set the default for new rows only.
3. Backfill existing rows in small batches.
4. Add a `CHECK` constraint as `NOT VALID`.
5. Validate the constraint.
6. Convert to `NOT NULL` if desired.

This avoids large rewrites and minimizes lock duration.

---

# Step-by-step migration

## Step 1: Add the column as nullable

This is metadata-only and usually very fast.

``...
```

### Claude Opus 4.6

**Generation Time:** 37166ms
**Tokens:** 2119

```
# Zero-Downtime Migration: Adding a NOT NULL Column at Scale in PostgreSQL

## Why Naive `ALTER TABLE` Fails at Scale

```sql
-- ❌ THIS WILL LOCK YOUR TABLE AND CAUSE DOWNTIME
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';
```

### What happens internally with this single statement:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NAIVE ALTER TABLE TIMELINE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. ACCESS EXCLUSIVE LOCK acquired on `orders`                      │
│     ├── ALL reads blocked  ❌                                       │
│     ├── ALL writes blocked ❌                                       │
│     └── ALL queries queue up behind the lock                        │
│                                                                     │
│  2. PostgreSQL rewrites EVERY row (pre-v11 behavior)                │
│     ├── 50,000,000 rows × ~200 bytes = ~10 GB rewrite              │
│     ├── Estimated time: 5–30 minutes depending on hardware          │
│     └── WAL generation: potentially 2–3× table size                 │
│                                                                     │
│  3. Indexes rebuilt                                                  │
│     └── Additional time proportional to index count                 │
│                                                                     │
│  4. Lock released                                                   │
│                                                                     │
│  Total downtime: MINUTES TO HOURS                                   │
│                                                                     │
│  PostgreSQL 11+ Improvement:                                        │
│  ─────────────────────────────────────────────────────────────────  │
│  ADD COLUMN ... DEFAULT (...
```

### Gemini 3.1 Pro

**Generation Time:** 34201ms
**Tokens:** 2104

```
Adding a `NOT NULL` column with a default value to a 50-million-row table is a classic database engineering challenge. How you solve it depends entirely on your PostgreSQL version and whether the default value is **constant** (e.g., `'active'`) or **volatile** (e.g., `gen_random_uuid()`).

Here is the comprehensive guide to doing this with zero downtime, why the naive approach fails, and how to verify the results.

---

### Why Naive `ALTER TABLE` Fails at Scale

The naive approach looks like this:
```sql
ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active';
```

If you run this on a busy 50-million-row table, you will likely cause an outage. Here is why:

1. **The Table Rewrite (Pre-PG 11 or Volatile Defaults):** Prior to PostgreSQL 11, or if your default value is volatile (like `NOW()`), Postgres must physically rewrite the entire table. It locks the table with an `ACCESS EXCLUSIVE` lock, writes 50 million new rows, updates all indexes, and blocks **all reads and writes** until it finishes. This means minutes or hours of downtime.
2. **The Lock Queue of Death (Even in PG 11+):** PostgreSQL 11 introduced a massive optimization: adding a column with a *constant* default no longer rewrites the table. It just updates metadata. **However**, it still requires a brief `ACCESS EXCLUSIVE` lock. If there is a long-running `SELECT` query on the table, the `ALTER TABLE` must wait for it to finish. While it waits, it blocks *every subsequent query* behind it. Your application will instantly hit connection limits and crash.

---

### The Zero-Downtime Migration Process

I will provide two paths. **Path A** is for modern Postgres with a constant default. **Path B** is the universal "bulletproof" method required for volatile defaults or older Postgres versions.

#### Path A: PostgreSQL 11+ with a CONSTANT Default
If you are on PG 11+ and your default is a static value (e.g., `0`, `false`, `'pending'`), Postgres can do this instantly via metadata. You just nee...
```

### Claude Sonnet 4.6

**Generation Time:** 33962ms
**Tokens:** 2118

```
# Zero-Downtime Column Addition in PostgreSQL at Scale

## Why the Naive Approach Fails

```sql
-- ❌ NEVER DO THIS ON A LARGE TABLE IN PRODUCTION
ALTER TABLE orders ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending';
```

### What Actually Happens Internally

```
Timeline of naive ALTER TABLE on 50M row table:
─────────────────────────────────────────────────────────────────────────────
T+0s    │ AccessExclusiveLock acquired (blocks ALL reads AND writes)
T+0s    │ Table rewrite begins (PostgreSQL < 11 rewrites entire table)
T+???   │ Every row physically updated with new default value
        │ ├── 50M rows × ~100 bytes avg = ~5GB table rewrite
        │ ├── WAL generated for every row (replication lag spikes)
        │ └── Disk I/O saturated
T+180s  │ Index rebuilds on new table copy
T+240s  │ Lock released — application was DOWN for 4+ minutes
─────────────────────────────────────────────────────────────────────────────

PostgreSQL 11+ improvement: Stores constant defaults in catalog (no rewrite)
BUT: NOT NULL constraint still requires table scan to verify
AND: Lock is still held during that scan
```

---

## The Safe Migration Strategy

### Overview: Three-Phase Approach

```
Phase 1: Add nullable column (instant, no lock)
Phase 2: Backfill data in small batches (online, no lock)
Phase 3: Add NOT NULL constraint safely (minimal lock)
```

---

## Phase 1: Add Nullable Column with Default

```sql
-- ✅ This is INSTANT in PostgreSQL 11+ (catalog-only change)
-- Even in older versions, adding nullable column is very fast
ALTER TABLE orders 
    ADD COLUMN status VARCHAR(50) DEFAULT 'pending';

-- Why this works:
-- 1. No table rewrite needed
-- 2. Lock held only for milliseconds (catalog update)
-- 3. Existing rows return 'pending' via catalog default
-- 4. New inserts automatically get 'pending'
```

```sql
-- Verify the column was added correctly
SELECT 
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE ...
```

### Grok 4.20

**Generation Time:** 6219ms
**Tokens:** 1486

```
**Safe Zero-Downtime Migration for Adding a `NOT NULL` Column with Default to a 50M-row Table in PostgreSQL**

### Why the naive approach fails at scale

```sql
ALTER TABLE large_table 
ADD COLUMN new_col text NOT NULL DEFAULT 'something';
```

This single statement does the following **while holding an `ACCESS EXCLUSIVE` lock** (the strongest lock):

1. Rewrites the entire table (all 50M rows) to add the new column.
2. Updates every row with the default value.
3. Adds the `NOT NULL` constraint.

On a 50M-row table this can take **many minutes to hours**, blocking all reads and writes. Even with `DEFAULT`, PostgreSQL still needs to physically write the value for the `NOT NULL` constraint in the old row versions.

### The safe, zero-downtime strategy (PostgreSQL 11+)

We use the **"add column as nullable → backfill → add constraint"** pattern with minimal locking.

#### Step-by-step migration

**1. Add the column as nullable (very fast)**

```sql
-- This is almost instantaneous even on 50M rows
ALTER TABLE large_table 
ADD COLUMN new_col text;   -- nullable, no default yet
```

This only changes the table metadata.

**2. Add a default (still cheap)**

```sql
ALTER TABLE large_table 
ALTER COLUMN new_col 
SET DEFAULT 'something';
```

Existing rows are **not** updated — they will return the default on `SELECT` thanks to the `DEFAULT` mechanism.

**3. Backfill in small batches (the real work)**

Create a function that updates in tiny, non-locking batches:

```sql
CREATE OR REPLACE FUNCTION backfill_new_col(batch_size int DEFAULT 10000)
RETURNS void AS $$
DECLARE
    rows_updated int := batch_size;
BEGIN
    WHILE rows_updated = batch_size LOOP
        UPDATE large_table 
        SET new_col = COALESCE(new_col, 'something')
        WHERE new_col IS NULL
          AND id >= (SELECT COALESCE(MAX(id), 0) 
                     FROM large_table 
                     WHERE new_col IS NOT NULL)
        LIMIT batch_size;

        GET DIAGNOSTICS rows_updated = ROW_COUNT;
      ...
```

### DeepSeek V3

**Generation Time:** 20199ms
**Tokens:** 864

```
# PostgreSQL Migration: Adding a NOT NULL Column with Default to a Large Table

## Problem Overview

When adding a NOT NULL column with a default value to a table with 50 million rows in PostgreSQL, a naive `ALTER TABLE` approach can cause significant downtime because:
1. It locks the table for the duration of the operation
2. It immediately updates all rows to set the default value
3. At scale, this operation can take hours or longer

## Safe Migration Process

Here's a step-by-step approach to add the column without downtime:

### 1. Add the Column as NULLable First

```sql
ALTER TABLE large_table ADD COLUMN new_column INTEGER NULL;
```

This is instantaneous as it just updates the table metadata without touching existing rows.

### 2. Update Existing Rows in Batches

```sql
-- First batch
UPDATE large_table SET new_column = 42 WHERE id BETWEEN 1 AND 1000000 AND new_column IS NULL;

-- Subsequent batches (run in separate transactions)
UPDATE large_table SET new_column = 42 WHERE id BETWEEN 1000001 AND 2000000 AND new_column IS NULL;
-- Continue until all rows are processed
```

Use application logic or a script to manage these batched updates. Consider:
- Using the primary key for efficient range queries
- Adding appropriate `WHERE` conditions to avoid re-processing
- Pausing between batches to reduce system load

### 3. Add a Default Value Constraint

```sql
ALTER TABLE large_table ALTER COLUMN new_column SET DEFAULT 42;
```

This doesn't modify existing rows, just sets the default for future INSERTs.

### 4. Create a Check Constraint for Data Integrity

```sql
ALTER TABLE large_table ADD CONSTRAINT new_column_not_null CHECK (new_column IS NOT NULL) NOT VALID;
```

The `NOT VALID` option means existing rows aren't checked immediately.

### 5. Validate the Check Constraint

```sql
ALTER TABLE large_table VALIDATE CONSTRAINT new_column_not_null;
```

This verifies all rows comply with the constraint without locking the table.

### 6. Convert to NOT NULL

```sql
ALT...
```

### GPT-OSS-120B

**Generation Time:** 133012ms
**Tokens:** 3931

```
## TL;DR  

**Goal:** Add a new column `status` (type `text`) to a 50‑million‑row table `orders` that must be **NOT NULL** and have a **default value** (`'new'`) – without blocking reads/writes for any noticeable amount of time.

**Result:** A series of small, non‑blocking statements that can be run as a single migration (e.g., with Flyway, Liquibase, Rails, Alembic, etc.):

```sql
-- 1. Add the column as nullable, with a “stored‑only” default (metadata‑only)
ALTER TABLE orders
    ADD COLUMN status text NOT NULL DEFAULT 'new';

-- 2. Back‑fill the column for the rows that existed before the ALTER.
--    Do it in batches so that each transaction finishes quickly.
DO $$
DECLARE
    batch_size   integer := 100_000;          -- tune to your workload
    rows_updated integer;
BEGIN
    LOOP
        UPDATE orders
        SET    status = 'new'
        WHERE  status IS NULL               -- rows that still need the value
        LIMIT  batch_size
        RETURNING 1 INTO rows_updated;     -- any row means we updated something

        IF NOT FOUND THEN
            EXIT;                          -- no more rows to update
        END IF;

        -- Give the planner a chance to release locks and let other traffic in
        PERFORM pg_sleep(0.05);            -- 50 ms pause (optional)
    END LOOP;
END $$;

-- 3. Verify that every row now has a non‑null value (quick check)
SELECT count(*) AS rows_missing
FROM   orders
WHERE  status IS NULL;   -- should return 0

-- 4. (Optional) Add a CHECK constraint that the column is NOT NULL *and* a
--    known enum, and mark it NOT VALID first so it does not block.
ALTER TABLE orders
    ADD CONSTRAINT orders_status_chk
        CHECK (status IN ('new','processing','shipped','canceled'))
        NOT VALID;

-- 5. Validate the constraint – this is the only moment when PostgreSQL
--    scans the whole table, but it happens after the back‑fill, so it is
--    guaranteed to succeed quickly.
ALTER TABLE orders VALIDATE CONSTRAINT orders_status...
```

### Gemini 3 Flash Preview

**Generation Time:** 8297ms
**Tokens:** 1177

```
To migrate a table with 50 million rows in PostgreSQL without causing downtime, you must avoid **Access Exclusive** locks that last longer than a few milliseconds.

### The Problem: Why Naive `ALTER TABLE` Fails
A naive migration looks like this:
```sql
ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';
```
**Why this fails at scale:**
1. **The Rewrite (Pre-Postgres 11):** Older versions would rewrite the entire 50M row table to add the value to every row, locking it for minutes.
2. **The Metadata Lock (Postgres 11+):** While Postgres 11+ optimizes this by storing the default in the catalog (avoiding a rewrite), the command still requires an `Access Exclusive` lock to update the table schema. If there are long-running queries or high traffic, this command will sit in a queue, blocking all subsequent reads and writes until it acquires the lock.

---

### The Zero-Downtime Strategy
To ensure safety, we break the migration into three distinct, low-impact steps.

#### Step 1: Add the column as Nullable (with a lock timeout)
We add the column without the `NOT NULL` constraint and without the `DEFAULT` clause initially. This makes the operation near-instant.

```sql
-- Set a short lock timeout so we don't block the site if we can't get a lock
SET lock_timeout = '2s';

ALTER TABLE orders ADD COLUMN status TEXT;
```

#### Step 2: Set the Default for new rows
Now, we set the default value. This only affects **new** rows inserted after this command. It does not touch existing data.

```sql
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';
```

#### Step 3: Backfill existing rows in batches
Updating 50 million rows in one transaction will bloat the table, exhaust memory, and potentially lock the table. We must update in small batches (e.g., 10,000 rows) with a small sleep (`pg_sleep`) between batches to allow the autovacuum to clean up dead tuples.

**Pseudo-code for a script (Python/Node/Bash):**
```sql
-- Repeat this until rows affected is 0
UP...
```

### MiniMax M2.5

**Generation Time:** 39139ms
**Tokens:** 2144

```

```

### MiMo-V2-Flash

**Generation Time:** 18282ms
**Tokens:** 2006

```
This is a classic database operations challenge. A naive `ALTER TABLE` on a table with 50 million rows can lock the table for minutes or even hours, blocking all reads and writes (downtime).

Here is the step-by-step migration strategy using a "shadow column" technique to achieve zero downtime.

### The Scenario
*   **Table:** `users`
*   **Existing Rows:** 50 million
*   **New Column:** `status` (Type: `VARCHAR`, Default: `'active'`, NOT NULL)

---

### Why Naive `ALTER TABLE` Fails
When you run a standard command like:
```sql
ALTER TABLE users ADD COLUMN status VARCHAR NOT NULL DEFAULT 'active';
```
PostgreSQL (prior to version 11) had to rewrite the entire table. Even in newer versions, adding a column with a static default value is usually instantaneous (because it only writes the default to the metadata), **BUT** adding a `NOT NULL` constraint requires a table scan.

1.  **The Lock:** To ensure the column is never `NULL`, PostgreSQL must scan all 50 million rows to verify the constraint.
2.  **The Blocking:** During this scan, the table is locked in `ACCESS EXCLUSIVE` mode. No `SELECT`, `INSERT`, `UPDATE`, or `DELETE` operations can occur.
3.  **The Consequence:** If the table is large (50M rows), the scan takes a long time. Your application times out, and users see errors.

---

### The Zero-Downtime Migration Strategy

We will use a multi-step process that splits the operation into small, non-blocking chunks.

#### Step 1: Add the Column (Nullable)
First, we add the column allowing `NULL` values. This is a metadata-only operation (instant) and does not lock the table.

```sql
ALTER TABLE users ADD COLUMN status VARCHAR;
```
*   **Why:** Postgres doesn't need to rewrite the table for existing rows; they simply get a `NULL` value for this new column.

#### Step 2: Backfill in Batches (Critical for Scale)
We cannot update 50 million rows at once; that would generate a massive WAL (Write Ahead Log) and hold a lock for the duration of the transaction. We update in...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*