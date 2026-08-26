# System Design Dojo 🥷

[![GitHub Actions](https://github.com/GadDev/system-design-dojo/actions/workflows/ci.yml/badge.svg)](https://github.com/GadDev/system-design-dojo/actions/workflows/ci.yml)
[![Docs](https://github.com/GadDev/system-design-dojo/actions/workflows/docs.yml/badge.svg)](https://github.com/GadDev/system-design-dojo/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![VitePress](https://img.shields.io/badge/docs-VitePress-646CFF?logo=vitepress&logoColor=white)](https://vitepress.dev/)
[![12 Week Curriculum](https://img.shields.io/badge/curriculum-12%20weeks-blue)](ROADMAP.md)
[![System Design](https://img.shields.io/badge/focus-System%20Design-orange)](ROADMAP.md)

> **Learn system design by designing systems.**

A hands-on **12-week system design dojo** for software engineers who want to move beyond memorizing architecture diagrams and learn how to reason about **scalability, distributed systems, reliability, data, failures, and engineering trade-offs**.

You won't just read about systems here.

You'll **design them, break them, scale them, defend your decisions, and reconstruct them from memory**.

---

## 🎯 What you'll learn

By the end of the dojo, you should be able to reason through a system from requirements to production trade-offs:

```text
Requirements
     ↓
Estimates
     ↓
API Design
     ↓
Data Model
     ↓
Architecture
     ↓
Scale
     ↓
Failures
     ↓
Reliability
     ↓
Observability
     ↓
Security
     ↓
Cost
     ↓
Trade-offs
```

The curriculum covers:

- networking and web fundamentals,
- databases and data modeling,
- caching and Redis,
- load balancing and horizontal scaling,
- queues and asynchronous processing,
- distributed workers and orchestration,
- retries, idempotency and failure handling,
- observability and reliability,
- distributed consistency,
- event-driven architecture,
- architecture patterns,
- system design interview mechanics,
- production-oriented capstone designs.

---

## 🗺️ The 12-week journey

| Phase | Focus |
|---|---|
| 🧱 **Foundations** | Networking, HTTP, DNS, databases and core system concepts |
| 🚀 **Scaling** | Caching, load balancing and horizontal scaling |
| ⚙️ **Distributed Systems** | Queues, workers, orchestration and asynchronous processing |
| 🛡️ **Reliability** | Failure handling, retries, idempotency and observability |
| 🧠 **Architecture** | Consistency, distributed data and architectural patterns |
| ⚔️ **Mastery** | System design interviews and production-grade capstones |

See [`ROADMAP.md`](ROADMAP.md) for the complete curriculum.

---

## 🚧 Project status

The complete **12-week curriculum is mapped**, while individual weeks are being expanded into full learning modules.

- ✅ **Week 1 — Foundations:** expanded
- 🚧 **Weeks 2–12:** curriculum mapped and progressively being developed
- ✅ Practical labs
- ✅ Architecture exercises
- ✅ Failure drills
- ✅ Retrieval practice
- ✅ Design templates
- ✅ Primary sources and book references

Start with:

[`week-01-foundations/README.md`](week-01-foundations/README.md)

---

## 🥋 How the dojo works

System design is not a spectator sport.

A useful learning ratio is:

```text
20%  Reading / Videos
          ↓
30%  Understanding
          ↓
50%  Designing Systems
```

System design is closer to learning guitar than studying history.

You can read about guitar for months, understand every chord theoretically, and still not know how to play.

Eventually, you have to pick up the guitar. 🎸

The same applies here.

For every major concept, you should eventually be able to:

1. explain it simply,
2. draw it,
3. identify where it fails,
4. explain its trade-offs,
5. use it inside a larger architecture.

---


## 🚀 Start training

Begin here:

```text
week-01-foundations/README.md
```

Then work through:

```text
Day 1 → Day 2 → Day 3 → ... → Day 7
```

Keep these nearby while studying:

```text
week-01-foundations/resources.md
week-01-foundations/cheat-sheet.md
BOOK-READING-PLAN.md
```

### ⚠️ One rule

Do **not** open:

```text
week-01-foundations/answer-key.md
```

until you've completed the review quiz.

Retrieval is part of the training.

---

## 🧠 The learning loop

Each topic should move through roughly the same cycle:

```text
Learn
  ↓
Explain
  ↓
Diagram
  ↓
Design
  ↓
Break
  ↓
Fix
  ↓
Recall
  ↓
Repeat
```

The goal isn't:

> "I've read about Redis."

The goal is:

> "I know when Redis helps, when it doesn't, what can fail, and what trade-offs I'm introducing."

---


## 🧪 Course standard

A mature dojo module contains:

- 🎯 learning objectives,
- 🧠 mental models,
- 🗺️ Mermaid architecture diagrams,
- 🏗️ concrete system examples,
- 📚 authoritative sources,
- 🧪 hands-on labs,
- 💥 failure drills,
- 🧩 retrieval quizzes,
- 📝 design templates and ADRs,
- ⚔️ capstone exercises,
- 🔐 separate answer keys.

The exercises are deliberately designed to force **active reasoning**, not passive consumption.

> **Do not optimize for finishing files.**
>
> Optimize for being able to close the repository and reconstruct the architecture from memory.

---

## 💥 Learn by breaking systems

A design isn't finished when the happy path works.

Ask:

```text
What happens when the database is slow?

What happens when Redis disappears?

What happens when a worker processes the same message twice?

What happens when one region becomes unavailable?

What happens when traffic suddenly increases 20×?

What happens when two services disagree about state?
```

Understanding failure modes is one of the fastest ways to move from:

```text
"I know this technology."
```

to:

```text
"I understand the system."
```

---

## 📚 The companion book

<a href="https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/"><img src="https://www.oreilly.com/covers/urn:orm:book:9781098119058/296w/?format=webp" alt="Designing Data-Intensive Applications, 2nd Edition cover" width="140"></a>

**Designing Data-Intensive Applications, 2nd Edition** — Martin Kleppmann & Chris Riccomini. [O'Reilly](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/) · [Amazon](https://www.amazon.com/Designing-Data-Intensive-Applications-2nd-Maintainable/dp/B0H27BX5FH)

Don't read it cover-to-cover before starting.

Use it as a **companion to the dojo**.

For example:

```text
Learning replication
        ↓
Study the dojo lesson
        ↓
Read the relevant DDIA chapter
        ↓
Design a replicated system
        ↓
Reason about its failure modes
```

See [`BOOK-READING-PLAN.md`](BOOK-READING-PLAN.md) for the full topic-to-chapter mapping across the reference books.

---

## ⚔️ Final phase

The final part of the dojo shifts from learning individual concepts to combining them under constraints.

### Week 11 — System Design Interview Mechanics

Practice turning vague requirements into structured architecture decisions.

[`week-11-system-design-interview/README.md`](week-11-system-design-interview/README.md)

### Week 12 — Capstone & Mastery

Bring the entire curriculum together through larger system designs.

[`week-12-capstone-mastery/README.md`](week-12-capstone-mastery/README.md)

Supporting material:

- [`TRAINING-LADDER.md`](TRAINING-LADDER.md) — System Design Training Ladder
- [`SYSTEM-DESIGN-NOTEBOOK.md`](SYSTEM-DESIGN-NOTEBOOK.md) — System Design Bible / Notebook

---

## 📈 Track your progress

Use:

[`PROGRESS.md`](PROGRESS.md)

The goal isn't simply checking boxes.

Track whether you can:

```text
Recognize the problem
        ↓
Choose an architecture
        ↓
Explain the trade-offs
        ↓
Predict failure modes
        ↓
Defend your decisions
```

---

## 📂 Repository guide

| File | Purpose |
|---|---|
| [`ROADMAP.md`](ROADMAP.md) | Full 12-week curriculum |
| [`PROGRESS.md`](PROGRESS.md) | Per-day completion tracker |
| [`REVIEW-NOTES.md`](REVIEW-NOTES.md) | Editorial standard for lessons and labs |
| [`BOOK-READING-PLAN.md`](BOOK-READING-PLAN.md) | Reference books mapped to curriculum topics |
| [`TRAINING-LADDER.md`](TRAINING-LADDER.md) | Progressive system design training model |
| [`SYSTEM-DESIGN-NOTEBOOK.md`](SYSTEM-DESIGN-NOTEBOOK.md) | Long-term system design reference notebook |

---

## 🧭 The mindset

There is rarely one universally correct system design.

Instead, there are decisions made under constraints.

```text
Consistency vs Availability

Latency vs Durability

Simplicity vs Flexibility

Cost vs Performance

Build vs Buy

Synchronous vs Asynchronous

Normalization vs Denormalization
```

The point of the dojo is not to memorize the "correct architecture."

It is to become comfortable saying:

> **Given these requirements and constraints, I would choose this design — and here are the trade-offs.**

That's system design.

---

## 🤝 Contributing

Contributions, corrections and improvements are welcome.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing changes.

Community expectations are documented in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 💬 A thought to leave with

> “A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable.”
>
> — **Leslie Lamport**, distributed systems pioneer

---

<p align="center">
  <strong>Design it. Break it. Scale it. Explain it. 🥷</strong>
</p>

<p align="center">
  Made with ❤️ in Luxembourg · © 2026
</p>
