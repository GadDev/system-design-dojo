# Day 2 — Retries, Exponential Backoff, Jitter & Retry Budgets

## Goal

Use retries to hide transient failure **without turning a partial outage into a retry storm**.

## Timebox

- 20 min — retry taxonomy
- 25 min — backoff + jitter
- 20 min — retry amplification
- 20 min — retry policy exercise
- 10 min — lab + quiz

---

# 1. A retry is another request

This sounds obvious, but it is the core lesson.

If the original load is:

```text
10,000 requests/sec
```

and every request retries twice during an outage, the dependency may suddenly see up to:

```text
30,000 attempts/sec
```

precisely when it is least healthy.

Retries are therefore a **load-management decision**.

---

# 2. When retrying helps

Often retryable:

- transient network disconnect,
- selected `5xx` failures,
- temporary service unavailable,
- rate limiting when instructed to wait,
- optimistic concurrency conflict when the operation is designed for retry,
- broker redelivery for an idempotent consumer.

Usually not useful to blindly retry:

- invalid request,
- authentication/authorization failure,
- unsupported media format,
- deterministic schema/validation failure,
- corrupted input that will fail identically,
- business rule rejection.

The question is:

> Is another attempt likely to have a different outcome?

---

# 3. Idempotency before retries

Suppose:

```text
POST /jobs/{id}/finalize
```

succeeds but the response is lost.

A retry must not:

- bill twice,
- create two transcript rows,
- emit duplicate final events,
- increment counters twice.

Use:

```text
idempotency key
unique constraint
guarded state transition
upsert
business operation ID
```

At-least-once delivery without idempotency is a correctness bug waiting for a network hiccup.

---

# 4. Exponential backoff

A simple schedule:

```text
base = 1 second

attempt 1 failure
wait 1s

attempt 2 failure
wait 2s

attempt 3 failure
wait 4s

attempt 4 failure
wait 8s
```

Usually cap it:

```text
wait = min(cap, base × 2^attempt)
```

Otherwise waits become impractically large.

---

# 5. Why jitter matters

Imagine 10,000 workers fail at the same moment.

Without jitter:

```text
T+1s → 10,000 retries
T+3s → 10,000 retries
T+7s → 10,000 retries
```

You created synchronized traffic waves.

With jitter:

```text
retry time = random(0, backoff_cap_for_attempt)
```

attempts spread over time.

The exact jitter algorithm matters less in Week 7 than the mental model:

> correlated retries recreate the overload condition.

---

# 6. Retry budget

Do not only define:

```text
max_retries = 3
```

Define a budget:

```text
maximum attempts
maximum elapsed time
maximum backoff
which layer retries
which error classes
```

Example:

```yaml
ai_transcription:
  max_attempts: 4
  max_elapsed: 90s
  retry_on:
    - timeout
    - 429
    - 500
    - 503
  never_retry:
    - invalid_audio
    - auth_error
  backoff: exponential
  jitter: full
```

---

# 7. Retry at one layer when possible

Consider:

```text
API retries Service A 3×
Service A retries Service B 3×
Service B retries DB 3×
```

Worst-case attempts multiply.

```text
3 × 3 × 3 = 27
```

Nested retries are a classic failure amplifier.

Choose the layer that has enough context to make the best retry decision.

---

# 8. Honor server feedback

For rate limiting:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

A well-behaved client should generally respect the server's retry guidance rather than immediately hammering it again.

For provider-specific APIs, classify errors from actual documentation rather than treating every non-200 identically.

---

# 9. Retry + DLQ

For asynchronous work:

```text
chunk attempt
   ↓ fails transiently
retry with backoff
   ↓
retry budget exhausted
   ↓
DLQ / FAILED_REQUIRES_ACTION
```

DLQ is useful when:

- automatic recovery is exhausted,
- the message/input needs inspection,
- replay should be controlled,
- you need to preserve failure context.

DLQ should include:

```text
message/job ID
failure class
attempt count
last error
timestamps
pipeline version
correlation/trace ID
```

---

# 10. Transcription retry matrix

Fill this in:

| Failure | Retry? | Backoff | Max attempts | Idempotency mechanism | Final state |
|---|---|---|---:|---|---|
| AI `429` | ? | ? | ? | ? | ? |
| AI `401` | ? | ? | ? | ? | ? |
| R2 `503` | ? | ? | ? | ? | ? |
| R2 `NoSuchKey` | ? | ? | ? | ? | ? |
| PostgreSQL serialization conflict | ? | ? | ? | ? | ? |
| Unsupported codec | ? | ? | ? | ? | ? |
| Worker crash before ACK | broker redelivery | broker delay | ? | ? | ? |

---

# Exercise — stop the retry storm

Scenario:

```text
200 workers
AI provider begins returning 503
all workers retry immediately
```

Design:

1. timeout,
2. retry classification,
3. exponential backoff,
4. jitter,
5. concurrency reduction,
6. circuit breaker interaction,
7. queue behavior,
8. user-visible job status,
9. final DLQ policy.

Then answer:

> At what point should the system stop trying to “help” automatically?

---

# Break it 💥

1. SDK already retries twice and your wrapper retries three times. How many attempts can happen?
2. `POST` operation succeeded but response timed out. What makes retry safe?
3. 10,000 mobile clients all use identical 1/2/4-second backoff without jitter.
4. Retry queue has no maximum age.
5. A permanent validation error is retried forever.

---

# Retrieval quiz

1. Why can retries decrease reliability?
2. What is exponential backoff?
3. What problem does jitter solve?
4. Why cap backoff?
5. Difference between max attempts and max elapsed retry time?
6. Why are nested retries dangerous?
7. Why does idempotency belong in a retry discussion?
8. What should happen after automatic retry budget exhaustion?

## Exit criterion

You can write a retry policy that names **error class, idempotency, max attempts, max elapsed time, backoff, jitter and terminal behavior**.
