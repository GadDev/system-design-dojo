# Distributed Processing Architecture Decision Record

## Decision

Short statement of the selected design.

## Context

What large workload are we splitting and why?

## Workload assumptions

```text
parent workload size:
arrival rate:
SLO:
provider/compute limits:
```

## Unit of work

```text
chunk definition:
identity:
pipeline version:
```

## Partition strategy

```text
target size/duration:
min/max:
boundary strategy:
overlap:
```

## Fan-out

How children are created and published.

## Concurrency policy

```text
global:
per tenant:
per parent:
per provider:
```

## Delivery semantics

```text
at-most-once / at-least-once / other:
ACK point:
retry policy:
DLQ policy:
```

## Idempotency

What duplicate business effects are possible and how are they suppressed?

## Durable workflow state

What is persisted and where?

## Fan-in barrier

What exact condition permits aggregation?

## Merge algorithm

```text
ordering:
overlap handling:
missing-child behavior:
output identity:
retry behavior:
```

## Race conditions

| Race | Invariant | Protection |
|---|---|---|
| | | |

## Lock decision

Do we need a lock? Why are CAS/constraints insufficient?

If yes:

```text
lock service:
lease:
renewal:
fencing:
partition behavior:
```

## Cancellation semantics

What happens to queued, running and completed children?

## Orchestrator choice

```text
DB+queue / Celery / Temporal / managed workflow / other
```

Why?

## Observability

Metrics, logs, traces and workflow inspection.

## Cost

Compute, provider, retries, storage and orchestration overhead.

## Alternatives considered

What did we not choose and why?

## Failure modes

Top five failures and recovery behavior.

## Review triggers

What measurements/events would force reconsideration?
