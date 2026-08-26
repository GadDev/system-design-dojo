# Day 4 — Distributed Transactions & Two-Phase Commit

## Goal

Understand why a transaction that spans **multiple independent resource managers** is fundamentally harder than one PostgreSQL transaction, and when two-phase commit is justified or too expensive.

## Timebox

- 20 min — local vs distributed atomicity
- 25 min — 2PC mechanics
- 20 min — failure windows
- 15 min — PostgreSQL prepared transactions
- 20 min — alternatives
- 10 min — quiz

---

# 1. Local ACID is powerful

Inside one PostgreSQL database:

```sql
BEGIN;

UPDATE jobs
SET status = 'COMPLETED'
WHERE id = :job_id;

INSERT INTO billing_ledger (...);

COMMIT;
```

The database coordinates atomicity for both changes.

Now split ownership:

```text
Job DB
Billing DB
Message broker
Object storage
```

There is no magical shared `COMMIT` unless the systems participate in a distributed transaction protocol.

---

# 2. The dual-write problem

Classic sequence:

```text
1. PostgreSQL COMMIT ✅
2. Publish JobCompleted ❌
```

Now database and message system disagree.

Reverse order:

```text
1. Publish JobCompleted ✅
2. PostgreSQL COMMIT ❌
```

Now consumers may react to a fact that never committed.

Week 5 introduced the transactional outbox for this reason.

---

# 3. Two-phase commit (2PC)

2PC introduces a coordinator and participants.

## Phase 1 — Prepare

```text
Coordinator
  ├── DB A: can you commit?
  ├── DB B: can you commit?
  └── resource C: can you commit?
```

Participants persist enough state to promise they can later commit.

## Phase 2 — Commit / rollback

If all prepared:

```text
Coordinator → COMMIT everyone
```

Otherwise:

```text
Coordinator → ROLLBACK everyone
```

This provides powerful atomicity across cooperating transactional resources.

---

# 4. Why 2PC is expensive operationally

A prepared participant may hold:

- locks,
- transaction state,
- resources needed by other work.

If the coordinator is unavailable after prepare, participants can remain uncertain.

That makes recovery logic essential.

PostgreSQL warns that prepared transactions should be short-lived and that leaving them prepared can interfere with vacuuming and keep locks held.

---

# 5. PostgreSQL reference: `PREPARE TRANSACTION`

Conceptually:

```sql
BEGIN;
UPDATE accounts SET ...;
PREPARE TRANSACTION 'global-tx-123';
```

Later:

```sql
COMMIT PREPARED 'global-tx-123';
```

or:

```sql
ROLLBACK PREPARED 'global-tx-123';
```

PostgreSQL documentation explicitly says this facility is intended for **external transaction managers**, not ordinary application code.

That should make you suspicious of casually building your own distributed transaction coordinator on a Friday afternoon. 😄

---

# 6. 2PC failure windows

Consider:

```text
DB A PREPARED ✅
DB B PREPARED ✅
Coordinator crashes 💥
```

The participants cannot simply forget the transaction.

They need durable coordinator/recovery information to decide commit or rollback.

Other hazards:

- long lock retention,
- coordinator availability,
- operational cleanup of orphaned prepared transactions,
- increased latency,
- all participants must support the protocol.

---

# 7. Why object storage usually doesn't join your 2PC

Your R2 object write is not a PostgreSQL prepared transaction participant.

So this workflow:

```text
write R2 object
update PostgreSQL
publish event
```

cannot usually be made one classic ACID transaction across all three.

Instead you design:

- idempotent steps,
- deterministic artifact keys,
- outbox/inbox patterns,
- sagas/compensation,
- reconciliation.

---

# 8. When a saga is more natural

For long-running business workflows:

```text
reserve quota
→ process video
→ charge usage
→ publish completion
```

holding distributed locks for minutes/hours is undesirable.

A saga uses **local transactions** plus continuation/compensation.

Example:

```text
ReserveQuota ✅
StartProcessing ✅
ChargeUsage ❌
        ↓
Compensate / release quota or mark billing pending
```

Important:

> Compensation is not database rollback.

It is a new business action that reaches an acceptable state.

---

# 9. Decision framework

Ask:

```text
Can these writes live in one database transaction?
        ↓ yes
Use local ACID.

No
        ↓
Must observers see atomic all-or-nothing state immediately?
        ↓ yes
Can all resources safely participate in 2PC?
        ↓ maybe
2PC / transactional coordinator may be justified.

No / long running / heterogeneous resources
        ↓
Saga + idempotency + outbox + reconciliation.
```

---

# Exercise — classify the transaction

For each workflow, choose local ACID, 2PC-style distributed transaction, saga/eventual workflow, or “redesign boundaries.”

1. Insert job + chunk rows in same PostgreSQL DB.
2. Update job DB + billing DB owned by separate services.
3. Write R2 artifact + PostgreSQL metadata.
4. Create user + profile in same database.
5. Reserve scarce inventory + charge payment provider.
6. Publish `JobCompleted` after DB commit.

Defend your choice.

---

# Break it 💥

1. Coordinator dies after all participants prepare.
2. One participant becomes unreachable during commit phase.
3. Prepared transaction holds a hot row lock for 20 minutes.
4. Object storage write succeeds but DB transaction rolls back.
5. Compensation itself fails.

What durable state is needed for recovery?

---

# Retrieval quiz

1. What makes a transaction “distributed” in this context?
2. What is the dual-write problem?
3. What happens in 2PC prepare phase?
4. Why can a prepared transaction be operationally dangerous?
5. Why is R2 unlikely to participate in PostgreSQL 2PC?
6. What problem does the transactional outbox solve?
7. Why is saga compensation not equivalent to rollback?
8. When should you prefer one local transaction over distributed coordination?

## Exit criterion

You can explain why **cross-resource atomicity costs coordination**, and choose a safer alternative when that cost is unnecessary.
