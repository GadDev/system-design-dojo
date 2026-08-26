# Week 10 Resources & Reading Map 📚

This week is about **pattern selection**, so the sources are intentionally a mix of foundational architecture writing and current vendor-neutral/reference guidance.

Rule:

> Read enough to understand the forces and tradeoffs. Do not copy someone else's target architecture before doing the design exercise yourself.

---

## Day 1 — Modular monolith

### Core reading

1. **Martin Fowler — Microservice Trade-Offs**  
   https://martinfowler.com/articles/microservice-trade-offs.html

Focus on:

- strong module boundaries,
- distribution cost,
- eventual consistency,
- operational complexity,
- the idea of a microservice premium.

Why read it on modular-monolith day?

Because it makes the strongest case for understanding what you give up when you cross a process/network boundary.

2. **Spring Modulith — Overview**  
   https://spring.io/projects/spring-modulith/

Even though our reference implementation is FastAPI/Python, Spring Modulith is a useful concrete example of treating module boundaries, module-level testing and architectural verification as first-class concerns inside one deployable application.

### Book

- **Building Evolutionary Architectures, 2nd Edition** — Ford, Parsons, Kua, Sadalage
  - focus on fitness functions and architecture that can evolve safely.

---

## Day 2 — Microservices

### Core reading

1. **Martin Fowler — Microservices**  
   https://martinfowler.com/articles/microservices.html

2. **Martin Fowler — Microservice Trade-Offs**  
   https://martinfowler.com/articles/microservice-trade-offs.html

3. **Martin Fowler — Microservice Prerequisites**  
   https://martinfowler.com/bliki/MicroservicePrerequisites.html

Focus on:

- independent deployment,
- decentralized data ownership,
- operational maturity,
- why distribution is a cost,
- why boundaries must be understood before extraction.

### Book

- **Building Microservices, 2nd Edition — Sam Newman**
  - service decomposition,
  - data ownership,
  - evolutionary extraction,
  - testing and operations.

---

## Day 3 — Event-driven architecture

### Core reading

1. **Azure Architecture Center — Event-Driven Architecture Style**  
   https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven

Focus on:

- producer/channel/consumer model,
- decoupling,
- independent scale,
- eventual consistency,
- when synchronous request-response is still simpler.

2. Revisit Week 5's queue delivery semantics and Week 9's event-driven consistency material.

### Book

- **Designing Event-Driven Systems — Ben Stopford**
- **Enterprise Integration Patterns — Hohpe & Woolf**

Focus on event channel, message, idempotent receiver, correlation and routing vocabulary.

---

## Day 4 — CQRS

### Core reading

**Azure Architecture Center — CQRS Pattern**  
https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

Focus on:

- simple CRUD as the baseline,
- separate read/write models,
- independent scaling,
- eventual consistency when stores split,
- why CQRS is unsuitable for simple domains.

Important point from the guidance:

> CQRS can be useful without event sourcing, and separate physical databases are an advanced implementation choice rather than the definition of the pattern.

### Book

- **Implementing Domain-Driven Design — Vaughn Vernon**
  - useful for command/query boundaries and aggregates.

---

## Day 5 — Event sourcing

### Core reading

1. **Azure Architecture Center — Event Sourcing Pattern**  
   https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing

Focus on:

- append-only events as system of record,
- rehydration,
- projections/materialized views,
- optimistic stream concurrency,
- snapshots,
- schema evolution,
- the explicit warning that event sourcing introduces significant complexity and should be adopted only when its benefits justify it.

2. **Martin Fowler — Event Sourcing**  
   https://martinfowler.com/eaaDev/EventSourcing.html

Use it for foundational vocabulary, then use the newer Azure guidance for operational tradeoffs.

### Book

- **Designing Data-Intensive Applications, 2nd Edition**
  - logs, event streams, derived data, materialized views.

---

## Day 6 — Saga pattern

### Core reading

1. **AWS Prescriptive Guidance — Saga Pattern**  
   https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/saga-pattern.html

Focus on:

- local transactions,
- coordination across microservices,
- failure/compensation,
- long-running workflows,
- complexity growth as the number of services increases.

2. Revisit Week 9's compensating transaction material.

### Book

- **Microservices Patterns — Chris Richardson**
  - saga choreography,
  - saga orchestration,
  - transactional outbox,
  - database-per-service.

---

# Recommended reading order

```text
Day 1
Fowler microservice trade-offs
→ understand the price of distribution

Day 2
Fowler microservices + prerequisites
→ understand when service extraction earns its keep

Day 3
Azure EDA
→ understand async collaboration

Day 4
Azure CQRS
→ understand read/write asymmetry

Day 5
Azure Event Sourcing + Fowler
→ understand history-as-state

Day 6
AWS Saga
→ understand cross-service business workflows

Day 7
NO new reading first
→ defend your own architecture
→ then compare it with the sources
```

---

# Book focus for the week

## Primary

### Building Microservices, 2nd Edition — Sam Newman

Use for:

- decomposition,
- ownership,
- deployment independence,
- data boundaries,
- migration strategies.

### Building Evolutionary Architectures, 2nd Edition

Use for:

- architectural fitness functions,
- incremental evolution,
- keeping options open without speculative overengineering.

### Designing Data-Intensive Applications, 2nd Edition

Use for:

- logs,
- derived data,
- dataflow,
- consistency implications of distributed architecture.

## Secondary

- **Microservices Patterns — Chris Richardson**
- **Enterprise Integration Patterns — Hohpe & Woolf**
- **Implementing Domain-Driven Design — Vaughn Vernon**

---

# Reading questions

After every source, answer:

```text
What concrete problem is the pattern solving?
What does it make easier?
What does it make harder?
What new failure mode appears?
What data-consistency assumption changes?
Would my transcription system pay this cost today?
What measurable trigger would change my answer?
```

That final question is the architecture muscle we are training.
