# Day 1 — Requirements, Scope & Ambiguity

## Goal

Learn to turn a vague prompt into a bounded engineering problem before drawing boxes.

## Timebox

- 20 min — functional vs non-functional requirements
- 15 min — clarification patterns
- 20 min — three prompt drills
- 10 min — scope-control exercise
- 5 min — retrieval quiz

---

## 1. Why requirements come first

Suppose the prompt is:

> Design a chat system.

That can mean wildly different systems:

```text
1-to-1 only?
group chat?
100 users or 1 billion?
message history?
offline delivery?
read receipts?
end-to-end encryption?
attachments?
realtime latency target?
```

An architecture that is excellent for a 50-person internal chat can be absurd for a global messenger.

### Interview objective

Your first job is not to solve the system.

Your first job is to **discover the system**.

---

# 2. Functional requirements

Functional requirements describe what users/system actors can do.

For a URL shortener:

```text
create short URL
redirect short URL
optional expiration
optional custom alias
```

For the first 45-minute design, explicitly exclude features that are not central:

```text
analytics dashboard → later
QR codes → out of scope
team collaboration → out of scope
```

Scope control is a design skill.

---

# 3. Non-functional requirements

Ask about the qualities that drive architecture.

Useful categories:

### Scale

```text
DAU / MAU
QPS
read/write ratio
object size
growth rate
```

### Performance

```text
p50 / p95 / p99 latency
realtime expectations
startup / upload / delivery latency
```

### Reliability

```text
availability target
acceptable data loss
RTO / RPO
retry behavior
```

### Consistency

```text
strong?
eventual?
read-your-writes?
acceptable stale window?
```

### Security / privacy

```text
public vs private data
authentication
authorization
PII
retention
abuse
```

### Cost

```text
storage-heavy?
network-heavy?
GPU-heavy?
CDN-heavy?
```

---

# 4. The five questions that usually unlock the problem

If time is tight, ask these:

1. **What are the top 2–3 user actions?**
2. **What scale should I design for?**
3. **What matters most: latency, availability, consistency, cost, or durability?**
4. **What data is large / hot / sensitive?**
5. **What can I explicitly leave out?**

Then summarize:

> “I’ll design for 10M DAU, read-heavy traffic, p95 redirects under 100 ms, high availability, and eventual consistency for analytics. I’ll keep custom domains and advanced analytics out of scope.”

That summary is valuable because it gives the interviewer a chance to correct your assumptions.

---

# 5. Non-functional priorities change designs

### Example A — Chat

If the requirement is:

```text
messages arrive within seconds
```

polling may be fine.

If:

```text
interactive chat
< 200 ms perceived delivery
```

persistent connections become more attractive.

### Example B — Payments

You might prioritize:

```text
correctness + auditability
```

over:

```text
absolute lowest latency
```

### Example C — Video feed

You may accept:

```text
slightly stale recommendation data
```

while requiring:

```text
video bytes delivered with high availability
```

---

# 6. Don't ask 37 questions

Requirements gathering can become avoidance.

Bad:

> “What color is the upload button?”

Useful:

> “What maximum upload size should I assume? That changes whether I proxy through the API or upload directly to object storage.”

Ask questions that can change architecture.

---

# Exercise — Three prompt drills

For each prompt, spend **3 minutes** writing:

- 3 functional requirements,
- 4 non-functional requirements,
- 3 clarifying questions,
- 3 explicit exclusions.

### Prompt A

> Design Pastebin.

### Prompt B

> Design a notification system.

### Prompt C

> Design Dropbox.

Then ask:

> Which clarification would most change my architecture?

---

# Interview phrase bank

Useful language:

> “Before I choose storage, I want to understand the access pattern.”

> “I’ll make an assumption so we can keep moving: 10M DAU and a 100:1 read/write ratio. I’ll revise it if you want a different scale.”

> “This requirement changes the design because…”

> “I’ll keep X out of scope for the first pass and return to it if we have time.”

---

# Retrieval quiz

1. Functional vs non-functional requirement?
2. Name five non-functional categories.
3. Why should you repeat assumptions back to the interviewer?
4. What makes a clarification question valuable?
5. Why is explicit scope exclusion useful?

## Exit criterion

Given a vague prompt, you can establish a useful scope in under five minutes without prematurely choosing technologies.
