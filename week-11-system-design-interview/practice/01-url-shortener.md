# Practice 01 — URL Shortener 🟢

## Prompt

> Design a URL shortening service like Bitly.

## Do not read further until you have scoped the problem.

---

## Suggested requirement cards

Reveal only if needed:

- 10M new links/day
- 1B redirects/day
- custom aliases optional
- links may expire
- target URLs may be editable only for authenticated owners
- redirect p95 target: <100 ms in primary markets

## Main design tensions

```text
read-heavy traffic
hot keys
cache freshness
expiration
ID generation
redirect semantics
```

## Expected components to consider

Not mandatory:

```text
API
PostgreSQL/KV store
index on short_code
Redis
CDN/edge for extreme hot reads
analytics event pipeline
```

## Deep-dive questions

1. How is `short_code` generated?
2. What prevents collisions?
3. What happens for an expired URL that is still cached?
4. What if one celebrity short link receives 300k RPS?
5. `301` vs temporary redirect — what product tradeoff appears?
6. What is authoritative for redirect target?

## 10× challenge

Assume the top 0.01% of links receive 60% of redirects.

What breaks first?

## Tradeoff to defend

> PostgreSQL + Redis first, rather than a globally sharded KV store on day one.
