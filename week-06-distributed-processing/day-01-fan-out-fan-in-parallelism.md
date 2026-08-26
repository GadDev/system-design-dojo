# Day 1 — Fan-Out, Fan-In, Concurrency & Parallelism

## Goal

Build the mental model for splitting one logical job into many independently executable units and joining them safely later.

## Timebox

- 20 min — fan-out / fan-in
- 15 min — concurrency vs parallelism
- 15 min — speedup and bottleneck math
- 20 min — transcription exercise
- 10 min — retrieval quiz

---

# 1. Fan-out

**Fan-out** takes one logical unit of work and creates multiple independent units.

```text
Parent Job
   ↓
 ┌─┼─────────────┐
 ↓ ↓             ↓
C1 C2 ...       C90
```

For transcription:

```text
90-minute audio
      ↓
chunk plan
      ↓
90 × 1-minute chunk jobs
```

Fan-out is valuable when the sub-jobs can be processed mostly independently.

Good candidates:

- transcribing independent time ranges,
- resizing many images,
- scanning many files,
- processing independent rows/objects,
- rendering independent video frames or segments.

Bad candidates are workloads where every step requires the previous step's output.

---

# 2. Fan-in

**Fan-in** waits for enough child results to become available and combines them into a parent result.

```text
C1 ─┐
C2 ─┼─→ barrier → merge → final result
C3 ─┤
... │
CN ─┘
```

The phrase “wait for everything, then merge” sounds trivial.

In a distributed system, it immediately raises questions:

- Who decides everything is complete?
- What if completion events arrive twice?
- What if two workers both observe the final count?
- What if a result says `done` but the output blob has not been durably written?
- What if one chunk permanently fails?
- Can partial output be accepted?

Fan-in is a **coordination problem**.

---

# 3. Map / Reduce as a useful mental model

The classic MapReduce model is useful vocabulary even when you are not using Hadoop.

```text
MAP
split work into independent computations

REDUCE
combine intermediate results
```

For this course:

```text
MAP    = chunk transcription
REDUCE = ordered transcript merge
```

Do not confuse the generic idea with one specific MapReduce product.

---

# 4. Concurrency vs parallelism

These words are related but not identical.

## Concurrency

Multiple tasks are **in progress** during overlapping time windows.

A single CPU can run concurrent tasks by switching between them.

## Parallelism

Multiple tasks are **literally executing at the same time** on separate compute capacity.

For a distributed worker pool:

```text
Worker 1 → Chunk 1
Worker 2 → Chunk 2
Worker 3 → Chunk 3
```

that is real parallelism.

## Throughput

How much work finishes per unit of time.

Parallelism is useful only while it increases useful throughput without saturating something else.

---

# 5. Parallelism is not free

Suppose one chunk takes approximately 20 seconds to transcribe.

For 90 chunks:

### Sequential

```text
90 × 20s = 1,800s = 30 minutes
```

### Concurrency = 15

Ignoring overhead:

```text
ceil(90 / 15) × 20s
= 6 × 20s
= 120s
```

Very nice.

But now add reality:

```text
split stage                 15s
queue/scheduling overhead   10s
slowest chunk               45s instead of 20s
merge stage                  8s
provider rate limiting      ???
```

The useful model is closer to:

```text
T_total
≈ T_split
+ fan-out scheduling
+ max(worker waves / stragglers)
+ T_merge
```

The slowest necessary child often determines fan-in time.

---

# 6. Amdahl's Law intuition

If part of your pipeline is inherently serial, adding infinite workers cannot make that part disappear.

For example:

```text
Download     serial-ish
Split        serial-ish
Transcribe   parallel
Merge        serial-ish
```

If splitting and merging together take 90 seconds, the absolute lower bound is already at least 90 seconds even with unlimited transcription capacity.

The lesson:

> Find the parallelizable fraction before buying more workers.

---

# 7. Why chunk retries reduce blast radius

Compare two failure domains.

## Monolithic job

```text
90-minute video
      ↓
85 minutes processed
      ↓
transient failure
      ↓
retry whole job
```

Potentially enormous wasted work.

## Chunked job

```text
Chunk 37
   ↓
failed
   ↓
retry Chunk 37
```

The already-durable output from chunks 1–36 and 38–90 remains useful.

A one-minute chunk makes the retry unit roughly 1/90 of the original media duration.

That does **not** mean the total failure probability becomes 90× lower. In fact, more tasks can mean more individual opportunities for a transient failure.

The benefit is that **recovery is local**.

That distinction matters.

---

# 8. Failure probability intuition

Suppose each chunk has a 1% chance of needing at least one retry.

For 90 chunks, the probability that at least one chunk needs a retry is:

```text
1 - (0.99 ^ 90)
≈ 59.5%
```

So chunking does not magically remove failures.

It changes their cost:

```text
failure → retry 1 chunk
```

rather than:

```text
failure → retry all prior work
```

This is an excellent system-design distinction.

---

# 9. Fan-out requires a concurrency policy

Do not interpret:

```text
90 chunks
```

as:

```text
launch 90 immediately
```

Concurrency should be bounded by:

- worker capacity,
- AI provider limits,
- CPU/GPU capacity,
- object-storage bandwidth,
- per-user fairness,
- cost budgets,
- database write capacity.

A plausible policy could be:

```text
global concurrent chunks      500
per-tenant concurrent chunks   20
per-parent-job concurrency      10
```

The exact numbers come from measurements.

---

# Exercise — Draw the 90-minute pipeline

Assume:

```text
video duration      = 90 minutes
chunk size          = 60 seconds
chunk count         = 90
worker concurrency  = 15
```

Draw:

1. parent job,
2. split/planning stage,
3. child chunk jobs,
4. queue,
5. worker pool,
6. result store,
7. fan-in barrier,
8. merge stage.

Then answer:

- Which stage is serial?
- Which stage is parallel?
- What resource limits concurrency?
- If chunk 37 fails, what is retried?
- If chunk 90 is 5× slower, what happens to completion latency?

---

# Break it 💥

Predict the behavior when:

1. 90 chunk messages are published twice.
2. Worker 8 dies after writing chunk output but before ACK.
3. The AI provider allows only 30 requests/sec.
4. Chunk 52 takes ten times longer than all others.
5. Parent job is cancelled while 12 chunks are running.

For each, identify whether the problem belongs to:

```text
delivery
idempotency
backpressure
straggler handling
orchestration
```

---

# Retrieval quiz

1. Define fan-out.
2. Define fan-in.
3. Why is fan-in a coordination problem?
4. Difference between concurrency and parallelism?
5. Why does more parallelism stop helping eventually?
6. What does chunking improve about retries?
7. Why can chunking increase the number of observed transient failures while still improving reliability?
8. What is a straggler?
9. Why should concurrency be bounded?
10. Name three possible concurrency limits in the transcription platform.

## Exit criterion

You can explain **why parallelization helps and what it does not solve** without saying “just add workers.”
