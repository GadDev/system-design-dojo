# Cache Decision Record

## Decision

```text
Use cache / Do not use cache / Revisit later
```

## Resource / endpoint

```text
GET /...
```

## Context

What does the endpoint/resource do?

## Source of truth

```text
PostgreSQL / object storage / external API / ...
```

## Read pattern

```text
QPS:
repetition:
hot/cold distribution:
```

## Write pattern

```text
writes/sec:
who writes:
```

## Origin cost

```text
p95 latency:
CPU/query cost:
connection pressure:
external cost:
```

## Freshness requirement

```text
maximum acceptable stale window:
read-your-own-write needed? yes/no
```

## Cache strategy

```text
cache-aside / other
```

## Key

```text
namespace:version:id
```

## Value

What is cached?

## TTL

```text
TTL:
why:
jitter:
```

## Invalidation

```text
trigger:
behavior if invalidation fails:
```

## Negative caching

```text
yes/no
TTL:
abuse risk:
```

## Failure behavior

If Redis is:

```text
down:
slow:
cold:
```

What does the API do?

## Origin protection

```text
fallback concurrency limit:
circuit breaker:
rate limit:
headroom:
```

## Hot-key strategy

What if one key receives 50% of traffic?

## Capacity

```text
key count:
average value:
estimated memory:
replication/headroom:
```

## Observability

Track:

```text
hit ratio
cache latency
origin QPS
origin latency
evictions
timeouts
fallbacks
hot keys
```

## Alternatives considered

- no cache
- DB optimization/index
- read replica
- CDN
- local L1
- materialized/derived data
- object storage

## Tradeoffs

What gets better?

What gets harder?

## Review trigger

What measurement or scale would cause us to revisit this decision?
