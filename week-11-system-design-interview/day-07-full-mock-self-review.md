# Day 7 — Full Mock Interview & Self-Review

## Goal

Complete one uninterrupted 45-minute system design, then review the **process**, not just the final diagram.

---

# Prompt

> Design a notification platform that can send email, push notifications, and SMS for multiple product teams.

Assume the interviewer will reveal more requirements only when asked.

---

# Rules

1. Set a 45-minute timer.
2. Do not open previous lessons.
3. Speak aloud as if someone is listening.
4. Draw while talking.
5. State assumptions.
6. If stuck, return to requirements rather than naming random technologies.

---

# Mandatory checkpoints

By minute 7:

```text
scope + scale assumptions
```

By minute 15:

```text
API/event interface + data model
```

By minute 27:

```text
high-level architecture
```

By minute 38:

```text
bottleneck/failure deep dive
```

Final minutes:

```text
tradeoffs + recap
```

---

# Self-review

Use [`scoring-rubric.md`](scoring-rubric.md).

Then classify every miss:

```text
Knowledge gap
→ I did not know the concept.

Reasoning gap
→ I knew it but didn't apply it.

Communication gap
→ I thought it but didn't explain it.

Time-management gap
→ I spent too long elsewhere.
```

This classification matters because each requires a different fix.

---

# Remediation

### Knowledge gap

Return to the relevant Week 1–10 lesson.

### Reasoning gap

Do another prompt using the seven-step template.

### Communication gap

Record a five-minute architecture explanation.

### Time-management gap

Repeat the same prompt with hard phase timers.

---

# Final oral questions

Answer in 90 seconds each:

1. Why not send notifications directly from the API?
2. What happens when the SMS provider is down for 20 minutes?
3. What is authoritative: your queue or your delivery database?
4. How do you prevent duplicate notifications?
5. Which metric would cause you to add workers?
6. What does graceful degradation look like?

---

# Week 11 graduation test

Pick a random system from the first six practice briefs.

Without notes, produce:

```text
Requirements
Estimates
API
Data
Architecture
10× / 100× / 1000×
Tradeoffs
```

If you can do this coherently, Week 12 starts.
