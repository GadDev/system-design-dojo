# Week 9 Labs

These labs intentionally use small local simulations so the **consistency mechanics are visible** before a framework abstracts them away.

## 1. Optimistic locking

```bash
python optimistic_locking_demo.py
```

Two actors read the same version and race to update. One conditional update wins; the other gets a conflict.

## 2. Replica lag simulation

```bash
python replica_lag_simulator.py
```

Shows how a successful primary write can be followed by a stale replica read and how a client can enforce monotonic display.

## 3. Durable partial-success reconciliation

```bash
python reconciliation_demo.py
```

Simulates:

```text
artifact write succeeds
DB finalization fails
message redelivers
```

The second attempt detects the deterministic artifact and repairs state without recomputing expensive work.

## 4. Saga simulator

```bash
python saga_simulator.py
```

A multi-step workflow fails during billing and executes compensating actions.

## 5. PostgreSQL reference schema

`consistency_schema.sql` contains:

- version columns,
- state constraints,
- outbox,
- consumer inbox,
- unique logical chunk identity,
- reconciliation-friendly metadata.
