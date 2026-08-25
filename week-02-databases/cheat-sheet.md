# Week 2 Cheat Sheet — Databases & Storage

## Workload-first database choice

Ask:

```text
reads / writes
relationships
consistency
size
cardinality
growth
latency
operations
```

Do not choose from slogans.

---

# SQL vs document

## Relational

Strong at:

```text
relationships
constraints
joins
multi-row transactions
ad-hoc queries
```

## Document

Strong when:

```text
aggregate naturally read together
schema varies
data can be embedded and remains bounded
```

## Object storage

Strong at:

```text
large immutable blobs
videos
audio
exports
large artifacts
```

---

# Primary key

```text
unique row identity
UNIQUE + NOT NULL
PostgreSQL creates unique B-tree index
```

Prefer stable identity.

```text
id = surrogate identity
email = business uniqueness
```

---

# Foreign key

```text
referential integrity
```

```sql
upload.user_id REFERENCES users(id)
```

PostgreSQL does **not** automatically index the referencing FK column.

---

# Index mental model

```text
read speed ↑
write cost ↑
storage ↑
maintenance ↑
```

Design from queries.

Common:

```text
B-tree → equality/range/order
GIN → JSONB/full-text-like inverted lookup
BRIN → huge naturally ordered tables
partial → hot subset
composite → query family matching left-side prefix/order
```

Validate with:

```sql
EXPLAIN (ANALYZE, BUFFERS) ...
```

---

# Transaction

```text
BEGIN
  related writes
COMMIT / ROLLBACK
```

ACID:

```text
Atomicity
Consistency
Isolation
Durability
```

PostgreSQL default isolation:

```text
READ COMMITTED
```

MVCC:

```text
multiple row versions / snapshots
readers and writers can coexist efficiently
```

Serializable:

```text
stronger guarantee
serialization failures possible
retry whole transaction
```

---

# Connection pooling

```text
connections are finite
```

Do not:

```text
open connection per HTTP request
hold transaction during slow AI call
multiply huge pools across 100 app instances
```

PgBouncer:

```text
session pooling
transaction pooling
statement pooling
```

Pool metrics:

```text
active connections
waiting clients
pool wait time
query p95/p99
DB CPU
I/O
locks
```

---

# Replication

```text
Primary → Standby/Replica
```

Goals:

```text
HA
failover
read scaling
migration/distribution
```

Not a backup.

## Async

```text
lower write latency
replica lag possible
```

## Sync

```text
stronger failover durability
higher coordination/latency cost
```

Read replica danger:

```text
write primary
immediate read replica
→ stale / 404
```

---

# Partitioning

```text
one logical table
multiple physical partitions
same PostgreSQL system
```

PostgreSQL:

```text
RANGE
LIST
HASH
```

Useful when:

```text
very large tables
queries align with partition key
retention/bulk drop
```

---

# Sharding

```text
multiple independent DB nodes
subset of rows on each
routing required
```

New problems:

```text
cross-shard joins
cross-shard transactions
rebalancing
hot shards
global uniqueness
operations
```

Use late, with evidence.

---

# Scale decision ladder

```text
slow query
→ EXPLAIN / indexes / SQL

connection pressure
→ pooling

read pressure
→ cache / replica

huge lifecycle-oriented table
→ partitioning

single-node storage/write ceiling
→ consider sharding
```

---

# Transcription storage heuristic

```text
PostgreSQL
→ users
→ uploads metadata
→ jobs
→ chunk state
→ searchable structured results

Object storage
→ raw video
→ extracted audio
→ large immutable transcript/export artifacts
```

Hybrid is normal.

---

# Ten questions to ask in a database design review

1. What are the dominant queries?
2. What is the write pattern?
3. What must be strongly consistent?
4. Which constraints should the DB enforce?
5. Which indexes correspond to real queries?
6. What are the transaction invariants?
7. How many concurrent DB connections can exist?
8. Which reads can tolerate staleness?
9. What table grows fastest?
10. What evidence would justify partitioning or sharding?
