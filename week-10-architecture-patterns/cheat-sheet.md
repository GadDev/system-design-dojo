# Week 10 Cheat Sheet — Architecture Patterns

## The master question

```text
What problem exists?
      ↓
Which pattern addresses it?
      ↓
What complexity does it add?
```

---

## Modular monolith

**Use when:**

- one product/team or tightly collaborating teams,
- boundaries can be enforced in code,
- local transactions are valuable,
- independent deployment is not yet necessary.

**Gives:**

- simple deployment,
- cheap in-process calls,
- easier transactions/testing,
- evolutionary boundaries.

**Costs:**

- boundaries require discipline,
- one deployable can become large,
- weak module enforcement can decay.

---

## Microservices

**Use when:**

- independent deployment has clear value,
- teams own stable capabilities,
- workloads need radically different scaling/runtime,
- operational maturity exists.

**Gives:**

- stronger boundaries,
- independent deployment/scaling,
- team autonomy.

**Costs:**

- network failure/latency,
- distributed consistency,
- observability/operations,
- versioned contracts.

```text
Microservice Premium
=
complexity you must earn back with real benefits
```

---

## Event-driven architecture

```text
Producer → Broker → Consumers
```

**Use when:**

- many independent consumers react to one fact,
- asynchronous lag is acceptable,
- producer should not know all consumers.

**Costs:**

- eventual consistency,
- duplicate delivery,
- ordering/schema challenges,
- harder debugging.

Command:

```text
DoSomething
```

Event:

```text
SomethingHappened
```

---

## CQRS

```text
Commands → write model
Queries  → read model
```

**Use when:** reads and writes need materially different models, scale or optimization.

**Does NOT require:**

- microservices,
- separate DBs,
- event sourcing.

Full CQRS with separate read store introduces eventual consistency.

---

## Event sourcing

```text
Event stream = source of truth
       ↓ replay
Current state
       ↓
Projections
```

**Use when:**

- audit/history/replay is core domain value,
- intent/change history matters,
- temporal reconstruction matters.

**Costs:**

- event schema evolution,
- projection complexity,
- replay/snapshot logic,
- unfamiliar mental model,
- expensive migration in/out.

Event sourcing ≠ event-driven architecture.

---

## Saga

```text
T1 → T2 → T3
      failure
C1 ← C2
```

**Use when:** one business workflow spans independently committed services.

### Choreography

```text
Events trigger next steps
```

### Orchestration

```text
Durable coordinator directs steps
```

Compensation is **business correction**, not rollback.

---

## Pattern relationships

```text
Modular monolith
    can use events
    can use CQRS
    can use sagas internally

Microservices
    often use EDA
    may require sagas
    do not require event sourcing

CQRS
    often pairs with event sourcing
    but does not require it

Event sourcing
    usually needs projections
    often leads to CQRS-style reads
```

---

## Extraction triggers

```text
team ownership
independent deployment
runtime difference
scale difference
security boundary
fault isolation
stable domain boundary
operational readiness
```

---

## Red flags 🚩

```text
“Every table becomes a service.”
“We use Kafka because we're event-driven.”
“CQRS means two databases.”
“Event sourcing is just audit logs.”
“Sagas provide distributed ACID.”
“Microservices automatically scale better.”
“Monolith means bad architecture.”
```

---

## Transcription default

```text
React
 ↓
FastAPI modular monolith
 ↓
PostgreSQL

Queue
 ↓
Independent workers
```

Keep this until a measured requirement justifies something more complicated.
