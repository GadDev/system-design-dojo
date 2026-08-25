# Week 2 Review — 40-Question Retrieval Quiz

## Rule

Do this **without notes first**.

Retrieval exposes gaps that rereading hides.

---

# Part 1 — Data-model choices

1. Name five workload characteristics that should influence database choice.
2. Why is "SQL vs NoSQL" too coarse to be a complete architecture decision?
3. What does normalization help reduce?
4. When can denormalization be a good design choice?
5. Why might PostgreSQL JSONB be useful without abandoning a relational model?
6. Give two objects in the transcription system that clearly belong in object storage.
7. What does polyglot persistence mean?

---

# Part 2 — Keys, constraints & relationships

8. What properties does a PostgreSQL primary key enforce?
9. What is the difference between a natural and surrogate key?
10. Why might a stable UUID be preferable to email as user identity?
11. What problem does a foreign key solve?
12. In a one-to-many relationship, where does the FK usually live?
13. Does PostgreSQL automatically index the referencing side of a foreign key?
14. What constraint prevents duplicate chunk numbers within one job?
15. Why is `ON DELETE CASCADE` a product/lifecycle decision rather than a convenience keyword?

---

# Part 3 — Indexes

16. Name three costs introduced by an index.
17. Why should indexes be designed from queries rather than columns?
18. What is the main Week 2 use case for a B-tree index?
19. Why does column order matter in `(user_id, created_at)`?
20. When can a partial index be attractive?
21. What type of index is commonly used for JSONB containment/search patterns?
22. When might BRIN be attractive?
23. What does `EXPLAIN` show?
24. What important behavior does `EXPLAIN ANALYZE` add?
25. Why might PostgreSQL correctly choose a sequential scan even when an index exists?

---

# Part 4 — Transactions & concurrency

26. Define ACID in your own words.
27. What does PostgreSQL autocommit mean?
28. What is MVCC trying to accomplish?
29. What is PostgreSQL's default transaction isolation level?
30. Why might a SERIALIZABLE transaction need to be retried?
31. Why is a transaction around a five-minute external AI API call usually a poor design?
32. What is a deadlock?
33. Why is `completed_chunks = completed_chunks + 1` safer than an application read-modify-write sequence?

---

# Part 5 — Pooling & scaling

34. Why do horizontally scaled API instances create database connection pressure?
35. What does PgBouncer do?
36. How does transaction pooling differ from session pooling?
37. Why is replication not a backup?
38. What correctness issue can replica lag create immediately after a write?
39. Partitioning vs sharding: explain the difference in two sentences.
40. What evidence would you want before sharding the transcription database?

---

# Architecture reconstruction

Draw this from memory and annotate the purpose of each arrow:

```text
FastAPI instances
      ↓
connection pool / PgBouncer
      ↓
PostgreSQL primary
      ↓
read replica
```

Then add:

```text
R2 object storage
```

and explain which data goes where.

---

# Scenario round

## Scenario A

The `jobs` table has 50M rows. `GET /jobs` is slow. Database CPU is modest.

What do you inspect first?

## Scenario B

Database CPU is low, but clients wait 2 seconds to acquire connections.

What class of problem is this?

## Scenario C

A user creates a job then immediately GETs it from a replica and receives 404.

Explain.

## Scenario D

Chunk table retention policy is 30 days, and you delete hundreds of millions of old rows monthly.

What database feature becomes worth investigating?

## Scenario E

You've optimized queries, pooled connections, scaled hardware, and separated stale-tolerant reads, but one PostgreSQL node is still at sustained write/storage limits.

What previously-premature option is now worth evaluating?

---

# Oral defense

Give yourself 90 seconds per prompt:

> Why PostgreSQL for the transcription control plane?

> When would you put transcript text in R2 instead?

> Why can adding a read replica reduce performance pressure but weaken freshness?

> Why is sharding not simply "partitioning but more scalable"?

> What is the most dangerous data race in chunk processing, and how would you defend against it?

---

# Score

| Score | Meaning |
|---|---|
| 36–40 | Strong — move on |
| 31–35 | Good — review two weak areas |
| 24–30 | Rework the relevant labs |
| <24 | Redraw the data model and repeat Days 2–6 |

The number is not the goal.

The goal is being able to answer **why** without hiding behind product names.
