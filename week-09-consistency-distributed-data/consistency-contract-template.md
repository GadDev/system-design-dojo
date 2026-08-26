# Consistency Contract Template

Use this before choosing replication, cache, event or database technology.

| Operation / fact | Authority | Required guarantee | Max/target staleness | Conflict rule | Behavior if authority unavailable |
|---|---|---|---:|---|---|
| | | | | | |

## Client-observation guarantees

```text
Read-your-writes required?:
Monotonic reads required?:
Bounded staleness target?:
Per-aggregate ordering required?:
```

## Write conflict policy

```text
Optimistic version / ETag:
Conditional state transition:
Unique constraint:
Pessimistic locking (if any):
Conflict response to caller:
```

## Replica routing

```text
Primary-only reads:
Replica-safe reads:
Post-write primary stickiness/window:
Lag metric/SLO:
```

## Convergence

```text
Derived copies:
Propagation mechanism:
Retry path:
Reconciliation path:
User-visible state during lag:
```
