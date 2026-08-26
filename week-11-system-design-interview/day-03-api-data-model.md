# Day 3 — API Design & Access-Pattern-First Data Modeling

## Goal

Define the system's contracts and data around actual user/workflow operations rather than generic CRUD tables.

---

# 1. API design is behavior design

For your transcription platform:

```http
POST /uploads
POST /uploads/{upload_id}/complete
POST /jobs
GET  /jobs/{job_id}
GET  /transcripts/{job_id}
```

Ask for every operation:

```text
Who calls it?
What are the inputs?
What is returned?
Sync or async?
Can it be retried?
How is authorization enforced?
What are the main failure responses?
```

---

# 2. Prefer resource/workflow semantics over verbs everywhere

Rather than:

```http
POST /doTranscriptionNow
```

prefer something closer to:

```http
POST /jobs
```

and return:

```http
202 Accepted
Location: /jobs/job_123
```

for long-running work.

The exact API style is less important than communicating lifecycle clearly.

---

# 3. Idempotency belongs in API design

If the client retries:

```http
POST /uploads/upl_123/complete
```

should two transcription jobs appear?

Probably not.

Design for retry ambiguity using:

```text
idempotency key
unique business key
conditional state transition
```

Do not postpone retry semantics until “reliability discussion.”

---

# 4. Access-pattern-first modeling

Avoid:

> “SQL is relational, so I'll make a users table.”

Start with queries.

### Example access patterns

```text
Get one job by ID
List user's newest 50 jobs
Find queued chunks ready for retry
Fetch all successful chunks ordered by chunk_index
Find expired uploads for cleanup
```

Now data design becomes grounded.

---

# 5. Example transcription model

```text
users
uploads
jobs
chunks
transcripts
```

Possible relationships:

```text
User 1 ── N Uploads
Upload 1 ── N Jobs
Job 1 ── N Chunks
Job 1 ── 1 Transcript
```

Important invariants might include:

```sql
UNIQUE (job_id, chunk_index, pipeline_version)
```

and guarded lifecycle updates.

---

# 6. API choices reveal architecture

### Chat

```text
REST for history
WebSocket for realtime messages
```

### File upload

```text
API for upload session/control
object-storage URL for bytes
```

### Notification

```text
POST /notifications
→ accept work
→ enqueue delivery
```

### Feed

```text
GET /feed?cursor=...
```

Cursor pagination often fits mutable high-volume timelines better than page numbers.

---

# 7. Don't over-specify

An interview normally does not need:

```text
43 endpoint definitions
complete SQL DDL
OpenAPI YAML
```

Show enough contract to support the architecture.

---

# Exercise — Notification system

Define APIs/events for:

```text
send notification
get delivery status
unsubscribe user
```

Then model:

```text
notification request
recipient preference
channel delivery attempt
provider response
```

Answer:

- Which operations are async?
- Which identifiers need idempotency?
- What data must be authoritative?
- Which data could be derived analytics?

---

# Retrieval quiz

1. Why start from access patterns?
2. Why might `202 Accepted` fit transcription?
3. Where does idempotency enter API design?
4. Give an example of a DB invariant that prevents duplicate chunk work.
5. Why might chat use more than one communication protocol?

## Exit criterion

You can sketch a small but meaningful API and data model in under eight minutes and explain the access patterns they support.
