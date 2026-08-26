# Day 2 — Work Partitioning & Chunk-Size Strategy

## Goal

Choose the unit of parallel work deliberately and understand how chunk size affects throughput, retries, context quality, scheduling overhead and cost.

## Timebox

- 20 min — partitioning principles
- 20 min — chunk-size tradeoffs
- 15 min — boundaries and overlap
- 20 min — sizing exercise
- 10 min — retrieval quiz

---

# 1. The partition is the failure domain

When you split work, you are defining the smallest unit that can be:

- scheduled,
- retried,
- timed out,
- cancelled,
- observed,
- billed,
- stored,
- merged.

For transcription:

```text
parent video
    ↓
chunk partitioning
    ↓
child failure domains
```

Chunk size is therefore an architectural decision, not a convenience parameter.

---

# 2. Small chunks vs large chunks

| Smaller chunks | Larger chunks |
|---|---|
| Fine retry granularity | Less orchestration overhead |
| More scheduling flexibility | Fewer messages/rows/results |
| Better load balancing | More context per request |
| More metadata + queue traffic | Larger failure domain |
| More merge boundaries | Worse straggler impact |
| More opportunities for duplicate deliveries | Lower scheduling overhead |

There is no universal ideal chunk duration.

---

# 3. A simple cost model

Let:

```text
D = media duration
S = chunk size
N = number of chunks = ceil(D / S)
O = fixed overhead per chunk
P = processing cost proportional to media duration
```

As `S` gets smaller:

```text
N increases
→ fixed overhead increases
→ retry granularity improves
```

As `S` gets larger:

```text
N decreases
→ overhead decreases
→ failure/straggler blast radius grows
```

You are balancing these effects.

---

# 4. Start with a hypothesis, then measure

Your existing architecture has used **30–60 second chunks** as a starting point.

Treat that as a hypothesis, not scripture.

Measure:

- p50/p95 chunk duration,
- provider request overhead,
- queue overhead,
- retry frequency,
- average transcript boundary quality,
- cost per media minute,
- merge correction rate,
- total parent completion time.

Then adjust.

For some transcription engines, 2–5 minute chunks may be more efficient. For others, shorter units may give better elasticity and recovery.

The correct number comes from the actual model/provider and workload.

---

# 5. Fixed-duration vs semantic boundaries

## Fixed duration

```text
00:00–01:00
01:00–02:00
02:00–03:00
```

Advantages:

- predictable sizing,
- simple indexing,
- easy progress math.

Problems:

- sentence/speaker can cross boundaries,
- cuts may happen during speech.

## Silence-aware segmentation

Prefer boundaries near detected silence.

```text
speech speech speech | silence | speech
                    ↑
                  split
```

Advantages:

- better linguistic boundaries,
- less awkward merge behavior.

Tradeoffs:

- uneven chunk sizes,
- possible worker imbalance,
- more preprocessing.

A practical strategy is often:

```text
target duration
+ min/max bounds
+ prefer nearby silence
```

---

# 6. Overlap

You may intentionally include a small overlap:

```text
Chunk 1: 00:00–01:02
Chunk 2: 00:58–02:02
```

This can preserve context around boundaries.

But now fan-in must deduplicate overlap.

Possible merge strategies:

- timestamps as the primary truth,
- token/text similarity around boundaries,
- word-level timestamps,
- keep canonical ownership windows,
- final cleanup model.

Overlap improves context but **creates merge complexity**.

---

# 7. Deterministic chunk identity

Never identify a chunk only by an ephemeral queue message ID.

Prefer a durable identity such as:

```text
(parent_job_id, chunk_index, pipeline_version)
```

or:

```text
(parent_job_id, start_ms, end_ms, pipeline_version)
```

This enables:

- idempotent retries,
- deterministic storage keys,
- duplicate detection,
- reprocessing after pipeline upgrades.

Example object key:

```text
jobs/{job_id}/v3/chunks/0042/transcript.json
```

---

# 8. Pipeline versioning

Suppose you improve:

- silence detection,
- transcription model,
- normalization,
- prompt,
- diarization.

Should the old chunk result be reused?

Maybe not.

Version the processing contract:

```text
pipeline_version = 3
```

Then idempotency is scoped correctly:

```text
UNIQUE(job_id, chunk_index, pipeline_version)
```

---

# 9. Straggler-aware partitioning

If chunks vary wildly in processing cost, the last chunk dominates fan-in latency.

Example:

```text
89 chunks finish in 18–25s
1 chunk takes 3m 40s
```

Parent completion time waits for the straggler.

Potential strategies:

- smaller chunks,
- split oversized chunks again,
- speculative execution for extreme stragglers,
- separate queues based on workload class,
- duration-aware scheduling.

Speculative execution means running a duplicate copy of a suspiciously slow task and accepting the first valid result.

It can reduce tail latency, but costs extra compute and requires strong idempotency.

Do not add it before you have actual straggler evidence.

---

# 10. Audio vs video partitioning

Your transcription model usually needs audio, not the full encoded video.

A common pipeline is:

```text
Video
 ↓
Extract / normalize audio
 ↓
Segment audio
 ↓
Transcribe chunks
```

This reduces bytes moved into transcription workers.

FFmpeg's generic segmenter can emit separate segments and can produce a CSV with segment start/end times. For exact video segment boundaries, keyframes matter; audio-only workflows are often simpler because you can segment the normalized audio directly.

---

# Exercise — Compare three chunk strategies

For a 90-minute video, compare:

```text
A = 30-second chunks → 180 tasks
B = 60-second chunks → 90 tasks
C = 5-minute chunks  → 18 tasks
```

For each, score 1–5:

- retry granularity,
- queue overhead,
- merge complexity,
- context quality,
- load balancing,
- progress resolution,
- provider efficiency.

Then write:

> I would start with ___ because ___. I would change it if metric ___ crosses threshold ___.

---

# Design deliverable — Chunk-Size ADR

Use this structure:

```text
Context
Workload assumptions
Chosen unit of work
Target chunk duration
Min/max duration
Boundary strategy
Overlap strategy
Identity/versioning
Concurrency assumptions
Failure/retry implications
Metrics
Alternative considered
Review trigger
```

---

# Break it 💥

1. A 60-second chunk contains 55 seconds of silence.
2. One chunk contains a 20-minute continuous speech section due to bad silence detection.
3. The model's maximum input duration changes.
4. Pipeline v2 accidentally reuses v1 output.
5. Two overlapping chunks both contain the same sentence.

How should the system behave?

---

# Retrieval quiz

1. Why is chunk size a failure-domain decision?
2. What improves when chunks become smaller?
3. What gets worse?
4. Fixed-duration vs silence-aware segmentation?
5. Why use overlap?
6. What new problem does overlap create?
7. Why include pipeline version in chunk identity?
8. What is a straggler?
9. When might speculative execution help?
10. Why should video usually be converted to an audio-focused intermediate representation before transcription?

## Exit criterion

You can defend a chunk-size policy using **measurements, failure domains and workload constraints**, not vibes.
