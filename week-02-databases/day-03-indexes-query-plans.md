# Day 3 — Indexes & Query Plans: Make Reads Fast Without Taxing Every Write

## Goal

Choose indexes from real queries, understand their costs, and use PostgreSQL's planner output to test your assumptions.

## Timebox

- 15 min — what an index buys/costs
- 20 min — B-tree, composite, partial, GIN/BRIN
- 20 min — `EXPLAIN` / `EXPLAIN ANALYZE`
- 20 min — transcription index lab
- 10 min — retrieval quiz

---

# 1. An index is an extra data structure

Without an index, PostgreSQL may scan many/all rows.

```text
Table
[1][2][3][4][5][6] ... [10,000,000]
```

An index creates a structure that helps locate matching rows efficiently.

```text
Index lookup
     ↓
matching row locations
     ↓
Table rows
```

This can make reads much faster.

But indexes cost:

- disk space,
- memory/cache pressure,
- extra work on INSERT,
- extra work on UPDATE,
- extra work on DELETE,
- maintenance.

So:

> "Add indexes to everything" is not a performance strategy.

---

# 2. Design indexes from queries

Suppose your app runs:

```sql
SELECT *
FROM jobs
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

A useful index candidate is:

```sql
CREATE INDEX idx_jobs_user_created
ON jobs (user_id, created_at DESC);
```

Why?

Because the index matches the filter prefix and desired ordering.

This is stronger reasoning than:

> "We index `created_at` because sorting is slow."

---

# 3. B-tree: your default workhorse

PostgreSQL B-tree indexes are useful for common operations such as:

```text
=
<
>
BETWEEN
ORDER BY
prefix combinations in multicolumn indexes
```

Typical examples:

```sql
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
```

Most Week 2 indexing decisions should start with B-tree.

---

# 4. Composite indexes

```sql
CREATE INDEX idx_chunks_job_index
ON chunks(job_id, chunk_index);
```

This is excellent for:

```sql
WHERE job_id = $1
ORDER BY chunk_index
```

But column order matters.

The same index may not efficiently satisfy every query on `chunk_index` alone.

Think of a composite index as optimized for a family of access patterns—not as two independent indexes glued together.

---

# 5. Unique indexes and constraints

A uniqueness constraint is about correctness:

```sql
UNIQUE (job_id, chunk_index)
```

It also creates an index that supports enforcing that uniqueness.

This is a nice example where:

```text
correctness requirement
       ↓
constraint
       ↓
index side effect
```

Don't reverse the reasoning and treat a correctness constraint only as a performance feature.

---

# 6. Partial indexes

Suppose 99% of jobs are completed, but your scheduler constantly queries active jobs:

```sql
SELECT *
FROM jobs
WHERE status IN ('queued', 'processing');
```

A partial index can index only the subset:

```sql
CREATE INDEX idx_jobs_active
ON jobs(created_at)
WHERE status IN ('queued', 'processing');
```

Possible benefits:

- smaller index,
- less maintenance than indexing every row,
- good match for a selective operational query.

But only if the workload actually uses it.

---

# 7. GIN and JSONB

If provider metadata is stored in `jsonb` and you genuinely query inside it:

```sql
SELECT *
FROM jobs
WHERE provider_metadata @> '{"language":"fr"}';
```

A GIN index may be useful.

```sql
CREATE INDEX idx_jobs_metadata_gin
ON jobs USING GIN(provider_metadata);
```

Again: index the query you have, not hypothetical flexibility.

---

# 8. BRIN for very large naturally ordered tables

BRIN indexes summarize ranges of physical table pages.

They can be tiny and useful for huge tables where values correlate with physical order, such as append-only timestamped events.

Potential future example:

```text
500M audit rows ordered roughly by created_at
```

Not usually your first index for a small SaaS database.

---

# 9. `EXPLAIN` tells you the plan

```sql
EXPLAIN
SELECT * FROM jobs WHERE user_id = '...';
```

You may see:

```text
Seq Scan
Index Scan
Bitmap Index Scan
Nested Loop
Hash Join
```

The planner chooses a plan based on:

- table statistics,
- estimated row counts,
- indexes,
- data distribution,
- cost model.

---

# 10. `EXPLAIN ANALYZE` executes the query

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM jobs
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

Look for:

```text
estimated rows vs actual rows
planning time
execution time
scan type
loops
buffer hits / reads
```

If estimates are wildly wrong, the planner may make poor choices.

Important:

`EXPLAIN ANALYZE` **actually executes** the statement.

Be careful with writes.

---

# 11. Indexes can make performance worse

Imagine a `chunks` table receiving thousands of writes per minute.

You add indexes on:

```text
job_id
chunk_index
status
start_ms
end_ms
provider
language
created_at
updated_at
```

Every insert/update now maintains many index structures.

Ask:

> Which queries justify each index?

A useful index should have an owner: a known access pattern.

---

# Lab — Index the transcription workload

Start with these queries.

### Query A — job history

```sql
SELECT id, status, progress, created_at
FROM jobs
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

### Query B — chunk merge

```sql
SELECT chunk_index, start_ms, end_ms, text
FROM chunks
WHERE job_id = $1
ORDER BY chunk_index;
```

### Query C — unfinished jobs

```sql
SELECT id
FROM jobs
WHERE status IN ('queued', 'processing')
ORDER BY created_at;
```

### Query D — upload dedup lookup

```sql
SELECT id
FROM uploads
WHERE user_id = $1
  AND content_hash = $2;
```

For each:

1. Propose an index.
2. Explain its column order.
3. State the write/storage cost.
4. Run `EXPLAIN` before and after.
5. Record whether PostgreSQL actually uses it.

---

# Break it 💥

Explain why each statement is dangerous:

1. "Indexes make queries faster, so add all of them."
2. "The table has an index, therefore PostgreSQL must use it."
3. "A composite index `(a,b)` is equivalent to separate indexes on `a` and `b`."
4. "`EXPLAIN ANALYZE DELETE ...` is harmless because EXPLAIN doesn't execute."
5. "A sequential scan is always bad."

That last one matters: scanning a tiny table can be cheaper than bouncing through an index.

---

# Retrieval quiz

1. What are the main costs of an index?
2. Why should indexes be derived from access patterns?
3. What query family is a B-tree good at?
4. Why does column order matter in a composite index?
5. What problem can a partial index solve?
6. When might GIN be useful?
7. What does `EXPLAIN` show?
8. What does `ANALYZE` add?
9. Why can a sequential scan be correct?
10. What would you inspect if estimated and actual row counts differ dramatically?

## Exit criterion

You can take a real SQL query, propose an index, explain the write cost, and validate the choice with `EXPLAIN ANALYZE` rather than intuition alone.
