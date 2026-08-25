# Lab — Local Redis

## Goal

Run Redis locally and observe keys, TTL, hits/misses, memory, and expiration.

---

# Option A — Docker

```bash
docker run --name system-design-redis \
  -p 6379:6379 \
  -d redis:8
```

Open CLI:

```bash
docker exec -it system-design-redis redis-cli
```

Test:

```bash
PING
```

Expected:

```text
PONG
```

---

# Basic commands

```bash
SET hello world
GET hello
DEL hello
```

---

# TTL

```bash
SET temp value EX 30
TTL temp
```

Wait and repeat:

```bash
TTL temp
GET temp
```

---

# Cache hit / miss stats

Reset stats if this is only a local lab:

```bash
CONFIG RESETSTAT
```

Generate hits/misses:

```bash
SET profile:42 ada
GET profile:42
GET profile:42
GET profile:999
```

Inspect:

```bash
INFO stats
```

Find:

```text
keyspace_hits
keyspace_misses
```

Calculate:

```text
hits / (hits + misses)
```

---

# Memory

```bash
INFO memory
```

Inspect:

```text
used_memory
used_memory_human
used_memory_peak
mem_fragmentation_ratio
```

Do not treat every number as alarming.

This is an observation lab.

---

# Expiration

```bash
SET a 1 EX 20
SET b 2 EX 40
SET c 3

TTL a
TTL b
TTL c
```

Remember:

```text
-1 → key exists but no expiry
-2 → key does not exist
```

---

# Eviction configuration

```bash
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```

For a disposable local lab only, you can experiment:

```bash
CONFIG SET maxmemory 10mb
CONFIG SET maxmemory-policy allkeys-lru
```

Do not copy lab settings into production.

---

# Latency

Basic ping measurement:

```bash
redis-cli --latency
```

Stop with `Ctrl+C`.

For deeper diagnosis, consult the Redis latency documentation.

---

# Cleanup

```bash
docker stop system-design-redis
docker rm system-design-redis
```

If you want to keep it:

```bash
docker start system-design-redis
```

---

# Lab questions

1. What does a hit look like?
2. What does a miss look like?
3. What happens after TTL reaches zero?
4. Difference between `DEL` and expiration?
5. Is Redis latency exactly zero locally?
6. Why is this local environment not representative of a production network?
