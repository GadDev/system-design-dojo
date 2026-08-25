# Week 2 — Sources, Books & Reading Map

This is the curated bibliography for Week 2.

**Reference system:** PostgreSQL 18.

**Verified for this course revision:** August 2026.

The source hierarchy remains:

1. official PostgreSQL documentation,
2. official maintainer/tool documentation,
3. durable database books,
4. production case studies,
5. interview resources.

---

# Day 1 — SQL vs NoSQL / data modeling

## PostgreSQL JSON / JSONB

https://www.postgresql.org/docs/18/datatype-json.html

Use for:

- `json` vs `jsonb`,
- JSONB indexing,
- deciding what belongs in flexible metadata.

Key lesson:

PostgreSQL is relational but can still model selected semi-structured data. Do not turn that into an excuse to put your entire domain in one JSONB column.

## MongoDB — Data modeling best practices

https://www.mongodb.com/docs/manual/data-modeling/best-practices/

Use as a document-database comparison point for:

- embedding,
- referencing,
- bounded vs unbounded child sets,
- modeling around access patterns.

## MongoDB — Referencing

https://www.mongodb.com/docs/manual/data-modeling/referencing/

Useful because it shows that even document databases have tradeoffs between embedding and normalized/reference-style models.

---

# Day 2 — Keys, constraints & relationships

## PostgreSQL 18 — Constraints

https://www.postgresql.org/docs/18/ddl-constraints.html

Required sections:

- `NOT NULL`,
- `UNIQUE`,
- primary keys,
- foreign keys,
- referential actions (`CASCADE`, `RESTRICT`, etc.).

Important PostgreSQL detail:

A primary key creates a unique B-tree index. A foreign key does **not** automatically create an index on the referencing columns.

## PostgreSQL 18 — Data Definition

https://www.postgresql.org/docs/18/ddl.html

Use as the broader schema/constraint reference.

---

# Day 3 — Indexes & query plans

## PostgreSQL 18 — Indexes

https://www.postgresql.org/docs/18/indexes.html

Recommended sections:

- introduction,
- B-tree,
- multicolumn indexes,
- partial indexes,
- indexes on expressions,
- index-only scans,
- examining index usage.

## PostgreSQL 18 — EXPLAIN

https://www.postgresql.org/docs/18/sql-explain.html

## PostgreSQL 18 — Using EXPLAIN

https://www.postgresql.org/docs/18/using-explain.html

Required lab skill:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...;
```

Remember: `ANALYZE` executes the query.

---

# Day 4 — Transactions, ACID, MVCC & isolation

## PostgreSQL 18 tutorial — Transactions

https://www.postgresql.org/docs/18/tutorial-transactions.html

Start here.

## PostgreSQL 18 — MVCC introduction

https://www.postgresql.org/docs/18/mvcc-intro.html

## PostgreSQL 18 — Transaction Isolation

https://www.postgresql.org/docs/18/transaction-iso.html

Focus on:

- Read Committed,
- Repeatable Read,
- Serializable,
- retries after serialization failures.

## PostgreSQL 18 — Concurrency Control

https://www.postgresql.org/docs/18/mvcc.html

Use as a deeper reference for:

- explicit locks,
- deadlocks,
- consistency checks,
- serialization failure handling.

## PostgreSQL 18 — SAVEPOINT

https://www.postgresql.org/docs/18/sql-savepoint.html

Optional for Week 2.

---

# Day 5 — Connection pooling

## PgBouncer — Features

https://www.pgbouncer.org/features.html

Required:

- session pooling,
- transaction pooling,
- SQL feature compatibility differences.

## PgBouncer — Usage

https://www.pgbouncer.org/usage.html

Useful operational metrics include:

- active clients,
- waiting clients,
- active/idle server connections,
- average wait time,
- `maxwait`.

The course uses PgBouncer as a concrete example, not as a rule that every PostgreSQL deployment needs it on Day 1.

---

# Day 6 — Replication & read replicas

## PostgreSQL 18 — High Availability, Load Balancing, Replication

https://www.postgresql.org/docs/18/high-availability.html

Required ideas:

- standby servers,
- hot standby,
- streaming replication,
- synchronous vs asynchronous tradeoffs,
- failover.

## PostgreSQL 18 — Comparison of replication solutions

https://www.postgresql.org/docs/18/different-replication-solutions.html

## PostgreSQL 18 — Logical Replication

https://www.postgresql.org/docs/18/logical-replication.html

Use to distinguish logical from physical replication.

---

# Day 6 — Partitioning

## PostgreSQL 18 — Table Partitioning

https://www.postgresql.org/docs/18/ddl-partitioning.html

Required:

- why partition,
- range/list/hash,
- partition pruning,
- best-practice warnings.

The docs explicitly warn that partitioning decisions must be made carefully. Good. Keep that energy.

---

# Day 6 — Sharding

PostgreSQL core provides partitioning and replication primitives but does not turn a single PostgreSQL database into an automatic transparent sharded cluster.

For a concrete PostgreSQL-based distributed example:

## Citus — Concepts

https://docs.citusdata.com/en/stable/get_started/concepts.html

Use only to understand:

- coordinator/router concepts,
- distributed tables,
- shard placement,
- why distributed SQL introduces new operational choices.

Do not install Citus just because you reached Day 6. 😄

---

# Books

## Designing Data-Intensive Applications, 2nd Edition

**Martin Kleppmann & Chris Riccomini — O'Reilly, 2026**

https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/

This is the main Week 2 companion.

Read/select chapters or sections on:

- data models,
- storage and retrieval,
- replication,
- partitioning/sharding,
- transactions.

Do not try to finish all of them this week.

Suggested use:

```text
Day 1 → data models
Day 3 → storage/retrieval
Day 4 → transactions
Day 6 → replication + partitioning
```

## Database Internals

**Alex Petrov — O'Reilly**

https://www.oreilly.com/library/view/database-internals/9781492040330/

Optional rabbit hole.

Excellent when you want deeper mental models for:

- B-trees / storage engines,
- WAL,
- replication,
- distributed database internals.

Not required for finishing Week 2.

## PostgreSQL: Up and Running

Use as a practical PostgreSQL companion if you want more hands-on administration/query examples, but prefer PostgreSQL's own documentation for exact current behavior.

---

# Reading schedule

## Minimal path

```text
Day 1 → lesson + PostgreSQL JSONB overview
Day 2 → constraints docs
Day 3 → indexes intro + EXPLAIN basics
Day 4 → transactions tutorial + MVCC intro
Day 5 → PgBouncer features
Day 6 → HA overview + partitioning overview
Day 7 → no new reading; design from memory
```

## Strong path

Add 20–40 minutes/day from DDIA.

## Deep path

Add:

- PostgreSQL isolation chapter,
- detailed EXPLAIN practice,
- physical vs logical replication,
- Citus architecture,
- Database Internals.

---

# Evidence notebook prompts

For every database mechanism:

```text
Mechanism:
Problem solved:
Evidence that would justify it:
Correctness tradeoff:
Performance tradeoff:
Operational tradeoff:
Simpler alternative:
```

Example:

```text
Mechanism: read replica
Problem: primary overloaded by stale-tolerant reporting reads
Evidence: primary read I/O saturation from reporting workload
Correctness cost: replica lag / stale reads
Operational cost: failover + routing + replica monitoring
Simpler alternative: query/index optimization
```
