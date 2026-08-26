# Week 10 Labs 🧪

These labs are intentionally small. Their job is to make the architectural idea tangible without hiding it under frameworks.

## Lab 1 — Modular boundary checker

```bash
python module_boundary_checker.py
```

Demonstrates:

- allowed public-module dependencies,
- forbidden imports into another module's internals,
- architecture rules as executable fitness functions.

## Lab 2 — CQRS projection

```bash
python cqrs_projection_demo.py
```

Demonstrates:

- authoritative write model,
- emitted events,
- independently updated read projection,
- temporary projection lag,
- idempotent event application.

## Lab 3 — Event sourcing

```bash
python event_sourcing_demo.py
```

Demonstrates:

- append-only stream,
- expected-version optimistic concurrency,
- aggregate rehydration,
- snapshots,
- projection rebuild.

## Lab 4 — Saga orchestrator

```bash
python saga_orchestrator_demo.py
```

Demonstrates:

- durable saga state,
- local step execution,
- a simulated failure,
- compensating business action,
- idempotent step result tracking.

## What to write after each lab

```text
What problem did the pattern solve?
What new state did the pattern require?
What new failure mode appeared?
Would this be justified in the transcription SaaS today?
```
