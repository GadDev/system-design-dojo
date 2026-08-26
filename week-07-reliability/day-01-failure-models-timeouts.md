# Day 1 — Failure Models, Deadlines & Timeouts

## Goal

Learn to bound waiting time and reason about **slow failure** as seriously as explicit error responses.

## Timebox

- 20 min — failure taxonomy
- 25 min — timeout/deadline mental model
- 20 min — timeout budgeting
- 20 min — transcription dependency exercise
- 10 min — retrieval quiz

---

# 1. Failure is broader than “500 error”

A dependency can fail in many ways:

| Failure class | Example | Important question |
|---|---|---|
| Explicit | `500 Internal Server Error` | Retryable? |
| Rate limited | `429 Too Many Requests` | Honor `Retry-After`? |
| Timeout | No response before deadline | Did the operation still happen? |
| Connection failure | TCP/TLS connection cannot be established | Is dependency reachable? |
| Partial failure | Some replicas/partitions unhealthy | Can we route around it? |
| Slow failure | p99 jumps from 500 ms to 20 s | Are resources being pinned? |
| Corrupt/invalid result | Response arrives but violates contract | Fail fast or retry? |
| Stale result | Replica responds with old state | Is staleness acceptable? |
| Overload | Queue/connection pools saturated | Will retries amplify it? |

The dangerous class is often **slow failure**.

A service that returns an error in 20 ms releases resources quickly.

A service that hangs for 30 seconds can consume:

- request slots,
- worker threads/tasks,
- DB connections,
- memory,
- queue visibility time,
- user patience.

---

# 2. Timeout vs deadline

A **timeout** is a bound for one operation.

```text
AI call timeout = 20 s
```

A **deadline** is the latest acceptable completion time for a larger request/workflow.

```text
This API operation must complete by T + 2 s.
```

Deadlines compose better across call chains.

```text
Client deadline: 2000 ms

API work          100 ms
DB budget         400 ms
Dependency A      500 ms
Dependency B      600 ms
serialization     100 ms
safety margin     300 ms
------------------------
Total            2000 ms
```

If Dependency A has already consumed 900 ms, blindly giving Dependency B its full 600 ms may violate the end-to-end deadline.

---

# 3. Connection timeout vs request timeout

Treat these separately.

```text
Connect timeout
   ↓
How long will I wait to establish the connection?

Request/read timeout
   ↓
How long will I wait for the operation/response?
```

For remote calls, unbounded waits are dangerous.

A system with no timeout can convert one dependency failure into resource exhaustion upstream.

---

# 4. Choosing timeout values

Do not pick:

```text
30 seconds because it feels safe.
```

Start from evidence:

- downstream p50 / p95 / p99 latency,
- acceptable false-timeout rate,
- network geography,
- connection-establishment cost,
- operation type,
- user/workflow deadline,
- retry budget.

Example:

```text
AI chunk transcription
p95 = 8 s
p99 = 14 s
p99.9 = 22 s
```

A 5-second timeout would create huge false failures.

A 2-minute timeout might hold worker capacity far too long during an outage.

The right value is workload-specific.

---

# 5. Timeout ambiguity

This is critical:

```text
Worker → AI provider: POST /transcribe

AI provider completes the operation
        ↓
network response is lost
        ↓
worker times out
```

The worker knows only:

```text
“I did not observe success.”
```

It does **not** necessarily know:

```text
“The operation did not happen.”
```

That is why timeouts and idempotency are tightly connected.

---

# 6. Deadline propagation

Consider:

```text
API
 ↓ 800ms remaining
Service A
 ↓ 350ms remaining
PostgreSQL
```

A mature system can propagate the remaining budget so downstream work does not continue after the caller can no longer use the result.

For background jobs, the equivalent concept may be:

```text
chunk attempt deadline
parent-job SLA/deadline
provider request timeout
queue visibility/lease duration
```

---

# 7. Transcription timeout matrix

Create one row per dependency:

| Dependency | Operation | Expected latency | Timeout | On timeout | Retry safe? |
|---|---|---:|---:|---|---|
| PostgreSQL | update chunk state | ? | ? | ? | ? |
| Redis | enqueue / ACK | ? | ? | ? | ? |
| R2 | GET audio chunk | ? | ? | ? | ? |
| AI provider | transcribe chunk | ? | ? | ? | ? |
| R2 | PUT chunk result | ? | ? | ? | ? |

Do **not** copy timeout values from a blog. Use measurements in production later.

---

# 8. Failure budget thought experiment

Suppose a chunk worker has a 60-second attempt deadline.

You could spend it as:

```text
Attempt 1: timeout 15 s
Backoff:   up to 2 s
Attempt 2: timeout 15 s
Backoff:   up to 4 s
Attempt 3: timeout 15 s
Reserve:   9 s
```

This is different from:

```text
3 attempts × 60 s each
```

which silently turned a 60-second operation into a 3-minute-plus operation.

---

# 9. Exercise — design a timeout budget

For a public endpoint:

```http
GET /jobs/{id}
```

Assume a 1-second end-to-end SLO target.

Budget:

```text
LB / network:
FastAPI:
PostgreSQL:
Redis optional cache:
serialization:
reserve:
```

Then design a separate timeout model for:

```text
AI chunk transcription
```

Explain why the values and semantics should differ.

---

# Break it 💥

Predict what happens if:

1. PostgreSQL accepts TCP connections but every query takes 25 seconds.
2. R2 GET never completes.
3. Worker timeout is shorter than normal p99 AI latency.
4. API gateway timeout is 30s but your backend waits 60s.
5. Client disconnects but the backend continues expensive work for minutes.

For each ask:

```text
What resource remains occupied?
Who should cancel?
Could a retry make it worse?
```

---

# Retrieval quiz

1. Difference between timeout and deadline?
2. Why is a slow dependency often more dangerous than a fast explicit failure?
3. Why does a timeout not prove an operation had no side effect?
4. Name two different timeout types.
5. What data should inform timeout values?
6. Why should retry duration fit inside a larger deadline/retry budget?
7. Give one reason a timeout can be **too short**.
8. Give one reason a timeout can be **too long**.

## Exit criterion

You can create a dependency timeout budget and explain what happens after each timeout instead of simply saying “we set 30 seconds.”
