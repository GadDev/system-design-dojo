# Day 5 — Failover, Redundancy, RTO/RPO & Stateful Recovery

## Goal

Understand what high availability actually requires when a stateful primary disappears.

## Timebox

- 20 min — redundancy/failover model
- 20 min — RTO/RPO
- 20 min — Redis/PostgreSQL examples
- 20 min — split brain + failback
- 10 min — exercise + quiz

---

# 1. Redundancy is not failover

Having two servers is not enough.

You need:

```text
failure detection
      ↓
leader/primary decision
      ↓
traffic/client reconfiguration
      ↓
state correctness
      ↓
recovery/failback
```

A standby nobody knows how to promote is just an expensive decoration.

---

# 2. RTO and RPO

## Recovery Time Objective — RTO

> How long can the service/data function remain unavailable?

Example:

```text
RTO = 5 minutes
```

## Recovery Point Objective — RPO

> How much recent data can the business tolerate losing?

Example:

```text
RPO = 30 seconds
```

RPO influences replication/durability choices.

RTO influences detection, promotion, routing and operational automation.

---

# 3. Availability vs durability

These are related but different.

A system can be:

```text
available but lose recent writes
```

or:

```text
temporarily unavailable but preserve every acknowledged write
```

Synchronous replication usually trades latency/availability for stronger durability guarantees.

Asynchronous replication usually improves write latency/availability but can leave a loss window during failover.

---

# 4. PostgreSQL failover mental model

```text
Primary PostgreSQL
      │ WAL
      ▼
Standby PostgreSQL
```

If primary fails:

```text
failure detected
      ↓
promote suitable standby
      ↓
route clients to new primary
      ↓
prevent old primary from accepting writes
      ↓
rebuild redundancy
```

The “prevent old primary” step matters.

If old and new primary both accept writes, you have a split-brain scenario.

---

# 5. Redis failover mental model

For non-clustered Redis, Sentinel can provide:

- monitoring,
- failure detection,
- leader election/failover coordination,
- replica promotion,
- client discovery of the current master.

But asynchronous replication means acknowledged writes can still be lost in certain failure windows.

Again:

> failover improves availability; it does not automatically mean zero data loss.

---

# 6. Failover must be tested

A document saying:

```text
“promote the replica”
```

is not evidence that failover works.

Test:

```text
How is failure detected?
How long does detection take?
Who/what promotes?
How do clients discover the new primary?
What happens to in-flight transactions?
How much data is missing?
How is the old primary fenced?
How is a new standby created?
```

---

# 7. Object storage failure

Your application does not control R2's internal failover.

Your responsibility is client-side behavior:

```text
classify error
honor retry guidance
backoff + jitter
bound concurrency
preserve upload/chunk state
avoid re-uploading successful multipart parts
surface delayed processing
```

Provider-managed does not mean failure-free.

---

# 8. AI provider failover

A second provider sounds attractive:

```text
Provider A fails
      ↓
Provider B
```

But ask:

- same transcript quality?
- same timestamps?
- same diarization behavior?
- same data-processing/GDPR terms?
- same supported languages?
- same cost?
- can outputs be merged consistently?
- can a job switch provider halfway through?

A fallback provider creates a **semantic compatibility problem**, not just a routing problem.

Often safer:

```text
queue/defer
```

than silently produce a materially different result.

---

# 9. Failback

After failover succeeds, the system may be in a degraded topology:

```text
new primary
no standby
```

Recovery is not complete until redundancy is restored.

Operational plan:

```text
stabilize
verify data
rebuild standby
restore replication
verify failover readiness
close incident
```

---

# Exercise — RTO/RPO table

Choose target objectives for:

| Component | RTO | RPO | Why |
|---|---:|---:|---|
| User/job PostgreSQL data | ? | ? | ? |
| Redis cache | ? | ? | ? |
| Redis queue/stream | ? | ? | ? |
| Uploaded video in R2 | ? | ? | ? |
| Generated transcript | ? | ? | ? |
| Analytics | ? | ? | ? |

Different data deserves different objectives.

---

# Break it 💥

1. PostgreSQL standby is 90 seconds behind when primary dies.
2. Old primary comes back and clients reconnect to it.
3. Redis failover succeeds but one acknowledged queue message was never replicated.
4. Failover automation promotes a stale/incomplete candidate.
5. Provider B is used as fallback but produces incompatible timestamp semantics.

---

# Retrieval quiz

1. Redundancy vs failover?
2. Define RTO.
3. Define RPO.
4. Why can asynchronous replication lose acknowledged writes?
5. What is split brain?
6. What is fencing/STONITH trying to prevent?
7. Why is failback part of recovery?
8. Why is multi-provider AI fallback more complex than changing an HTTP hostname?

## Exit criterion

You can describe failover as a **state transition with RTO/RPO, fencing and recovery**, not as “we have a replica.”
