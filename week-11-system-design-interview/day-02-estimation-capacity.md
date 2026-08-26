# Day 2 — Back-of-the-Envelope Estimation

## Goal

Estimate enough to reveal the dominant scale and likely bottlenecks — without pretending your napkin arithmetic is a capacity test.

## Timebox

- 15 min — estimation mindset
- 20 min — QPS/storage/bandwidth formulas
- 20 min — worked examples
- 15 min — estimation drill
- 5 min — retrieval quiz

---

# 1. Why estimate?

You estimate to answer questions like:

```text
Do I need sharding?
Could one PostgreSQL instance plausibly handle this?
Is CDN bandwidth dominant?
How much storage accumulates per year?
How many workers are needed to keep up?
```

You do **not** estimate to produce fake precision such as:

```text
We require exactly 3,842.71 servers.
```

---

# 2. Useful formulas

## Average requests per second

```text
average RPS
=
requests per day / 86,400
```

Peak often needs an assumption:

```text
peak RPS
≈
average RPS × peak factor
```

Use 2×, 5×, 10× only as an explicit assumption, never as a law of nature.

---

## Storage growth

```text
storage/day
=
objects/day × average object size
```

Then:

```text
annual raw storage
≈
storage/day × 365
```

Add replication/encoding/metadata separately if relevant.

---

## Bandwidth

```text
bits/sec
=
bytes/sec × 8
```

Example:

```text
50,000 downloads/sec
× 200 KB
≈ 10 GB/sec
≈ 80 Gbit/sec
```

That strongly suggests CDN/edge delivery matters.

---

## Cache origin load

```text
origin QPS
=
total QPS × (1 - cache hit ratio)
```

Example:

```text
100,000 RPS
99% cache hit
→ 1,000 origin RPS
```

---

## Worker concurrency

Little's-Law-style intuition:

```text
concurrency
≈
throughput × average processing time
```

If you need:

```text
70 chunks/sec
```

and each takes:

```text
15 sec
```

then average concurrent processing is roughly:

```text
70 × 15 = 1,050 chunks
```

before headroom.

---

# 3. Work from the dominant resource

For a URL shortener:

```text
RPS + hot reads
```

may dominate.

For Dropbox:

```text
bytes + metadata operations + sync conflicts
```

may dominate.

For video transcription:

```text
media hours + GPU/AI processing + storage/network
```

may dominate.

Different units reveal different architectures.

---

# 4. Worked example — URL shortener

Assume:

```text
10M new links/day
1B redirects/day
```

Average redirect RPS:

```text
1,000,000,000 / 86,400
≈ 11,600 RPS
```

Assume 5× peak:

```text
≈ 58,000 RPS peak
```

With 99% cache hit:

```text
≈ 580 DB reads/sec
```

This tells you why a cache can dramatically change database pressure.

---

# 5. Worked example — 100k media hours/day

Suppose a future transcription platform processes:

```text
100,000 media hours/day
```

One-minute chunks:

```text
100,000 × 60
= 6,000,000 chunks/day
```

Average chunk arrival:

```text
6,000,000 / 86,400
≈ 69.4 chunks/sec
```

If each one-minute chunk takes 15 seconds to transcribe:

```text
69.4 × 15
≈ 1,041 concurrent chunk executions
```

At a 3× peak:

```text
~3,125 concurrent executions
```

The value is not “the answer.”

The value tells you:

> Worker/GPU capacity, provider quotas, queue depth, and cost are first-class design concerns.

---

# 6. Estimation order

A useful order:

```text
Users / workload volume
      ↓
Read/write operations
      ↓
Average + peak throughput
      ↓
Data size + retention
      ↓
Bandwidth
      ↓
Concurrency / compute
```

Only calculate values that influence a design decision.

---

# Exercise

Estimate for a file-upload service:

```text
5M DAU
2% upload each day
average file = 800 MB
peak = 4× average
30-day raw retention
```

Calculate:

1. uploads/day,
2. raw bytes/day,
3. 30-day raw storage,
4. average upload starts/sec,
5. peak upload starts/sec,
6. what is *not* captured by these numbers.

Spoiler: average upload-start RPS can be modest while network ingress is enormous.

---

# Common mistakes

- treating average traffic as peak traffic,
- ignoring read/write ratio,
- estimating storage but not retention,
- estimating requests but not bytes,
- forgetting background work,
- using provider limits as universal truths,
- adding sharding because the number sounds “large.”

---

# Retrieval quiz

1. Why estimate in system design?
2. Formula for average RPS?
3. Why multiply by a peak factor?
4. What does cache hit ratio do to origin load?
5. Why can bandwidth dominate while API RPS remains small?
6. What does `throughput × duration` approximate?

## Exit criterion

You can produce 3–5 useful order-of-magnitude calculations in five minutes and connect each calculation to an architectural implication.
