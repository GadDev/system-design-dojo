# Week 7 — Reliability Cheat Sheet 🛡️

## Mindset

```text
Not: Will it fail?

Ask:
When it fails, what happens next?
```

---

## Failure classes

```text
explicit error
connection failure
timeout
slow response
partial failure
stale response
overload
rate limit
corrupt/invalid response
```

---

## Timeout

Bounds how long one operation waits.

```text
connection timeout
request/read timeout
workflow/attempt deadline
```

Too short → false failures + retry traffic.

Too long → resource pinning + slow failure.

---

## Deadline

Latest acceptable completion time for a larger operation.

```text
remaining budget should shrink downstream
```

---

## Retry

Use when another attempt may succeed.

```text
retry only safe/idempotent operations
bound attempts
bound elapsed time
```

Avoid retrying deterministic permanent errors.

---

## Exponential backoff

```text
1s → 2s → 4s → 8s ... capped
```

## Jitter

Randomize retry timing so clients do not synchronize.

---

## Retry storm

```text
failure
 ↓
retries
 ↓
more load
 ↓
more failure
 ↓
more retries
```

Break the loop with:

```text
backoff + jitter
retry limits
admission control
circuit breaking
load shedding
```

---

## Circuit breaker

```text
CLOSED
  ↓ failures/slow calls
OPEN
  ↓ wait
HALF_OPEN
  ├ success → CLOSED
  └ failure → OPEN
```

Question:

```text
Should I call the dependency right now?
```

---

## Bulkhead

Limit how much shared capacity one dependency/workload can consume.

```text
AI concurrency pool
DB connection pool
tenant concurrency
```

---

## Graceful degradation

```text
hard dependency failure → operation may stop
soft dependency failure → reduced feature set
```

Example:

```text
transcript ready
AI summary unavailable
```

---

## Health checks

```text
startup  → finished starting?
liveness → should process be restarted?
readiness → should instance receive traffic?
```

Do not restart healthy processes just because a dependency is temporarily unavailable.

---

## Graceful shutdown

```text
not ready
 ↓
stop new work
 ↓
drain/checkpoint
 ↓
release leases/connections
 ↓
terminate
```

---

## RTO

Maximum desired recovery time.

## RPO

Maximum acceptable data-loss window.

---

## Failover

```text
detect
 ↓
choose/promote
 ↓
fence old primary
 ↓
reroute clients
 ↓
restore redundancy
```

Replica ≠ automatic failover.

Failover ≠ zero data loss.

---

## DLQ

```text
automatic retry exhausted
      ↓
quarantine + inspect + controlled redrive
```

Must have:

```text
owner
alert
retention
failure context
redrive process
```

---

## Reliability dependency checklist

```text
Timeout?
Retryable errors?
Idempotent?
Backoff + jitter?
Retry budget?
Breaker?
Bulkhead?
Degraded mode?
Health semantics?
Failover?
RTO/RPO?
Recovery proof?
```

---

## Transcription failure reminders

### Redis dies

```text
cache role? queue role?
outbox?
DB stampede protection?
failover?
```

### Worker dies

```text
redelivery
idempotency
deterministic output
```

### PostgreSQL dies

```text
what can degrade?
what must stop?
standby/failover?
```

### R2 5xx

```text
retry failed operation
backoff + jitter
preserve multipart progress
```

### AI 429

```text
Retry-After
reduce concurrency
queue
breaker
DO NOT scale into rate limit
```

### Duplicate upload

```text
allowed?
processing dedup?
identity includes config/version?
privacy boundaries?
```
