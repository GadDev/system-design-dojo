# Week 6 Labs

These labs intentionally avoid hiding distributed-processing mechanics behind a large framework.

## 1. `fanout_simulator.py`

Simulates:

- N chunk tasks,
- bounded concurrency,
- random service times,
- transient failures,
- child retries,
- fan-in timing.

Run:

```bash
python fanout_simulator.py --chunks 90 --concurrency 15 --failure-rate 0.05
```

Observe:

- total completion time,
- retry count,
- slowest child,
- difference between sequential and parallel execution.

## 2. `race_condition_demo.py`

Uses SQLite transactions/unique constraints to demonstrate why an invariant can be safer than an in-memory “check then act.”

Run:

```bash
python race_condition_demo.py
```

## 3. `chunk_size_calculator.py`

Compare chunk sizes for a long video.

```bash
python chunk_size_calculator.py --duration-minutes 90
```

## 4. `orchestrator_simulator.py`

A tiny durable parent/child workflow simulation using SQLite.

It demonstrates:

```text
plan children
process concurrently
retry one failed child
claim merge with a guarded transition
reconstruct state from DB
```

Run:

```bash
python orchestrator_simulator.py
```

The lab is educational, not production infrastructure.
