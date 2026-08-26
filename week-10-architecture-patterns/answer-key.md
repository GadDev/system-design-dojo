# Week 10 Answer Key

Use this only after attempting the review.

## Core answers

1. **Monolith vs big ball of mud:** monolith describes deployment shape; big ball of mud describes poor internal structure/coupling.
2. **Modular monolith:** explicit domain modules, controlled dependencies, clear ownership/contracts inside one deployable.
3. **Domain modules:** align code with business capabilities and reduce cross-domain knowledge.
4. **Public contract:** the deliberately exposed commands/queries/events other modules may depend on.
5. **Cycles:** they make modules mutually dependent and hard to reason about or extract.
6. **Shared DB:** yes; logical ownership can still prevent arbitrary cross-module mutation.
7. **Internal events:** reduce direct coupling while preserving simple deployment.
8. **Independent deployment:** a service can be released without requiring coordinated deployment of neighbors.
9. **Benefits:** independent deployment, independent scaling, stronger boundaries, team autonomy, runtime diversity, fault isolation.
10. **Distribution costs:** latency, partial failure, retries/timeouts, eventual consistency, observability, contract versioning, operational overhead.
11. **Microservice premium:** the productivity/operational cost that must be repaid by benefits in a sufficiently complex context.
12. **Distributed monolith:** many processes with tight coupling, shared internals or coordinated deploys, but all the distributed-systems costs.
13. **Table-per-service:** tables are storage details, not business capabilities.
14. **Extraction triggers:** separate team, release cadence, scaling/runtime difference, compliance/fault isolation, stable boundary, operational readiness.
15. **Early extraction:** freezes uncertain domain boundaries behind expensive network/data contracts.
16. **Command vs event:** command asks for an action; event announces a fact that happened.
17. **EDA benefit:** producer need not know all consumers; consumers scale/evolve independently.
18. **Eventual consistency:** consumers process asynchronously after the authoritative change.
19. **Outbox:** prevents committed business state from losing publication intent.
20. **Idempotency:** at-least-once delivery can produce duplicates.
21. **Stable events:** persistence internals create brittle coupling.
22. **Sync is better:** when caller needs immediate result/strong consistency and the workflow is simple.
23. **CQRS:** separates command/write responsibilities from query/read responsibilities.
24. **Two DBs:** no.
25. **Event sourcing:** no.
26. **Projection:** precomputes query-specific representation, reducing join/aggregation cost.
27. **Projection lag:** user can observe stale state after a successful command.
28. **CQRS signs:** divergent read/write models, huge read/write asymmetry, expensive queries, independent read scaling.
29. **CRUD signs:** simple domain, low traffic, one model serves both well.
30. **Event sourcing authority:** append-only event stream.
31. **Rehydration:** rebuild aggregate state by replaying events.
32. **Snapshots:** avoid replaying an extremely long stream every time.
33. **Projections:** event streams are poor general-purpose query models.
34. **Stream concurrency:** append only if expected version still matches.
35. **Schema evolution:** historical events remain part of the source of truth for years.
36. **ES vs EDA:** EDA is collaboration using events; ES is persistence where events are authoritative state history.
37. **Saga:** coordinates one business workflow across multiple local transactions/services.
38. **Choreography vs orchestration:** event reactions vs explicit workflow coordinator.
39. **Compensation:** a new business action that semantically corrects earlier work; it is not restoring RAM/database state atomically.
40. **Idempotent saga steps:** retries/redelivery must not duplicate financial or state effects.

---

## Scenario guidance

### A — GPU workers

You need independent runtime/deployment much sooner than you necessarily need a fully isolated business microservice. A separately deployed worker app consuming a queue may solve the pressure with less complexity.

### B — completion consumers

Events are a strong fit if Billing, email, analytics and search can react independently and tolerate brief lag. Keep the authoritative job transition local/transactional.

### C — job history

A sensible investigation order:

```text
measure query
→ indexes/query tuning
→ cache if repeated and safe
→ projection/read model
→ CQRS if asymmetry persists
→ service extraction only for additional ownership/runtime reasons
```

### D — billing audit

Start with the simplest mechanism satisfying the requirement. An immutable ledger may provide auditability without making events the aggregate source of truth. Event sourcing is justified when replay/reconstruction/intent history and derived projections are first-class domain needs.

### E — cancellation

Inside one monolith, local transactions and direct coordination can cover much of the workflow. Once Jobs, Billing and ML own separate transactions, partial success is unavoidable and a saga provides explicit forward/compensating workflow semantics.

---

## Smell guidance

1. Growth alone does not identify a service boundary or bottleneck.
2. Storage decomposition is not domain decomposition.
3. CQRS is a logical separation, not a mandatory tool stack.
4. Publishing events does not make events the persistence source of truth.
5. Expensive computation cannot literally be rolled back; compensation is business-specific.
6. Shared private tables undermine service autonomy.
7. Auditability can often be achieved more simply than full event sourcing.
8. An eventually consistent projection is inappropriate if the use case requires authoritative current financial state.
