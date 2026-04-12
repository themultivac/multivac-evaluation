# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-142215
**Timestamp:** 2026-04-02T14:22:15.794045
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Write a database migration that adds a NOT NULL column with a default value to a table with 50 million rows in PostgreSQL — without locking the table or causing downtime. Explain the step-by-step process, why naive ALTER TABLE fails at scale, and how to verify data integrity after migration.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 8.79 | 6.00 | 10.00 | 1.14 |
| 2 | Grok 4.20 | 8.40 | 5.40 | 9.60 | 1.31 |
| 3 | Gemini 3 Flash Preview | 8.27 | 6.70 | 9.60 | 0.82 |
| 4 | Claude Sonnet 4.6 | 8.08 | 5.65 | 10.00 | 1.61 |
| 5 | MiMo-V2-Flash | 7.96 | 6.05 | 9.60 | 1.25 |
| 6 | Claude Opus 4.6 | 7.74 | 4.45 | 10.00 | 1.99 |
| 7 | GPT-OSS-120B | 7.39 | 3.55 | 9.35 | 1.90 |
| 8 | DeepSeek V3 | 6.95 | 4.15 | 8.60 | 1.45 |
| 9 | Gemini 3.1 Pro | 6.66 | 4.35 | 8.80 | 1.49 |
| None | MiniMax M2.5 | 6.76 | 0.50 | 9.35 | 4.19 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Gemini 3.1 Pro | 5.42 |
| 2 | GPT-5.4 | 5.99 |
| 3 | Claude Opus 4.6 | 6.56 |
| 4 | Grok 4.20 | 7.81 |
| 5 | MiniMax M2.5 | 7.86 |
| 6 | GPT-OSS-120B | 7.98 |
| 7 | Claude Sonnet 4.6 | 8.12 |
| 8 | MiMo-V2-Flash | 8.94 |
| 9 | Gemini 3 Flash Preview | 9.09 |
| 10 | DeepSeek V3 | 9.44 |

**Strictest Judge:** gemini_31_pro
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

**Generation Time:** 32996ms
**Tokens:** 2112

```
Here’s the safe, production-grade way to add a `NOT NULL` column with a default to a very large PostgreSQL table.

---

# Goal

Add a new column to a table with **50 million rows** such that:

- existing traffic keeps working
- no long blocking lock or downtime
- all rows eventually have a value
- column becomes `NOT NULL`
- future inserts get the default automatically

---

# Why the naive approach is dangerous

A naive migration looks like this:

```sql
ALTER TABLE big_table
ADD COLUMN status text NOT NULL DEFAULT 'active';
```

At scale, this can be a problem because historically this may:

- force a **table rewrite** on some PostgreSQL versions / scenarios
- hold an **ACCESS EXCLUSIVE lock**
- block reads/writes while the schema change is applied
- generate huge WAL
- cause replication lag
- take a very long time on 50M rows

Even on newer PostgreSQL versions where `ADD COLUMN ... DEFAULT <constant>` is optimized, combining everything into one statement still means:

- you still take a lock for the DDL
- setting `NOT NULL` can require validation work
- operationally it is safer to split the migration into phases
- app rollout is easier when schema and backfill are decoupled

So at scale, the safe pattern is:

1. add column as nullable
2. set default for new rows
3. backfill old rows in batches
4. enforce constraint safely
5. optionally convert to `NOT NULL`

---

# Safe migration strategy

Assume:

- table: `orders`
- new column: `status`
- type: `text`
- default: `'active'`

---

## Step 1: Add the column as nullable

This is fast because PostgreSQL only updates metadata.

```sql
ALTER TABLE orders ADD COLUMN status text;
```

### Lock behavior
This still takes a brief `ACCESS EXCLUSIVE` lock, but only for metadata change. If executed carefully, it should be very short.

### Important
Run this during a normal deployment window, but it should not require downtime.

---

## Step 2: Set the default for future inserts

```sql
ALTER TABLE orders ALTER COLUMN status ...
```

### Claude Opus 4.6

**Generation Time:** 253787ms
**Tokens:** 2119

```
# Zero-Downtime Migration: Adding a NOT NULL Column at Scale in PostgreSQL

## Why Naive `ALTER TABLE` Fails at Scale

```sql
-- ❌ THIS WILL LOCK YOUR TABLE FOR HOURS ON 50M ROWS
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';
```

### What happens internally with the naive approach:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NAIVE ALTER TABLE TIMELINE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. ACCESS EXCLUSIVE LOCK acquired on table                         │
│     ├── ALL reads blocked  ❌                                       │
│     ├── ALL writes blocked ❌                                       │
│     └── ALL queries queue up behind the lock                        │
│                                                                     │
│  2. PostgreSQL rewrites EVERY row (pre-PG11 for volatile defaults)  │
│     ├── 50,000,000 rows × ~200 bytes = ~10GB rewrite               │
│     ├── Generates WAL logs (doubles I/O)                            │
│     └── Duration: 30 min to several hours                           │
│                                                                     │
│  3. Indexes rebuilt                                                  │
│     └── Additional time proportional to index count                 │
│                                                                     │
│  4. Lock released                                                   │
│     └── Queued queries stampede the server                          │
│                                                                     │
│  TOTAL DOWNTIME: 30 minutes to hours                                │
└─────────────────────────────────────────────────────────────────────┘
```

### PostgreSQL Version Nuances

```
┌─────────────────────────────────────────────────────────...
```

### Gemini 3.1 Pro

**Generation Time:** 34985ms
**Tokens:** 2104

```
To safely add a `NOT NULL` column with a default value to a 50-million-row PostgreSQL table without downtime, the approach depends entirely on your PostgreSQL version and whether the default value is a **constant** (e.g., `0`, `'active'`) or **volatile** (e.g., `gen_random_uuid()`, `NOW()`).

Here is the complete guide, starting with a crucial modern caveat, followed by the universal zero-downtime strategy, the explanation of locks, and verification steps.

---

### The Modern PostgreSQL Caveat (PG 11+)
If you are using **PostgreSQL 11 or newer**, and your default value is a **constant** (not a volatile function), PostgreSQL includes a massive optimization. You can actually run the naive command:

```sql
-- THIS IS SAFE in PG 11+ IF the default is a constant.
ALTER TABLE users ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'active';
```
In PG 11+, this does **not** rewrite the table. It simply updates the system catalog and dynamically injects the default value when rows are read. It takes milliseconds.

**However, you MUST use the multi-step strategy below if:**
1. You are on PostgreSQL 10 or older.
2. Your default value is volatile (e.g., `uuid_generate_v4()`).
3. Your default value depends on other columns in the table.

---

### Why the Naive `ALTER TABLE` Fails at Scale
If you run `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT ...` on an older version of PG or with a volatile default, PostgreSQL must physically write the new value to every single row on disk. 

Because of PostgreSQL's MVCC (Multi-Version Concurrency Control) architecture, it doesn't just update the rows in place; **it rew
```

### Claude Sonnet 4.6

**Generation Time:** 31984ms
**Tokens:** 2119

```
# Zero-Downtime Column Addition in PostgreSQL at Scale

## Why Naive ALTER TABLE Fails

```sql
-- ❌ THIS WILL CAUSE DOWNTIME AT SCALE
ALTER TABLE orders ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending';
```

### What Actually Happens Internally

```
Timeline of naive ALTER TABLE on 50M row table:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

T=0s    ┌─ ACCESS EXCLUSIVE LOCK acquired
        │  (blocks ALL reads AND writes)
        │
T=0s    ├─ PostgreSQL rewrites ENTIRE table
        │  50M rows × avg row size = massive I/O
        │  Estimated time: 10-45 minutes
        │
T=?min  ├─ Table statistics updated
        │
T=?min  └─ Lock released

During this window:
  ✗ SELECT queries → wait or timeout
  ✗ INSERT/UPDATE/DELETE → wait or timeout  
  ✗ Application → degraded/down
  ✗ Connection pool → exhausted
  ✗ Cascading failures → likely
```

### PostgreSQL Version Context

```sql
-- PostgreSQL 11+ changed behavior for ADD COLUMN with constant defaults
-- Understanding the difference is CRITICAL

-- PostgreSQL < 11:  Always rewrites table (dangerous at scale)
-- PostgreSQL >= 11: Constant defaults stored in catalog, no rewrite needed
--                   BUT: NOT NULL still causes full table scan for validation

SELECT version(); -- Know your version before proceeding
```

---

## The Safe Migration Strategy

```
Strategy Overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Add column as NULLABLE (no lock, no rewrite)
Step 2: Add DEFAULT value to column definition  
Step 3: Backfill existing rows in small batches
Step 4: Add NOT NULL constraint as NOT VALID
Step 5: Validate constraint (doesn't block reads/writes)
Step 6: Clean up
```

---

## Complete Migration Implementation

### Step 1: Add Column as Nullable Without Default

```sql
-- ✅ SAFE: No table rewrite, minimal lock duration (milliseconds)
-- Lock type: ACCESS EXCLUSIVE but held for microseconds only
ALTER TABLE orders ADD COLUMN statu...
```

### Grok 4.20

**Generation Time:** 12613ms
**Tokens:** 1347

```
**✅ Safe Zero-Downtime Migration for Adding a `NOT NULL` Column with Default on a 50M-row Table**

### Why the naive approach fails at scale

```sql
ALTER TABLE orders ADD COLUMN status text NOT NULL DEFAULT 'pending';
```

This single statement does the following **while holding an `ACCESS EXCLUSIVE` lock**:

1. Rewrites the entire table (50M rows) to add the new column.
2. Updates every row with the default value.
3. Adds the `NOT NULL` constraint.

On a 50M-row table this can take **minutes to hours**, blocking all reads and writes. The table is completely unavailable during that time.

---

### Correct Zero-Downtime Strategy (PostgreSQL 11+)

We break it into **five safe, low-impact steps**:

#### Step 1: Add the column as nullable (instant)

```sql
ALTER TABLE orders 
  ADD COLUMN status text;
```

This is metadata-only in PostgreSQL ≥ 11. No table rewrite, almost no lock.

#### Step 2: Set a default (still cheap)

```sql
ALTER TABLE orders 
  ALTER COLUMN status SET DEFAULT 'pending';
```

Existing rows are **not** updated — the default only applies to future `INSERT`s. This is also very fast.

#### Step 3: Backfill the existing rows in batches (with minimal locking)

Use a script or `pg_background` / `pg_cron` / application-level worker:

```sql
DO $$
DECLARE
    batch_size integer := 10000;
    rows_updated integer;
BEGIN
    LOOP
        UPDATE orders 
        SET status = 'pending'
        WHERE status IS NULL
        LIMIT batch_size;

        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        EXIT WHEN rows_updated = 0;

        -- Very important: yield to other transactions
        PERFORM pg_sleep(0.01);  -- 10ms pause
    END LOOP;
END $$;
```

**Better version** (even less locking):

```sql
-- Run this in a loop from an external script
WITH batch AS (
    SELECT ctid 
    FROM orders 
    WHERE status IS NULL 
    LIMIT 10000
    FOR UPDATE SKIP LOCKED
)
UPDATE orders o
SET status = 'pending'
FROM batch b
WHERE o.ctid = b.ctid;
```

Use `SKIP LOCKED` ...
```

### DeepSeek V3

**Generation Time:** 22475ms
**Tokens:** 834

```
# Database Migration for Adding a NOT NULL Column with Default to a Large Table

## The Challenge

Adding a `NOT NULL` column with a default value to a table with 50 million rows in PostgreSQL requires careful planning to avoid locking the table for extended periods or causing downtime.

## Why Naive ALTER TABLE Fails at Scale

A simple `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT ...` has several problems with large tables:

1. **Long Lock Time**: PostgreSQL needs to rewrite all rows to add the new column, which can take hours on large tables.
2. **Blocking Operations**: The table is locked in an `ACCESS EXCLUSIVE` mode, blocking all reads and writes.
3. **Transaction Log Growth**: The operation generates significant WAL (Write-Ahead Log) volume.
4. **Performance Impact**: Heavy I/O load affects database performance.

## Step-by-Step Safe Migration Process

### 1. First Migration: Add the Column as NULLABLE
```sql
ALTER TABLE large_table ADD COLUMN new_column INTEGER;
```

This is instantaneous as it just updates the catalog. No rows are rewritten.

### 2. Second Migration: Add Default Value in Batches
Use a batched approach to update existing rows:

```sql
DO $$
DECLARE
  batch_size INTEGER := 10000;
  max_id INTEGER;
  min_id INTEGER := 0;
BEGIN
  SELECT MAX(id) INTO max_id FROM large_table;
  
  WHILE min_id <= max_id LOOP
    UPDATE large_table
    SET new_column = 0  -- Your default value
    WHERE id > min_id AND id <= min_id + batch_size
    AND new_column IS NULL;
    
    min_id := min_id + batch_size;
    COMMIT;
    
    -- Optional: Add a small delay to reduce load
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;
```

### 3. Third Migration: Add NOT NULL Constraint
Once all rows are populated:

```sql
ALTER TABLE large_table ALTER COLUMN new_column SET NOT NULL;
```

This is now safe because all existing rows have values.

### 4. Fourth Migration: Add Default Value to Column Definition
```sql
ALTER TABLE large_table ALTER COLUMN new_column SET DEFAULT 0;
...
```

### GPT-OSS-120B

**Generation Time:** 4872ms
**Tokens:** 2173

```
## TL;DR  

| Step | What you do | Why it works (no full‑table rewrite, no long‑lasting lock) |
|------|-------------|------------------------------------------------------------|
| 1️⃣  | **Add the column as nullable** (no default). | Only a *metadata* change → an `ACCESS EXCLUSIVE` lock is taken for a few milliseconds; the 50 M rows are untouched. |
| 2️⃣  | **Back‑fill the column in small batches** (`UPDATE … WHERE col IS NULL LIMIT N`). | Each batch runs in its own transaction, holds only a `ROW EXCLUSIVE` lock, and touches a few thousand rows at a time – the table stays online for reads and writes. |
| 3️⃣  | **Add the NOT‑NULL constraint** (`ALTER TABLE … ALTER COLUMN … SET NOT NULL`). | The column is already populated, so PostgreSQL only needs to *validate* the existing rows (a fast scan) and then releases the lock. |
| 4️⃣  | **Set the default for future inserts** (`ALTER TABLE … ALTER COLUMN … SET DEFAULT …`). | Again a pure metadata change – no data rewrite, no lock beyond a brief `ACCESS EXCLUSIVE`. |
| 5️⃣  | **(Optional) Add indexes concurrently** if you need them. | `CREATE INDEX CONCURRENTLY` never blocks writes. |

The whole migration can be run on a production system with **zero downtime** and **no long‑lasting exclusive lock**.

---

## 1. Why the naïve `ALTER TABLE … ADD COLUMN … NOT NULL DEFAULT …` blows up on a 50 M‑row table

```sql
ALTER TABLE big_table ADD COLUMN new_col text NOT NULL DEFAULT 'foo';
```

* **What PostgreSQL does**  
  * From PG 11 onward the **default value** is stored only in the system catalog – the table is *not* rewritten.  
  * The **`NOT NULL`** clause, however, forces PostgreSQL to **scan every row** to verify that the constraint holds.  
  * To guarantee a consistent view while scanning, PostgreSQL upgrades the lock to **`ACCESS EXCLUSIVE`** for the whole duration of the scan.

* **Consequences on a 50 M‑row table**  
  * The scan can take minutes (or hours) depending on I/O, CPU and row size.  
  * While the lock is ...
```

### Gemini 3 Flash Preview

**Generation Time:** 12628ms
**Tokens:** 1241

```
To migrate a table with 50 million rows in PostgreSQL, a naive approach can be catastrophic. Even though modern PostgreSQL versions (11+) have optimized `ADD COLUMN ... DEFAULT`, adding a `NOT NULL` constraint still requires a full table scan to validate existing rows, which can hold an `ACCESS EXCLUSIVE` lock for minutes, blocking all reads and writes.

Here is the zero-downtime strategy.

---

### Step 1: Add the column as Nullable
First, we add the column without the `NOT NULL` constraint. In PostgreSQL 11+, adding a column with a constant default value is a metadata-only change and is nearly instantaneous.

```sql
-- Transaction 1
ALTER TABLE users ADD COLUMN country_code TEXT DEFAULT 'US';
```
*   **Why:** This adds the column but does not immediately check existing rows for nulls, preventing a long-held lock.

### Step 2: Set the Default for new rows
If you didn't include the default in Step 1, set it now. This ensures that any **new** rows inserted from this point forward will have the value.

```sql
-- Transaction 2
ALTER TABLE users ALTER COLUMN country_code SET DEFAULT 'US';
```

### Step 3: Backfill existing data in batches
Even if you used a `DEFAULT` in Step 1, some rows might have been created as `NULL` during the split-second migration, or you may be adding a column to an older Postgres version. We update existing rows in small batches to avoid long-running transactions that bloat the table and bloat the WAL.

**Do not use one big UPDATE statement.** Use a script (Python, Ruby, or a PL/pgSQL loop):

```sql
-- Run this repeatedly until 0 rows are updated
UPDATE users 
SET country_code = 'US' 
WHERE id IN (
    SELECT id FROM users 
    WHERE country_code IS NULL 
    LIMIT 10000
);
-- COMMIT after every batch;
-- VACUUM ANALYZE users; (Optional, to clean up dead tuples)
```

### Step 4: Add the NOT NULL constraint "Invisibly"
Now we need to enforce the constraint. We add it as `NOT VALID`. This tells Postgres: "Enforce this for all new writes, but don'...
```

### MiniMax M2.5

**Generation Time:** 0ms
**Tokens:** 0

```

```

### MiMo-V2-Flash

**Generation Time:** 18906ms
**Tokens:** 2143

```
Here is a comprehensive guide to adding a `NOT NULL` column with a default value to a large PostgreSQL table (50M+ rows) without locking the table or causing downtime.

---

### The Problem: Why Naive `ALTER TABLE` Fails

If you run a standard SQL command like this:

```sql
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;
```

**What happens internally:**
1.  **Exclusive Lock:** PostgreSQL needs to modify the table definition in the system catalogs (pg_attribute, pg_class).
2.  **Full Table Rewrite:** In older PostgreSQL versions (< 11), adding a column with a default value required rewriting the entire table to physically insert the default value into every existing row. Even in PostgreSQL 11+, if the default is volatile (e.g., `random()`) or if the column is `NOT NULL` without a default, it requires a rewrite.
3.  **The Lock:** To perform these operations safely, PostgreSQL takes an `ACCESS EXCLUSIVE` lock. This blocks **all** operations (reads, writes, updates, deletes) on that table until the command finishes.

**At Scale (50M rows):**
*   A rewrite can take hours depending on hardware and row size.
*   During this time, your application is effectively down (timeouts, hung requests).
*   Replication lag will spike on standby servers.

---

### The Solution: The Split-Strategy Migration

To avoid locks and downtime, we use a multi-step approach that leverages PostgreSQL's ability to add an un-validated `NOT NULL` constraint and backfill data in small batches.

**Prerequisites:**
*   PostgreSQL 11+ (for efficient `ALTER TABLE ... ADD COLUMN` without a rewrite).
*   Sufficient disk space (you need space for the new column and a temporary table during validation).

#### Step-by-Step Migration Process

We will assume the table is named `users` and we are adding `is_active BOOLEAN DEFAULT TRUE`.

#### Step 1: Add the Column (Nullable)
First, add the column allowing `NULL` values. This is an metadata-only operation (fast) and does not lock existing...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*