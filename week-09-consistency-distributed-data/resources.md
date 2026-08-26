# Week 9 — Sources & Reading Map 📚

The priority order for this week is:

```text
PostgreSQL / IETF / primary papers
        ↓
major architecture guidance
        ↓
books
        ↓
worked examples
```

Do not memorize consistency vocabulary without tying it to a failure scenario.

---

# Day 1 — consistency models

## Core

- **Designing Data-Intensive Applications, 2nd Edition** — Martin Kleppmann & Chris Riccomini  
  Focus: replication, consistency models, linearizability, transactions, distributed failure.  
  https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/

- PostgreSQL 18 — Transaction Isolation  
  https://www.postgresql.org/docs/18/transaction-iso.html

## Read for

- snapshot visibility,
- serializable guarantees,
- why transaction isolation is about concurrent observations,
- why applications sometimes need stricter guarantees than default Read Committed.

---

# Day 2 — CAP, partitions & replicas

## Core

- Eric Brewer — **CAP Twelve Years Later: How the “Rules” Have Changed**  
  DOI: 10.1109/MC.2012.37  
  Search/read via IEEE or your library access.

- Seth Gilbert & Nancy Lynch — **Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services** (2002)  
  Original formal CAP proof.

- AWS — CAP theorem practical explanation  
  https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/cap-theorem.html

- PostgreSQL 18 — Logical Replication  
  https://www.postgresql.org/docs/18/logical-replication.html

## Read for

- CAP applies to behavior during communication partitions,
- partition tolerance is not a nice-to-have in distributed systems,
- asynchronous copies naturally introduce lag,
- do not classify entire technologies without specifying topology/operation.

## Optional rabbit hole

- PACELC — learn the intuition only: **partition tradeoff, otherwise latency/consistency tradeoff**.

---

# Day 3 — optimistic concurrency

## Core

- RFC 9110 — HTTP Semantics, §13 Conditional Requests / `If-Match`  
  https://www.rfc-editor.org/rfc/rfc9110.html#name-conditional-requests

- PostgreSQL 18 — Concurrency Control  
  https://www.postgresql.org/docs/18/mvcc.html

- PostgreSQL 18 — Data Consistency Checks at the Application Level  
  https://www.postgresql.org/docs/18/applevel-consistency.html

## Read for

- lost updates,
- conditional requests,
- serializable transactions vs application conflict checks,
- row-level/pessimistic locking vs optimistic versioning.

---

# Day 4 — distributed transactions

## Core

- PostgreSQL 18 — Two-Phase Transactions  
  https://www.postgresql.org/docs/18/two-phase.html

- PostgreSQL 18 — `PREPARE TRANSACTION`  
  https://www.postgresql.org/docs/18/sql-prepare-transaction.html

## Important PostgreSQL warning

PostgreSQL states that `PREPARE TRANSACTION` is intended for **external transaction managers**, and warns against leaving transactions in prepared state for long periods because they retain locks and can interfere with maintenance.

## Book

- **Database Internals** — Alex Petrov  
  Read sections around distributed transactions, replication and consensus as your depth companion.

---

# Day 5 — event-driven architecture

## Core

- Microsoft Azure Architecture Center — Event-Driven Architecture Style  
  https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven

- Apache Kafka Design / Documentation  
  https://kafka.apache.org/documentation/

## Read for

- producer/channel/consumer model,
- pub/sub vs streaming,
- decoupling,
- eventual consistency,
- ordering and duplicates,
- replay,
- correlation and observability,
- schema evolution.

## Companion

- **Designing Event-Driven Systems** — Ben Stopford  
  Useful for log/event-stream architecture and practical event design.

---

# Day 6 — sagas & compensation

## Core

- AWS Prescriptive Guidance — Saga patterns  
  https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-patterns.html

- AWS — Saga choreography  
  https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html

- AWS — Saga orchestration  
  https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html

- Microsoft Azure Architecture Center — Compensating Transaction pattern  
  https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction

## Read for

- local transactions,
- continuation vs compensation,
- choreography vs orchestration,
- compensation can fail and therefore must itself be durable/idempotent,
- compensation is business logic, not magical rollback.

---

# Day 7 — design lab

No new reading before doing the lab.

After your design, revisit:

1. PostgreSQL transaction isolation/concurrency docs.
2. CAP practical guidance.
3. Event-driven architecture challenges.
4. Saga orchestration/choreography tradeoffs.

Compare your decisions, not your boxes.

---

# Recommended books for this week

## 1. Designing Data-Intensive Applications, 2nd Edition

Primary book for this phase.

Focus on:

- replication,
- distributed consistency,
- transactions,
- linearizability,
- distributed-system failure,
- streams/dataflow.

## 2. Database Internals — Alex Petrov

Use for deeper storage/distributed-database mechanics.

## 3. Designing Event-Driven Systems — Ben Stopford

Use for event streams, logs and event-driven architecture.

## 4. Enterprise Integration Patterns

Useful pattern vocabulary:

- idempotent receiver,
- message sequence,
- aggregator,
- correlation identifier,
- compensating actions.

---

# Reading rule

After every source, answer:

> **Which fact requires this consistency guarantee, and what happens when the guarantee cannot be provided?**

Then answer:

> **How does the system detect and repair divergence?**
