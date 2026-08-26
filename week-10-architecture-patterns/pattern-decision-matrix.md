# Architecture Pattern Decision Matrix

This is a **reasoning aid**, not a scoring algorithm.

| Pattern | Primary problem | Strong signal | Major benefit | Major cost | Avoid when |
|---|---|---|---|---|---|
| Modular monolith | Need structure without distribution | One product/team, evolving domain | Simple ops + strong local cohesion | Boundary discipline | Independent deployment is truly blocking teams |
| Microservices | Independent ownership/deployment/runtime | Stable capability + separate team/scale | Autonomy + strong boundary | Distribution + ops + consistency | Domain unclear / ops immature |
| Event-driven | Many independent reactions to facts | Multiple async consumers | Producer/consumer decoupling | Eventual consistency + debugging | Simple request/response is enough |
| CQRS | Reads and writes need different models/scale | Read/write asymmetry | Purpose-built read/write models | Projection lag + duplication | CRUD already works |
| Event sourcing | History/replay is core state value | Audit + reconstruction + temporal domain | Full immutable history | Deep persistence/evolution complexity | Audit table/ledger is enough |
| Saga | One workflow spans local transactions | Multi-service sequencing/compensation | Explicit distributed business workflow | Intermediate states + compensation complexity | One local transaction can solve it |

## Transcription SaaS default

| Concern | Current recommendation | Why |
|---|---|---|
| Core API | Modular monolith | simplest architecture that preserves domain boundaries |
| Transcription execution | Independent worker runtime | different scale/hardware; queue already provides boundary |
| JobCompleted reactions | Internal events now; broker events when consumers become independent | do not pay broker tax early |
| Job history | PostgreSQL first | measure before CQRS |
| Billing audit | Immutable ledger first | event sourcing only if replay/history becomes core domain requirement |
| Cancellation | Local workflow today | saga only after workflow crosses independently committed services |
