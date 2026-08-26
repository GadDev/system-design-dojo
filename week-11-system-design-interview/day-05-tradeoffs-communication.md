# Day 5 — Tradeoffs, Communication & Senior-Level Reasoning

## Goal

Turn architecture choices into explicit decisions rather than declarations.

---

# 1. A senior answer has context

Weak:

> Kafka is scalable.

Better:

> Kafka gives us durable partitioned logs and replay, but our current requirement is a work queue with modest throughput and no replay-driven consumers. I would start with RabbitMQ/Redis Streams and revisit Kafka if retention/replay or multiple independent streaming consumers become requirements.

The structure is:

```text
Requirement
→ Option
→ Benefit
→ Cost
→ Decision
→ Revisit trigger
```

---

# 2. Common tradeoff dimensions

```text
latency vs consistency
availability vs coordination
simplicity vs flexibility
cost vs performance
build vs buy
sync vs async
normalized vs denormalized
precompute vs compute-on-read
fan-out-on-write vs fan-out-on-read
locality vs global consistency
```

You don't need to mention all of them. Mention the ones relevant to the design.

---

# 3. Speak in assumptions

Use:

> “Given our assumed 60k peak redirect RPS and 99% cache hit target…”

instead of:

> “We need Redis.”

This makes the reasoning falsifiable.

If the assumption changes, the architecture can change without anyone “losing.”

---

# 4. Acknowledge alternatives

Useful phrasing:

> “Another reasonable option is X. I’m choosing Y because…”

That demonstrates breadth without spending ten minutes comparing every database invented since 1970.

---

# 5. Communicate uncertainty

Good system design includes uncertainty.

Say:

> “I don't have enough evidence yet to shard. I would instrument table growth and query p95 and introduce partitioning first if lifecycle management becomes the pain.”

This is stronger than confidently inventing requirements.

---

# 6. Interview steering

The interviewer may push:

> “What if traffic jumps 100×?”

Don't defend your original design emotionally.

Respond:

```text
New requirement
↓
Find new bottleneck
↓
Adapt architecture
```

System design is not a courtroom defense of your first diagram.

---

# 7. Your 90-second conclusion

End with:

```text
1. Main requirements
2. Main architecture
3. Authoritative data stores
4. Primary scale strategy
5. Primary failure strategy
6. Biggest tradeoff
7. What you would validate next
```

Example:

> “I chose direct object-storage uploads so the API remains a control plane rather than carrying multi-GB media. PostgreSQL is authoritative for job lifecycle; the queue is at-least-once and workers are idempotent. Workers scale from queue age rather than API CPU. The main tradeoff is extra orchestration complexity in exchange for independent retries and throughput. Before increasing complexity further I would load-test upload-init RPS, DB completion bursts, and worker/provider capacity.”

---

# Exercise — Decision rewrites

Rewrite each weak statement.

### A

> “Use NoSQL because it scales.”

### B

> “Use WebSockets because they are realtime.”

### C

> “Use microservices for scalability.”

### D

> “Use Kafka for the queue.”

### E

> “Shard the database.”

For each use:

```text
requirement → evidence → decision → tradeoff → revisit trigger
```

---

# Retrieval quiz

1. What makes a tradeoff statement strong?
2. Why state assumptions explicitly?
3. How should you react when the interviewer changes scale?
4. Why mention alternatives?
5. What belongs in a 90-second conclusion?

## Exit criterion

Your explanations sound like engineering decisions, not product documentation for technologies.
