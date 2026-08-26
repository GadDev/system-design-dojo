# Day 6 — Design Netflix-lite 🔴

## Prompt

> Design a global video-on-demand streaming platform.

Focus on ingest/preparation, catalog metadata, playback authorization and global delivery — not recommendation ML.

---

# The dominant idea

For a streaming service, the API may be important, but the biggest workload is often:

```text
VIDEO BYTES
VIDEO BYTES
VIDEO BYTES
```

A global media-delivery architecture is fundamentally about moving huge immutable assets close to viewers efficiently.

---

# Content lifecycle

```text
Studio master
   ↓
Ingest
   ↓
Encode many formats/bitrates
   ↓
Package segments/manifests
   ↓
Origin storage
   ↓
CDN / edge caches
   ↓
Viewer
```

---

# Playback control vs data

```text
Viewer → Playback API
          ↓ auth / entitlement
          ↓ manifest / CDN location

Viewer ==================> CDN
             media segments
```

Again:

```text
control plane
≠
data plane
```

---

# CDN strategy

Netflix's Open Connect provides a useful real-world model: content appliances can be embedded inside ISP networks, localizing substantial traffic and reducing transit distance/load.

Think through:

```text
cache placement
content popularity
prefill vs demand caching
origin shielding
regional failover
```

---

# Adaptive bitrate

A title has several encoded variants.

The client adapts to:

```text
network throughput
device capability
buffer health
```

Tradeoff:

```text
more renditions
→ better playback adaptation
→ more storage/encoding cost
```

---

# Viral-content challenge

A globally anticipated premiere starts at 20:00 UTC.

Unlike random traffic, demand is predictable and synchronized.

Questions:

- pre-position content?
- capacity reserve?
- cache warm-up?
- origin shield?
- what if one ISP cache cluster fails?
- how does client fail over?

---

# Estimation

Estimate:

```text
concurrent viewers
average delivered bitrate
aggregate egress
cache hit/offload
stored encode multiplier
```

Example intuition:

```text
10M concurrent viewers
× 5 Mbps
= 50 Tbps
```

That number instantly explains why “just add more API servers” is irrelevant to the dominant problem.

---

## Exit criterion

You design around **content preparation + edge delivery**, and your first scaling questions are measured in bandwidth/cache locality rather than API QPS alone.
