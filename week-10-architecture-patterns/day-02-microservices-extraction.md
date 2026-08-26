# Day 2 — Microservices: Pay the Distribution Tax Only When You Need the Benefit

## Goal

Understand what microservices actually buy you, what they cost, and which evidence justifies extracting a module from a modular monolith.

## Timebox

- 20 min — what makes a service a service
- 25 min — benefits vs distribution tax
- 20 min — service boundaries and data ownership
- 20 min — extraction scorecard
- 10 min — break-it drill + quiz

---

## 1. A microservice is not “a small folder in Docker”

Useful characteristics include:

- independently deployable,
- owns a coherent business capability,
- has an explicit contract,
- can evolve without coordinated releases with every neighbor,
- owns its state or has clear authority boundaries,
- is operated as an independent runtime.

If five “services” must always deploy together, share private tables and fail together, you may have built a **distributed monolith**.

---

## 2. What microservices can solve

### Independent deployment

If Billing changes 20 times/month but Jobs changes twice, separate deployment may reduce coordination.

### Independent scaling

Your GPU transcription workers may need:

```text
GPU nodes
queue-depth autoscaling
high memory
```

while the API needs:

```text
cheap CPU replicas
low latency
high request concurrency
```

These workloads already deserve separate processes even before becoming separate business services.

### Team autonomy

If a stable team owns Billing end-to-end, a service boundary can align code, data, deployment and responsibility.

### Fault isolation

A failing notification service need not take down job submission—if the architecture truly isolates the dependency.

---

## 3. The distribution tax

You replace:

```python
result = billing.calculate(job)
```

with something like:

```text
DNS
TLS
HTTP/gRPC/broker
serialization
network latency
timeouts
retries
partial failure
observability
versioning
authentication
eventual consistency
```

That is not automatically bad.

It is simply **not free**.

Martin Fowler describes this as the microservice premium: distribution, eventual consistency and operational complexity need to be justified by the benefits of stronger boundaries and independent deployment.

---

## 4. Service boundary ≠ table boundary

A service should normally own a business capability and its authoritative data.

Bad split:

```text
UserService
JobService
ChunkService
TranscriptLineService
```

just because tables exist.

Better candidates:

```text
Identity
Transcription Processing
Billing / Usage
Notifications
```

because they have distinct capabilities, workloads or ownership.

---

## 5. Extraction signals

Score a module on evidence such as:

### Team pressure

- separate team ownership,
- frequent coordination conflicts,
- independent release cadence needed.

### Runtime pressure

- radically different scaling profile,
- special hardware/runtime,
- different availability target,
- high resource isolation need.

### Domain maturity

- stable boundary,
- clear inputs/outputs,
- well-understood ownership.

### Operational readiness

- CI/CD automation,
- observability,
- service authentication,
- on-call ownership,
- deployment and rollback tooling.

If the domain boundary is unclear, splitting early can freeze the wrong boundary behind a network API.

---

## 6. Candidate: transcription processing

For your SaaS, processing is a strong candidate for **runtime independence** early:

```text
API/control plane
       ↓ queue
Transcription workers
```

But ask whether it needs to be a full independent business microservice or simply an independently deployed worker application sharing the same domain code/data contracts.

Those are different steps.

A reasonable evolution:

```text
Stage 1
one repo + modular monolith + worker process

Stage 2
same repo + separately deployed worker service

Stage 3
separate ownership/data/API only if pressure justifies it
```

---

## 7. Database-per-service is powerful—and expensive

If Billing owns its own database:

```text
Jobs DB         Billing DB
   │                │
   └── event/API ───┘
```

then you gain stronger ownership.

You also lose easy joins and cross-module local transactions.

Now you need:

- API composition,
- events,
- read projections,
- sagas,
- reconciliation,
- or some combination.

That is why Week 9 came before Week 10. 😄

---

## 8. Strangler-style extraction

A practical extraction process:

```text
1. Establish internal module boundary.
2. Define stable contract.
3. Route all callers through it.
4. Move runtime behind that contract.
5. Move data ownership if justified.
6. Remove old implementation.
```

Avoid:

```text
“Rewrite entire system as microservices.”
```

Evolution is usually safer than revolution.

---

## Exercise — Extraction scorecard

Score these candidates 0–3:

| Candidate | Team autonomy | Scale difference | Runtime difference | Boundary maturity | Failure isolation | Operational readiness |
|---|---:|---:|---:|---:|---:|---:|
| Billing | | | | | | |
| Transcription workers | | | | | | |
| Notifications | | | | | | |
| Jobs | | | | | | |
| Results | | | | | | |

Then answer:

> Which single component would you extract first, if any?

Your answer must include the pain it solves.

---

## Break it 💥

Explain the problem with each design:

1. Ten services share the same database tables directly.
2. Every API request makes six sequential service calls.
3. A “microservice” cannot deploy unless three neighbors deploy too.
4. The team has no distributed tracing or automated deployment.
5. The domain is still changing weekly, but service boundaries are frozen.
6. A service exists solely because one database table exists.

---

## Retrieval quiz

1. What does independent deployment actually mean?
2. Name three parts of the distribution tax.
3. Why can microservices improve module boundaries?
4. Why can extracting too early make boundaries worse?
5. What is a distributed monolith?
6. Why might transcription workers be deployed independently without immediately becoming a fully isolated business service?
7. When does database-per-service create consistency complexity?

## Exit criterion

You can give a stronger reason for a service extraction than “it scales better.”
