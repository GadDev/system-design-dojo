# Practice 03 — Distributed Rate Limiter 🟢

## Prompt

> Design a rate limiter for a public API.

## Requirement cards

- per-user and per-IP rules
- some endpoint-specific limits
- 200k RPS global traffic
- rules change without deploy
- limiter should add very low latency

## Main lesson

```text
correctness vs availability vs latency
```

## Deep dive

Compare:

```text
fixed window
sliding window
sliding log
token bucket
```

Then:

```text
local limiter
vs
distributed Redis-backed limiter
vs
hybrid
```

Questions:

- What if Redis is unavailable?
- Fail open or closed?
- How do hot tenants affect Redis?
- How do regions coordinate?
- Do quotas need exact global consistency?
