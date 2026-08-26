# Service Extraction Scorecard

Use this before extracting a module from the modular monolith.

Score 0–3:

- 0 = no pressure
- 1 = weak
- 2 = meaningful
- 3 = strong

| Dimension | Score | Evidence |
|---|---:|---|
| Independent team ownership | | |
| Different release cadence | | |
| Independent scaling need | | |
| Special runtime/hardware | | |
| Fault-isolation requirement | | |
| Security/compliance boundary | | |
| Domain boundary is stable | | |
| Contract is already explicit | | |
| Data ownership is clear | | |
| CI/CD maturity | | |
| Observability maturity | | |
| On-call/operational ownership | | |

## Distribution-tax checklist

Will extraction introduce:

- [ ] network latency
- [ ] retries/timeouts
- [ ] service authentication
- [ ] API/event versioning
- [ ] eventual consistency
- [ ] distributed tracing
- [ ] separate deployment
- [ ] separate database
- [ ] saga/reconciliation needs
- [ ] cross-service testing

## Decision

### Extract now / strengthen module / defer

Reason:

### Revisit trigger

What measurable condition would change the decision?
