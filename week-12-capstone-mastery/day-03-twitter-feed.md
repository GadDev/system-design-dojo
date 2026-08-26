# Day 3 — Design a Twitter/X-style Home Feed 🔴

## Prompt

> Design a home feed showing recent posts from accounts a user follows.

Focus on distribution/fan-out, not recommendation ML.

---

# The core asymmetry

```text
one write
→ potentially millions of followers
```

versus:

```text
one read
→ needs a fast personalized list
```

This creates the famous tradeoff:

```text
fan-out-on-write
vs
fan-out-on-read
```

---

# Fan-out on write

When Alice posts:

```text
post
 ↓
Fanout workers
 ↓
append post ID to follower timelines
```

Benefits:

```text
fast reads
```

Costs:

```text
huge write amplification
celebrity fan-out
stale/deleted entry cleanup
```

---

# Fan-out on read

When Bob opens feed:

```text
fetch followed accounts
 ↓
fetch candidate recent posts
 ↓
merge/rank
```

Benefits:

```text
cheap writes
```

Costs:

```text
read amplification
latency
complex query/merge
```

---

# Hybrid

A common reasoning target:

```text
ordinary accounts
→ fan-out on write

celebrity/high-follower accounts
→ merge on read
```

The exact threshold must be measured.

---

# Data model

```text
users
follow_edges
posts
home_timeline_entries / cache
```

Discuss whether timeline entries contain:

```text
full post
or
post IDs
```

IDs reduce duplication and make edits/deletes easier to centralize.

---

# Deep-dive questions

- What is feed ordering?
- How fresh must new posts appear?
- How are deleted posts removed?
- What happens when user follows/unfollows someone?
- How do celebrity posts avoid exploding queue/backlog?
- What is authoritative: post store or feed cache?
- Can the feed be eventually consistent?

---

# 100× bottleneck

Assume one account has 100M followers and posts during a global event.

Your architecture should not require completing 100M synchronous timeline writes before acknowledging the post.

---

## Exit criterion

You can explain fan-out-on-write/read as a workload tradeoff rather than memorizing “Twitter uses fan-out.”
