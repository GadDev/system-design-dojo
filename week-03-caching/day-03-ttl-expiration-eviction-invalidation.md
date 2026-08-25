# Day 3 — TTL, Expiration, Eviction & Invalidation

## Goal

Design freshness and memory policies deliberately instead of choosing `TTL=300` because five minutes "feels normal."

## Timebox

- 20 min — TTL and freshness
- 15 min — expiration vs eviction
- 20 min — invalidation strategies
- 15 min — jitter and synchronized expiry
- 15 min — Redis lab
- 10 min — retrieval quiz

---

# 1. TTL is a freshness boundary

TTL means **time to live**.

Example:

```bash
SET profile:42 '{...}' EX 300
```

The key is eligible to disappear after roughly 300 seconds.

Conceptually:

```text
TTL = upper bound on how long an uninvalidated cached copy may survive
```

That makes TTL a **business correctness choice**, not just a Redis setting.

---

# 2. Start with staleness tolerance

Bad reasoning:

> "Let's use a 5-minute TTL."

Better:

> "Profile updates may take up to 60 seconds to appear, therefore the fallback freshness bound should be ≤60 seconds."

Examples:

| Data | Possible tolerance |
|---|---|
| Static country list | hours |
| Public profile | tens of seconds/minutes |
| Product price | business-dependent |
| Job progress | a few seconds |
| Authz decision | often much stricter |
| Bank balance | usually not something to casually cache with stale semantics |

These are examples, not universal rules.

---

# 3. Short TTL vs long TTL

## Short

```text
freshness ↑
hit ratio potentially ↓
origin traffic ↑
cache churn ↑
```

## Long

```text
hit ratio potentially ↑
origin traffic ↓
staleness risk ↑
memory residency ↑
```

TTL is a tradeoff knob.

---

# 4. TTL is not invalidation

Suppose a profile has:

```text
TTL = 1 hour
```

but the user edits it now.

Waiting an hour may be unacceptable.

So you can combine:

```text
explicit invalidation on write
+
TTL as safety net
```

This is common.

---

# 5. Expiration is not eviction

These solve different problems.

## Expiration

```text
"this key should stop existing after time T"
```

Driven by freshness/lifetime.

## Eviction

```text
"Redis is running out of memory; which key should we remove?"
```

Driven by capacity.

A key can be evicted **before** its TTL expires.

A key can also expire even when memory is plentiful.

---

# 6. Redis memory limits

A cache is finite.

Conceptually:

```text
working set > available memory
↓
eviction
```

Redis supports configurable memory policies such as:

```text
allkeys-lru
allkeys-lfu
allkeys-random
volatile-ttl
noeviction
```

You do not need to memorize every policy.

Know the principle:

> Eviction policy should match workload behavior and Redis's role.

If Redis is purely disposable cache data, an all-keys cache-oriented policy can be reasonable.

If Redis mixes durable-ish application state with cache entries, the design becomes much more dangerous.

Often the cleanest answer is:

```text
separate responsibilities
```

---

# 7. LRU vs LFU intuition

## LRU

Evict items that have not been used recently.

Good mental model:

```text
"recently useful things probably remain useful"
```

## LFU

Prefer retaining items accessed frequently.

Good mental model:

```text
"frequently useful things deserve memory"
```

Neither algorithm magically knows business value.

---

# 8. Invalidation strategies

## TTL-only

```text
write DB
do nothing
wait for expiry
```

Simple.

Potentially stale.

## Explicit delete

```text
write DB
DEL cache key
```

Common cache-aside approach.

## Write-through

Application writes cache and authoritative store in the write path.

Can improve read-after-write freshness but increases coupling.

## Event-driven invalidation

```text
DB/business update
↓
event
↓
cache invalidator
```

Useful across services.

Introduces asynchronous delivery and event-failure questions.

---

# 9. The famous hard problem

A classic joke says there are two hard things in computer science:

```text
cache invalidation
naming things
off-by-one errors
```

😄

The joke survives because invalidation combines:

- concurrency,
- partial failure,
- multiple writers,
- multiple caches,
- uncertain timing.

Do not seek a universal "correct cache strategy."

Start with explicit freshness requirements.

---

# 10. Synchronized expiration

Suppose one million keys are populated during a deployment:

```text
TTL = 300 seconds
```

Five minutes later:

```text
huge number expire together
↓
miss storm
↓
database spike
```

A mitigation is TTL jitter:

```text
base TTL = 300 sec
random jitter = ±30 sec
```

Example:

```python
ttl = 300 + random.randint(-30, 30)
```

Now expiration is spread over time.

Jitter reduces synchronized behavior.

---

# 11. TTL must respect domain expiration

URL shortener example:

```text
link expires in 43 seconds
```

Do not cache it for:

```text
300 seconds
```

A safer cache TTL is:

```text
min(normal_cache_ttl, seconds_until_link_expiry)
```

Otherwise the cache may resurrect an expired link.

This is a beautiful example of **cache TTL inheriting a domain constraint**.

---

# 12. Absolute vs sliding expiration

## Absolute

Expires after a fixed time regardless of access.

```text
created at 12:00
TTL 10m
expires ~12:10
```

## Sliding

Refresh expiration when accessed.

Useful for some session-style data.

Potential danger:

```text
a hot key may live forever
```

For ordinary cache-aside, absolute TTL is easier to reason about.

---

# Lab

Try:

```bash
SET lesson value EX 10
TTL lesson
```

Wait.

Then:

```bash
GET lesson
TTL lesson
```

Experiment with:

```bash
EXPIRE lesson 30
PERSIST lesson
```

Inspect memory/eviction configuration:

```bash
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
INFO stats
```

---

# Exercise — create a freshness policy

For each:

```text
URL redirect
job progress
user profile
completed transcript
pricing configuration
```

write:

```text
TTL:
invalidated by:
acceptable stale window:
behavior on Redis failure:
domain expiration constraint:
```

Do not choose TTL until the stale window is written first.

---

# Break it 💥

1. A 10-minute cache TTL is used for a link that expires in 2 minutes.
2. Redis evicts a key after 30 seconds even though its TTL is 1 hour.
3. All popular keys expire at the exact same second.
4. Database write succeeds and cache invalidation fails.
5. A rarely accessed but very expensive object is constantly evicted by your policy.

What metric or design change would reveal or mitigate each problem?

---

# Retrieval quiz

1. What does TTL bound?
2. Why should staleness tolerance come before choosing TTL?
3. Difference between expiration and eviction?
4. Can a key be evicted before TTL expires?
5. Why combine invalidation with TTL?
6. What is TTL jitter?
7. Why can identical TTLs create load spikes?
8. Explain LRU vs LFU at a high level.
9. Why must a URL cache TTL never outlive the URL's domain expiration?
10. Why is mixing unrelated persistent state and cache data in one Redis instance risky?

## Exit criterion

You can design TTL and eviction policies from **freshness + memory requirements** rather than habit.
