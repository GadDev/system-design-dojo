# Consistency Architecture Decision Record

## Decision

```text
Title:
Status: proposed / accepted / superseded
Date:
Owner:
```

## Context

Which business workflow/fact are we designing?

## Invariants

```text
1.
2.
3.
```

## Authority map

| Fact | Authoritative store | Derived copies | Why |
|---|---|---|---|
| | | | |

## Consistency contract

| Operation/read | Required guarantee | Max staleness | Behavior if guarantee unavailable |
|---|---|---:|---|
| | | | |

## Concurrency control

```text
Version / ETag:
Guarded state transition:
Unique constraint:
Pessimistic lock (if any):
Conflict response:
Retry behavior:
```

## Distributed transaction boundary

```text
Local transactional resources:
External/non-transactional resources:
Why one ACID transaction is/is not possible:
2PC considered?:
Decision:
```

## Event propagation

```text
Outbox:
Event types:
Aggregate key/version:
Ordering scope:
Inbox/dedup:
Schema versioning:
```

## Saga / compensation

```text
Step:
Local commit:
Forward retry:
Compensation:
Point of no return:
Manual recovery:
```

## Replica/read strategy

```text
Primary-only operations:
Replica-safe operations:
Read-your-writes strategy:
Monotonic-read strategy:
Lag SLO:
```

## Reconciliation

```text
Invariant checks:
Schedule/trigger:
Auto-repair cases:
Quarantine cases:
Alert/manual cases:
```

## Metrics

```text
optimistic_conflict_total
projection_lag_seconds
reconciliation_backlog
artifact_db_mismatch_total
outbox_oldest_unpublished_seconds
duplicate_event_total
```

## Alternatives rejected

What stronger/weaker consistency designs were considered and why rejected?

## Review trigger

What latency, incident, scale or product requirement would make us revisit this decision?
