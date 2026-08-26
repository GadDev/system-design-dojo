# Reliability Architecture Decision Record

## Decision

```text
Title:
Status: proposed / accepted / superseded
Date:
Owner:
```

## Context

What user/business workflow are we protecting?

## Dependency map

```text
Caller → Dependency → Operation
```

## Failure modes

| Failure | Impact | Detectability | Frequency/likelihood | Notes |
|---|---|---|---|---|
| | | | | |

## Timeout/deadline

```text
Connection timeout:
Request timeout:
Overall deadline:
How values will be measured/tuned:
```

## Retry policy

```text
Retryable errors:
Non-retryable errors:
Max attempts:
Max elapsed:
Backoff:
Jitter:
Retry-After support:
Retrying layer:
```

## Idempotency

```text
Logical operation ID:
Unique constraint / guarded transition:
Deterministic artifact key:
Duplicate side effects prevented:
```

## Circuit breaker

```text
Scope:
Minimum samples:
Failure threshold:
Slow-call threshold:
Open duration:
Half-open probes:
Behavior while open:
```

## Bulkhead / concurrency limits

```text
Global:
Per dependency:
Per tenant:
Per parent job:
```

## Graceful degradation

```text
Core behavior that remains:
Features disabled/delayed:
User-visible status/message:
```

## Health semantics

```text
Startup:
Liveness:
Readiness:
Drain/shutdown:
```

## RTO / RPO

```text
RTO:
RPO:
Replication/failover mechanism:
Fencing/split-brain prevention:
Failback/rebuild plan:
```

## DLQ / manual recovery

```text
When message enters DLQ:
Owner:
Alert:
Retention:
Inspection:
Redrive safety:
```

## Metrics

```text
timeout rate
retry amplification
retry recovery rate
breaker state
queue age
DLQ depth
failover duration
data-loss/reconciliation checks
```

## Game-day test

```text
Hypothesis:
Fault:
Blast radius:
Expected behavior:
Abort condition:
Recovery proof:
```

## Alternatives rejected

What simpler/more complex mechanisms were considered and why were they rejected?

## Review trigger

What evidence would make us revisit this decision?
