# Day 6 — Sagas, Compensation, Source of Truth & Reconciliation

## Goal

Design long-running workflows that reach a valid outcome **without pretending every step can be one global transaction**.

This day directly answers:

> Worker finished chunk → queue says DONE → database update failed. What is the source of truth?

## Timebox

- 20 min — saga mental model
- 20 min — choreography vs orchestration
- 20 min — compensation
- 25 min — source-of-truth matrix
- 25 min — reconciliation
- 10 min — quiz

---

# 1. Saga mental model

A saga is a sequence of local transactions.

```text
Step A local commit
    ↓
Step B local commit
    ↓
Step C local commit
```

If later work fails, the workflow runs retry/continuation or business-specific compensation.

```text
A ✅
B ✅
C ❌
 ↓
Compensate B
Compensate A
```

Not every step is necessarily reversible.

---

# 2. Choreography vs orchestration

## Choreography

Services react to events:

```text
UploadCompleted
    ↓
Processor starts
    ↓ ChunkTranscribed
Aggregator reacts
    ↓ JobCompleted
Billing reacts
```

Benefits:

- loose coupling,
- no central workflow engine.

Costs:

- workflow becomes hard to see,
- cycles and event spaghetti,
- recovery logic scattered across consumers.

## Orchestration

A coordinator owns workflow state:

```text
Orchestrator
  ├── start processing
  ├── wait for chunks
  ├── trigger merge
  ├── persist completion
  └── compensate/retry
```

Benefits:

- explicit state machine,
- clearer recovery and observability.

Costs:

- coordinator is important infrastructure,
- stronger coupling to workflow definition.

Week 6 already prepared you for this tradeoff.

---

# 3. Compensation is a new business action

Suppose usage billing was recorded before a user cancellation.

You do not “time travel” and erase history.

You may append:

```text
UsageCharged +10 minutes
UsageRefunded -10 minutes
```

Likewise, if an email was sent, you cannot unsend it.

Compensation might be:

- send correction email,
- issue refund,
- release quota reservation,
- mark object for deletion,
- append correcting ledger entry.

---

# 4. Source of truth is per fact

Consider your chunk workflow.

## Fact A — “Does the chunk artifact exist?”

Possible authority:

```text
R2 object at deterministic key
```

## Fact B — “Has the workflow accepted chunk 42 as completed?”

Possible authority:

```text
PostgreSQL chunk row/state machine
```

## Fact C — “Is this queue delivery still pending?”

Authority:

```text
broker delivery/ACK state
```

## Fact D — “What does the UI show?”

Likely derived from PostgreSQL, maybe cached.

Therefore this scenario is not contradictory:

```text
R2: artifact exists ✅
DB: chunk PROCESSING
Queue: message redelivered
```

It means:

```text
computation/output succeeded
business-state finalization did not
```

---

# 5. Design the worker around durable evidence

Use deterministic artifact key:

```text
results/{job_id}/{pipeline_version}/{chunk_index}.json
```

Worker redelivery:

```text
1. inspect authoritative chunk row
2. if already SUCCEEDED → ACK duplicate
3. otherwise check deterministic artifact
4. if artifact exists and checksum/version valid:
       skip expensive AI recomputation
       reconcile DB state
5. if artifact missing:
       recompute
6. conditional DB transition to SUCCEEDED
7. ACK only after durable state is safe
```

This dramatically shrinks the cost of ambiguous failures.

---

# 6. Do not make R2 alone the workflow authority

An object exists, but that doesn't necessarily mean:

- correct pipeline version,
- expected checksum,
- valid metadata,
- parent job wasn't cancelled,
- billing/accounting transition completed.

That is why authority is **fact-specific**.

---

# 7. Reconciliation

Retries handle immediate transient failures.

Reconciliation handles **durable divergence that survives ordinary retries**.

A reconciliation job might query:

```sql
SELECT id, job_id, chunk_index, artifact_key
FROM chunks
WHERE status IN ('RUNNING', 'RETRYING')
  AND updated_at < now() - interval '15 minutes';
```

Then compare:

```text
DB state
vs
R2 artifact
vs
broker/workflow state
```

Possible repair:

```text
DB says RUNNING + artifact valid
→ conditional repair to SUCCEEDED

DB says SUCCEEDED + artifact missing
→ mark inconsistent / retry production / alert

DB says CANCELLED + orphan artifact
→ lifecycle-delete artifact later
```

---

# 8. Reconciliation requires invariants

Useful invariants:

```text
SUCCEEDED chunk must have valid artifact_key

one accepted result per
(job_id, chunk_index, pipeline_version)

completed_chunks must equal count of accepted SUCCEEDED children
before merge claim
```

A reconciler checks invariants and repairs or alerts.

Without invariants, “reconciliation” becomes guesswork.

---

# 9. Queue is not your business database

The broker knows things like:

```text
published
pending
redelivered
acked
```

It usually does not own:

```text
user-visible job state
billing state
artifact validity
workflow invariants
```

So:

> “Queue says done”

is usually not enough to declare the business workflow complete.

---

# Exercise — source-of-truth matrix

Fill:

| Fact | Authority | Derived copies | Allowed divergence | Reconciliation |
|---|---|---|---|---|
| upload object exists | | | | |
| job status | | | | |
| chunk result bytes | | | | |
| chunk accepted as complete | | | | |
| parent progress | | | | |
| billing ledger | | | | |
| search index | | | | |
| broker delivery state | | | | |

---

# Exercise — saga

Design this workflow:

```text
Accept Job
→ Reserve monthly quota
→ Process chunks
→ Merge transcript
→ Record billable minutes
→ Publish completion
```

For each step define:

- local transaction,
- retryable errors,
- idempotency key,
- compensation if required,
- point of no return,
- authoritative state.

---

# Break it 💥

1. Compensation fails halfway through.
2. Reconciler and normal worker both repair the same chunk.
3. Orphan R2 artifacts accumulate.
4. DB says `SUCCEEDED` but artifact checksum is wrong.
5. Billing event delivered twice.
6. Search projection misses one event permanently.

How do you detect and repair each?

---

# Retrieval quiz

1. What is a saga?
2. Choreography vs orchestration?
3. Why is compensation not rollback?
4. Why is source of truth defined per fact?
5. In our design, what does the queue authoritatively know?
6. Why use deterministic artifact keys?
7. What problem does reconciliation solve that retries do not?
8. Give two invariants a reconciler can verify.

## Exit criterion

You can explain **exactly** how the system converges after a durable partial success.
