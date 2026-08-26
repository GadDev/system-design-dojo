# Week 11 — System Design Interview Mechanics ⚔️

## Mission

For ten weeks you learned the ingredients. This week you learn to **cook under pressure**.

By the end of the week, you should be able to take an ambiguous prompt, lead the conversation, make reasonable assumptions, estimate scale, design interfaces/data, draw a coherent architecture, identify the first bottlenecks, and defend tradeoffs — without turning the interview into a technology shopping list.

The system design interview is an open-ended conversation. The goal is not to guess the interviewer's hidden architecture. The goal is to make your reasoning visible.

---

## The 7-step framework

Use this sequence every time:

```text
1. Requirements
      ↓
2. Scale estimation
      ↓
3. API design
      ↓
4. Data model
      ↓
5. High-level architecture
      ↓
6. Bottlenecks: 10× / 100× / 1000×
      ↓
7. Tradeoffs
```

### Cross-cutting lenses

While moving through the seven steps, repeatedly ask:

```text
Failure
Security / privacy
Observability
Cost
```

Do **not** bolt them onto the last 30 seconds as decorative architecture parsley. 🌿

---

## Suggested 45-minute timebox

| Phase | Time |
|---|---:|
| Requirements + scope | 5–7 min |
| Estimation | 4–5 min |
| API + data model | 6–8 min |
| High-level design | 10–12 min |
| Deep dive / bottlenecks | 8–10 min |
| Tradeoffs + wrap-up | 4–5 min |

The exact split is flexible. The point is to avoid spending 25 minutes debating one database schema before you have an architecture.

---

## Week 11 rule

For every component you draw, be able to finish this sentence:

> **“I need this because…”**

Examples:

```text
Redis
→ because the redirect workload is read-heavy and contains hot keys.

Queue
→ because notification sending is asynchronous and bursty.

Object storage
→ because multi-GB media should not live in PostgreSQL rows.
```

Weak:

> “Kafka is scalable.”

Strong:

> “I would begin with Redis Streams or RabbitMQ because replaying a long event history is not yet a requirement and operational simplicity matters more than Kafka's log-retention model at our current scale.”

---

## Daily plan

| Day | Topic | Main deliverable |
|---|---|---|
| 1 | Requirements, scope & non-functional requirements | Clarification checklist |
| 2 | Back-of-envelope estimation | Capacity worksheet |
| 3 | API + data model | Interface/data contract |
| 4 | High-level architecture + bottleneck analysis | 10×/100×/1000× map |
| 5 | Tradeoffs, communication & interview steering | Decision narrative |
| 6 | Training ladder 1–6 | Six timed mini-designs |
| 7 | Full 45-minute mock + review | Scored design + remediation plan |

---

## Week 11 practice systems

```text
🟢 1 URL Shortener      → DB + cache
🟢 2 Pastebin           → storage
🟢 3 Rate Limiter       → Redis / distributed counters
🟡 4 Notification       → queues / delivery
🟡 5 File Upload        → object storage / resumability
🟡 6 Chat               → realtime / connection state
```

Each brief lives under [`practice/`](practice/).

---

## Exit criterion

You are ready for Week 12 when you can receive an unfamiliar prompt and, within five minutes, have:

1. a bounded problem,
2. explicit scale assumptions,
3. two or three non-functional priorities,
4. a rough API/data model,
5. a clear place to start drawing.

If the first thing out of your mouth is still “I'd use Kafka…”, do another mock. 😄
