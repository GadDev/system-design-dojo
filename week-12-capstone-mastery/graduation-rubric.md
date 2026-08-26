# System Design Ninja — Graduation Rubric 🥷

Score 0–3 per dimension.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Scope | unclear | partial | bounded | priorities + exclusions crisp |
| Estimation | absent | arithmetic only | useful | drives architecture |
| API | absent | generic | coherent | lifecycle/retry semantics explicit |
| Data | generic | tables only | access-pattern based | authority/invariants/consistency explicit |
| Architecture | cargo cult | incomplete | coherent | simple + evolutionary |
| Scale | “add servers” | generic | bottlenecks identified | metric-driven staged path |
| Async | confused | queue box | delivery/retry model | idempotent orchestration + backpressure |
| Reliability | ignored | retries | bounded recovery | failover/degradation/reconciliation |
| Observability | ignored | logs | useful metrics | SLO-led logs+metrics+traces |
| Consistency | ignored | generic | per-operation | per-fact authority + convergence |
| Security/privacy | ignored | auth only | sensible | data lifecycle + abuse + tenant isolation |
| Cost | ignored | mention | drivers identified | architecture choices tied to unit economics |
| Tradeoffs | declarations | one-sided | alternatives | decision + cost + trigger |
| Communication | chaotic | reactive | clear | leads ambiguity collaboratively |

Maximum: **42**.

## Graduation

```text
36–42 → strong first-pass system-design mastery
30–35 → solid; target weak categories
24–29 → repeat advanced mocks
<24   → revisit Weeks 1–10 where gaps cluster
```

## Final test

You should be able to defend an unfamiliar design for 45–60 minutes without:

- immediately naming technologies,
- hiding assumptions,
- ignoring failures,
- treating all data as equally consistent,
- treating scaling as “Kubernetes,”
- or producing a diagram with no explanation of tradeoffs.
