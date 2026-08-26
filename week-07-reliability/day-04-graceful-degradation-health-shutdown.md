# Day 4 — Graceful Degradation, Health Checks & Graceful Shutdown

## Goal

Keep useful product behavior available during partial failure and prevent health automation from causing more damage.

## Timebox

- 20 min — graceful degradation
- 25 min — liveness/readiness/startup
- 20 min — graceful shutdown/draining
- 20 min — transcription degraded modes
- 10 min — quiz

---

# 1. Availability is not binary

A product can often continue with reduced functionality.

Example transcription platform:

```text
Core upload available
AI summaries unavailable
Search unavailable
Analytics delayed
```

versus:

```text
503 everything
```

Ask:

> What is the minimum useful product we can still safely provide?

---

# 2. Hard dependency vs soft dependency

### Hard dependency

Without it, this operation cannot remain correct.

Example:

```text
Create job → authoritative PostgreSQL unavailable
```

You may need to reject/defer rather than pretend creation succeeded.

### Soft dependency

The core operation can continue without it.

Example:

```text
AI-generated title service unavailable
→ still save the transcript
```

Reliability improves when unnecessary hard dependencies become soft.

---

# 3. Degraded modes for transcription

Possible modes:

### Redis cache unavailable

```text
read directly from PostgreSQL
+ reduce optional cache traffic
+ protect DB from stampede
```

### AI summary unavailable

```text
transcript = ready
summary = temporarily unavailable
```

### AI transcription provider unavailable

```text
accept upload if durable intake remains healthy
mark job QUEUED / WAITING_FOR_PROVIDER
stop launching expensive doomed attempts
```

### Analytics unavailable

```text
buffer/drop non-critical analytics according to policy
core user workflow continues
```

---

# 4. Health checks are contracts

Health checks answer different questions.

## Startup

> Has this process finished starting?

Useful for slow initialization.

## Liveness

> Is this process stuck in a state where restart is likely to help?

Failure may trigger restart.

## Readiness

> Should this instance receive traffic **right now**?

Failure removes the instance from normal routing while the process may remain alive.

Do not collapse them into one `/health` endpoint with one meaning.

---

# 5. The dangerous liveness check

Imagine:

```text
PostgreSQL becomes slow
      ↓
API liveness checks PostgreSQL
      ↓
all pods report NOT LIVE
      ↓
Kubernetes restarts all pods
      ↓
all pods reconnect simultaneously
      ↓
DB receives connection storm
      ↓
🔥
```

A dependency outage should not automatically imply the API process itself must be restarted.

Readiness is often the safer place for traffic-serving dependency conditions.

---

# 6. Dependency-aware readiness

Possible design:

```text
/livez
  process event loop alive
  basic internal sanity

/readyz
  required config loaded
  DB connection acquisition possible
  migrations/schema compatible
  service not draining
```

Be careful about checking every optional dependency synchronously on every probe.

Probes themselves create traffic.

---

# 7. Graceful shutdown

When removing an API/worker instance:

```text
mark not ready
      ↓
stop receiving new work
      ↓
drain in-flight work
      ↓
finish / checkpoint / release leases
      ↓
close connections
      ↓
terminate
```

Abrupt termination can create:

- dropped HTTP requests,
- lost ACKs,
- duplicate message redelivery,
- half-written temp files,
- confused clients.

For queue workers, redelivery may be okay **if effects are idempotent**.

---

# 8. Graceful degradation requires explicit UX

Bad:

```text
Processing...
```

for six hours with no explanation.

Better:

```text
Your upload is safe.
Transcription is delayed because processing capacity is temporarily unavailable.
No action is required.
```

Reliability is partly a **product communication problem**.

---

# Exercise — degraded mode matrix

Fill:

| Dependency | Hard/soft for operation? | Degraded behavior | User message | Recovery trigger |
|---|---|---|---|---|
| Redis cache | ? | ? | ? | ? |
| Queue | ? | ? | ? | ? |
| PostgreSQL | ? | ? | ? | ? |
| R2 | ? | ? | ? | ? |
| AI transcription | ? | ? | ? | ? |
| AI summary | ? | ? | ? | ? |
| Analytics | ? | ? | ? | ? |

---

# Break it 💥

1. Every readiness probe runs a heavyweight DB query every second.
2. AI provider outage makes every API pod unready.
3. Redis cache failure causes direct DB traffic to increase 100×.
4. Worker receives SIGTERM halfway through a chunk.
5. User sees “failed” even though upload is durable and processing will resume.

---

# Retrieval quiz

1. Define graceful degradation.
2. Hard vs soft dependency?
3. Startup vs liveness vs readiness?
4. Why can a poorly designed liveness check create a cascading failure?
5. Why mark an instance unready before termination?
6. What does graceful worker shutdown need to consider?
7. Give one transcription feature that could degrade independently.
8. Why is degraded UX/status part of reliability?

## Exit criterion

You can define **what still works** during each dependency outage and configure health semantics without restarting healthy processes because a dependency is sick.
