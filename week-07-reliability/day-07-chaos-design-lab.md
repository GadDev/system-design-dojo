# Day 7 — Chaos Design Lab: Destroy the Transcription System 💥

## Mission

Do not design a new happy-path architecture today.

Attack the one you already built.

Your job is to prove that failure behavior is deliberate.

---

# Timebox

- 15 min — reconstruct architecture
- 20 min — dependency inventory
- 25 min — failure matrix
- 30 min — game-day experiments
- 20 min — RTO/RPO + degradation review
- 20 min — reliability ADR
- 10 min — oral defense

---

# Part 1 — Reconstruct the system from memory

Draw:

```text
Client
 ↓
Load Balancer
 ↓
FastAPI replicas
 ├── PostgreSQL
 ├── Redis / Queue
 └── Presigned upload control

Client ==================> R2

Queue
 ↓
Orchestrator
 ↓
Chunk Queue
 ├→ Worker
 ├→ Worker
 └→ Worker
       ├→ R2
       ├→ AI Provider
       └→ PostgreSQL

Chunk results
 ↓
Fan-in
 ↓
Merge
 ↓
Final Transcript
```

Now circle every network boundary.

Every circle is a candidate partial failure.

---

# Part 2 — Failure Mode and Effects Analysis (FMEA-lite)

For each failure, score:

```text
Impact:      1–5
Likelihood:  1–5
Detectability difficulty: 1–5
```

You are not doing formal safety engineering. The point is prioritization.

| Failure | User impact | Detection | Automatic recovery | Manual recovery | Risk score |
|---|---|---|---|---|---:|
| Redis unavailable | | | | | |
| Worker crash | | | | | |
| PostgreSQL primary lost | | | | | |
| R2 503 | | | | | |
| AI 429 | | | | | |
| AI slow responses | | | | | |
| duplicate upload | | | | | |
| duplicate queue delivery | | | | | |
| merge finalizer crash | | | | | |
| network partition | | | | | |

---

# Part 3 — The six required attacks

## Attack A — Redis dies

Answer:

1. Cache or queue or both?
2. Which operations still work?
3. Which must stop?
4. Is data/messages lost?
5. Is Redis failover configured?
6. What happens during failover?
7. What protects PostgreSQL from a cache-bypass stampede?
8. What tells users processing is delayed?

## Attack B — Worker dies during chunk 37

Answer:

1. When does broker redelivery occur?
2. What side effects may already exist?
3. How is chunk 37 uniquely identified?
4. What prevents duplicate billing/output/counters?
5. Does the parent progress counter drift?
6. How is the child reconciled?

## Attack C — PostgreSQL unavailable

Answer:

1. Which API requests can safely degrade?
2. Which writes must fail/defer?
3. What do workers do with completed AI output?
4. Is queue consumption paused?
5. Do we have a standby?
6. RTO/RPO?
7. What prevents split brain?

## Attack D — R2 returns 500/503

Answer:

1. Retry class?
2. Timeout?
3. Backoff/jitter?
4. Concurrency reduction?
5. Multipart part vs whole upload retry?
6. What state proves which parts already succeeded?

## Attack E — AI provider rate limits us

Answer:

1. Honor `Retry-After`?
2. Reduce provider concurrency?
3. Circuit breaker?
4. Queue-age implications?
5. Worker autoscaling implications?
6. User-visible state?
7. When does job go to DLQ/permanent failure?

## Attack F — duplicate upload

Answer:

1. Is duplicate upload semantically allowed?
2. Is duplicate *processing* allowed?
3. How would you fingerprint equivalent work?
4. What inputs/config must be part of identity?
5. What are the privacy implications of cross-user dedup?

---

# Part 4 — Design chaos experiments

A chaos experiment needs:

```text
Hypothesis
Blast radius
Fault injection
Expected system behavior
Metrics to watch
Abort condition
Recovery step
Evidence collected
```

Never start with:

```text
“Let's kill production Redis and see what happens 😈”
```

Start small.

---

## Experiment 1 — worker termination

Hypothesis:

> Killing one worker after durable chunk output but before ACK causes exactly one logical chunk result after redelivery.

Fault:

```text
SIGKILL worker at injected checkpoint
```

Observe:

- pending/redelivered message,
- duplicate attempts,
- unique result count,
- parent progress,
- final transcript correctness.

Abort if:

```text
duplicate billing or corrupt parent state appears
```

---

## Experiment 2 — AI rate limit

Inject:

```text
429 for 60 seconds
```

Expected:

- retries use backoff+jitter,
- concurrency drops/holds,
- queue grows in a controlled way,
- no retry storm,
- breaker may open if policy says so,
- jobs show delayed state,
- recovery ramps gradually.

---

## Experiment 3 — PostgreSQL latency

Inject latency rather than total outage.

This often reveals more interesting failures:

- connection pool saturation,
- request pile-up,
- false liveness failures,
- retry amplification,
- queue consumer stalls.

Expected:

```text
timeouts bound resource use
readiness/degradation policy activates
liveness does not restart every healthy process
```

---

## Experiment 4 — R2 transient errors

Inject 503s on selected object operations.

Expected:

```text
retry failed operation only
respect elapsed retry budget
preserve successful multipart state
no restart-from-zero behavior
```

---

# Part 5 — Failure matrix

Produce this as your final artifact:

| Component | Failure mode | Detection | Immediate action | Retry | Degrade | Failover | User impact | Recovery proof |
|---|---|---|---|---|---|---|---|---|
| FastAPI | | | | | | | | |
| PostgreSQL | | | | | | | | |
| Redis | | | | | | | | |
| Queue | | | | | | | | |
| Worker | | | | | | | | |
| R2 | | | | | | | | |
| AI provider | | | | | | | | |
| Merge | | | | | | | | |

---

# Part 6 — Reliability ADR

Use `reliability-decision-template.md` and document:

```text
Timeout strategy
Retry policy
Circuit-breaker policy
Bulkhead/concurrency boundaries
Degraded modes
Health semantics
RTO/RPO
Failover plan
DLQ policy
Game-day plan
```

---

# Part 7 — Oral defense

Give yourself 2 minutes per question.

### A

> Why can retries turn a 5% dependency failure into a system-wide outage?

### B

> Why does a timeout not tell you whether a remote side effect happened?

### C

> AI provider is down. Why might “accept uploads and queue them” be safer than immediately failing every upload?

### D

> PostgreSQL is slow. Why can restarting every API instance make the situation worse?

### E

> Redis failed over successfully. Why might some acknowledged writes/messages still be missing?

### F

> What is the difference between being highly available and having zero data loss?

---

# Scoring rubric — 24 points

Give yourself 0–3 in each category:

| Category | Score |
|---|---:|
| Timeout/deadline design | /3 |
| Retry safety + idempotency | /3 |
| Retry storm protection | /3 |
| Circuit/bulkhead design | /3 |
| Graceful degradation | /3 |
| Health + shutdown semantics | /3 |
| Failover + RTO/RPO | /3 |
| Game-day/recovery evidence | /3 |

```text
21–24 → strong reliability reasoning
17–20 → good; review weak categories
12–16 → revisit Days 2–5
<12   → rebuild the dependency recovery matrix
```

---

# Final Week 7 question

> When a dependency fails, what exact evidence tells you it is safe to resume normal traffic?

If your answer is only:

```text
“the service came back”
```

you are not done yet.
