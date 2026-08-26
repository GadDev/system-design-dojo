# System Design Mock Scoring Rubric — 30 Points

Score yourself after the design, not during it.

| Area | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Requirements | jumped in | weak scope | mostly clear | crisp priorities + exclusions |
| Estimation | none | decorative | useful estimates | estimates drive decisions |
| API | missing | vague | usable | retry/lifecycle semantics clear |
| Data model | generic | partial | access-pattern based | invariants + authority clear |
| Architecture | incoherent | over/under-designed | coherent | simple + evolvable |
| Scaling | buzzwords | one bottleneck | multiple stages | metric-driven 10×/100×/1000× |
| Reliability | ignored | generic retries | useful failure handling | bounded retries, idempotency, degradation |
| Tradeoffs | declarations | one-sided | alternatives discussed | requirement→decision→cost→trigger |
| Communication | hard to follow | reactive | structured | leads conversation clearly |
| Time management | incomplete | badly skewed | mostly balanced | complete + useful deep dive |

Maximum: **30**.

## Interpretation

```text
26–30  Strong interview-ready performance
22–25  Good; fix 1–2 weak dimensions
18–21  Inconsistent; more timed mocks
<18    Return to framework drills
```

## Important

Do not optimize only for the score.

Write:

```text
Strongest reasoning moment:
Weakest assumption:
One concept gap:
One communication gap:
One change for next mock:
```
