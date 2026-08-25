# Day 1 — SQL vs NoSQL: Choose From the Workload, Not the Logo

## Goal

Learn to choose a database family from the shape of the data and workload rather than from slogans such as "NoSQL scales" or "SQL is safer."

## Timebox

- 15 min — relational vs document mental models
- 15 min — workload dimensions
- 15 min — normalization vs denormalization
- 15 min — transcription-system exercise
- 10 min — retrieval quiz

---

# 1. Start with the workload

Before choosing a database, write the operations the system must perform.

For the transcription platform:

```text
Create user
Create upload
Create job
Update job progress
Insert hundreds of chunk results
Fetch job history by user
Fetch final transcript
Delete all data for a user
```

These operations tell us more than a generic "SQL vs NoSQL" comparison.

A senior design discussion starts with:

```text
access patterns
consistency requirements
cardinality
size / growth
latency target
operational constraints
```

Not:

```text
Which database is coolest this quarter?
```

---

# 2. Relational model

A relational database stores data in relations—practically, tables with rows and typed columns—and lets you express relationships and constraints explicitly.

Example:

```text
users
  id
  email

jobs
  id
  user_id → users.id
  status
```

Strengths for this workload:

- strong integrity constraints,
- expressive joins,
- multi-row transactions,
- mature indexing,
- good fit for ownership relationships,
- predictable query model.

Costs:

- schema changes require discipline,
- joins can become expensive at scale if abused,
- highly distributed writes are not "free",
- normalization can require more reads/joins.

---

# 3. Document model

A document database often stores related fields together as one document.

Conceptually:

```json
{
  "jobId": "job-123",
  "userId": "user-9",
  "status": "processing",
  "chunks": [
    { "index": 0, "text": "..." },
    { "index": 1, "text": "..." }
  ]
}
```

This can be attractive when:

- related data is usually read together,
- the aggregate is bounded in size,
- schema varies substantially,
- application code naturally treats the object as one aggregate.

But ask what happens when:

- a 3-hour video produces hundreds/thousands of segments,
- chunks update independently,
- you need to query chunks separately,
- the parent document grows without a clear bound.

The data model must follow the workload.

---

# 4. SQL vs NoSQL is not binary

PostgreSQL can store relational columns **and** semi-structured JSONB.

Example:

```sql
CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    status text NOT NULL,
    provider_metadata jsonb
);
```

This gives you:

```text
structured invariant data → typed columns
provider-specific flexible metadata → JSONB
```

That is often better than forcing every field into either a rigid relational schema or one giant JSON blob.

PostgreSQL's `jsonb` can also be indexed, but that does not mean every schema should become JSON.

---

# 5. Normalize or denormalize?

Suppose you want the user's email on every job.

## Normalized

```text
jobs.user_id → users.id
```

Read email by joining `users`.

Advantages:

- one authoritative email value,
- updates happen in one place,
- less duplication.

## Denormalized

```text
jobs.user_email
```

Advantages:

- some reads become simpler,
- historical snapshot semantics may be intentional.

Costs:

- duplicated data,
- update consistency becomes your problem.

The correct question is not:

> Is denormalization bad?

It is:

> Do we intentionally want duplication because it improves a known access pattern or preserves historical state?

---

# 6. A decision matrix

Score each candidate for your application.

| Requirement | PostgreSQL | Document DB | Object Storage |
|---|---:|---:|---:|
| User/job relationships | Strong | Good | Poor |
| Multi-row transactions | Strong | Product-dependent | No |
| Flexible metadata | Good with JSONB | Strong | Blob only |
| Huge media files | Poor fit | Poor fit | Excellent |
| Ad-hoc joins/reporting | Strong | Mixed | Poor |
| Cheap large immutable blobs | Poor | Poor/medium | Excellent |

Notice something useful:

**A system can—and usually does—use more than one storage technology.**

For your platform:

```text
PostgreSQL → metadata + ownership + job state
Object storage → video/audio + possibly large transcript artifacts
```

That is polyglot persistence driven by data shape, not by fashion.

---

# 7. Exercise — Choose storage per object

For each object, choose one primary storage location and explain why:

1. User account metadata
2. Original 4 GB video
3. Job state
4. Per-chunk transcript result
5. Final transcript text
6. Provider request/response metadata
7. Exported CSV

For every answer write:

```text
Choice:
Dominant access pattern:
Consistency need:
Expected size:
Why not the alternative:
```

Do not look for one database to win all seven.

---

# Break it 💥

Your team says:

> "Let's put everything in MongoDB because the transcript is JSON."

Challenge the proposal.

Ask:

- Which objects have strong relationships?
- Which updates must be atomic?
- Which documents can grow without bound?
- Which queries need joins/filtering/reporting?
- Are we choosing MongoDB because of workload evidence or because JSON feels familiar?

Then reverse the exercise:

> "Let's put everything in PostgreSQL because transactions are nice."

What goes wrong with 4 GB video blobs?

---

# Retrieval quiz

1. Name five workload dimensions that should influence database choice.
2. Why is "NoSQL scales better" an incomplete statement?
3. What is normalization trying to reduce?
4. When can denormalization be intentional?
5. Why might JSONB be useful inside an otherwise relational schema?
6. Why is object storage a better fit than PostgreSQL for multi-GB videos?
7. What does "polyglot persistence" mean?

## Exit criterion

You can defend a storage choice using **access patterns + consistency + size + operational cost**, without relying on database stereotypes.
