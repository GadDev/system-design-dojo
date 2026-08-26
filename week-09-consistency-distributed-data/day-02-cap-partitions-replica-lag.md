# Day 2 — CAP, Network Partitions & Replica Lag

## Goal

Use CAP as a practical question about **what the system does when replicas cannot communicate**, not as a trivia exercise about labeling products AP/CP.

## Timebox

- 20 min — CAP intuition
- 15 min — partitions vs ordinary latency
- 20 min — replicas and staleness
- 20 min — scenarios
- 10 min — retrieval quiz

---

# 1. The useful CAP question

Assume two nodes store shared state:

```text
Region A  ←──── network ────→  Region B
```

Now the network partitions:

```text
Region A  ←────  X  ────→  Region B
```

Both regions receive requests.

You cannot guarantee both of these simultaneously for the same shared fact:

- every request returns a successful response,
- every response acts on one immediately consistent value.

That is the useful design tension.

---

# 2. CAP terminology in practice

## Consistency (C)

In CAP, consistency is close to a single-copy/linearizable view: clients do not observe divergent values as though conflicting replicas were both authoritative.

## Availability (A)

Every request to a non-failing node receives a response rather than being refused solely because coordination cannot complete.

## Partition tolerance (P)

The system continues to have defined behavior despite lost/delayed communication between nodes.

In real distributed deployments, network partitions cannot be wished away.

So the practical question is usually:

> **During the partition, for this operation, do we reject/defer work to preserve consistency, or continue with weaker consistency to preserve availability?**

---

# 3. Don't turn CAP into product astrology

Avoid statements like:

```text
PostgreSQL = CA
Kafka = AP
MongoDB = CP
```

without describing topology, configuration and operation.

A system can choose differently for different paths.

Example:

```text
billing write       → refuse if authoritative DB unavailable
analytics ingest    → buffer locally and reconcile later
job status read     → allow stale replica read
job cancellation    → require primary/authoritative confirmation
```

Same product. Different consistency decisions.

---

# 4. Partitions are not the only source of stale data

Even with a healthy network, asynchronous replication creates lag.

```text
Primary
  ↓ commit v42
WAL / replication stream
  ↓
Replica still v41
  ↓ later
Replica v42
```

A read replica can therefore improve read scalability while changing freshness guarantees.

---

# 5. Replica lag and read-after-write

Scenario:

```text
POST /jobs/job-1/cancel
→ primary commits CANCELLED

GET /jobs/job-1
→ routed to replica
→ returns PROCESSING
```

Possible strategies:

- temporarily route that user's reads to primary,
- attach a version/LSN and wait until replica catches up,
- use session stickiness to an authoritative read path,
- accept the inconsistency if the UX permits it,
- return the mutation result directly and refresh later.

No single choice is universally correct.

---

# 6. Monotonic reads across replicas

Without care:

```text
Request 1 → Replica A → version 52
Request 2 → Replica B → version 49
```

Now the user sees progress move backward.

For job progress, that is a particularly ugly failure mode.

A client-side defensive rule might be:

```text
shown_progress = max(previous_progress, received_progress)
```

But that only masks one symptom. You still need a server-side consistency contract.

---

# 7. Partition scenarios for the transcription platform

## Scenario A — PostgreSQL primary unreachable from API

Do you:

- accept a new transcription job anyway?
- issue an upload URL but delay job creation?
- reject with `503`?

If job ownership/quota/state must be committed authoritatively, accepting blindly is dangerous.

## Scenario B — analytics projection unavailable

Could the core transcription flow continue?

Probably yes if analytics is derived.

## Scenario C — R2 reachable, PostgreSQL unreachable from worker

Worker can potentially produce an immutable chunk artifact, but cannot finalize workflow state.

This creates **durable partial success**.

You need retry/reconciliation.

## Scenario D — one regional read replica isolated

Could continue serving stale reads if the endpoint permits it, or remove it from serving stricter operations.

---

# 8. CAP does not answer normal-operation latency tradeoffs

CAP is specifically interesting during partitions.

During normal operation, designers also trade latency against consistency.

Optional rabbit hole: PACELC.

```text
If Partition:
    Availability vs Consistency
Else:
    Latency vs Consistency
```

You do not need to memorize the acronym. Keep the intuition.

---

# Exercise — Partition decision table

For each operation, assume Region A cannot communicate with the authoritative database in Region B.

| Operation | Continue? | Consistency sacrificed? | User response | Recovery |
|---|---|---|---|---|
| fetch public pricing | | | | |
| start transcription job | | | | |
| cancel job | | | | |
| append analytics event | | | | |
| fetch completed transcript artifact | | | | |
| update billing ledger | | | | |

---

# Break it 💥

1. Two active regions independently accept cancellation and retry operations for the same job.
2. Replica lag grows from 50 ms to 45 seconds.
3. One API region can reach Redis but not PostgreSQL.
4. Worker can reach R2 but not PostgreSQL.
5. A dashboard reads from a replica that is hours behind.

For each, decide whether the correct response is:

- reject,
- degrade,
- buffer,
- serve stale,
- reconcile later.

---

# Retrieval quiz

1. What is the practical CAP decision during a partition?
2. Why is partition tolerance not usually optional in a distributed deployment?
3. Why is CAP not a useful reason to label a whole product “AP” or “CP” without context?
4. What is replica lag?
5. How can read replicas break read-your-writes?
6. Give two strategies for handling read-after-write when replicas lag.
7. Why might job progress require monotonic-read behavior?
8. What should happen if the authoritative store is unreachable for a correctness-critical write?

## Exit criterion

You can reason from a **network-partition scenario to a concrete user-visible behavior**, without chanting “pick two.”
