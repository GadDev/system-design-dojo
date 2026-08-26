# Week 12 — Real-World Architecture Reading Map

Use these **after** designing each system yourself. The goal is comparison, not memorization.

---

# Day 1 — Video transcription

Revisit:

- Cloudflare R2 multipart uploads: https://developers.cloudflare.com/r2/objects/multipart-objects/
- FFmpeg formats/segmenting: https://ffmpeg.org/ffmpeg-formats.html
- OpenTelemetry: https://opentelemetry.io/docs/

---

# Day 2 — YouTube-lite

### YouTube resumable upload protocol

- https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol

The current protocol explicitly supports pausing/resuming large video uploads and recovering uploaded byte ranges after interruption.

### Google Cloud Transcoder

- https://docs.cloud.google.com/transcoder/docs/concepts/overview

Useful model for asynchronous media-transcoding jobs with object-storage inputs/outputs.

### Media CDN

- https://docs.cloud.google.com/media-cdn/docs
- https://docs.cloud.google.com/media-cdn/docs/origins

Useful for edge caching, origin shielding and media delivery.

---

# Day 3 — Twitter/X-style feed

### X/Twitter infrastructure at scale

- https://blog.x.com/engineering/en_us/topics/infrastructure/2017/the-infrastructure-behind-twitter-scale
- https://blog.x.com/engineering/en_us/a/2013/new-tweets-per-second-record-and-how

Use these for lessons around timeline caches, service decomposition, sharded storage and scaling evolution — not as a current implementation blueprint.

---

# Day 4 — Uber-like dispatch

### Uber H3

- https://www.uber.com/gb/en/blog/h3/

Use it to understand why hierarchical spatial indexing is useful for marketplace/geospatial workloads.

### High-QPS geospatial query example

- https://www.uber.com/us/en/blog/orders-near-you/

---

# Day 5 — Dropbox-lite

### Sync engine

- https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine

Key lesson: offline clients/network partitions are ordinary conditions for sync.

### Magic Pocket

- https://dropbox.tech/infrastructure/inside-the-magic-pocket

Key lesson: separate immutable file-content blocks from higher-level mutable metadata/revision logic.

### Recent storage-efficiency evolution

- https://dropbox.tech/infrastructure/improving-storage-efficiency-in-magic-pocket-our-immutable-blob-store

Useful reminder that architecture continues to evolve under cost/efficiency pressure.

---

# Day 6 — Netflix-lite

### Netflix Open Connect

- https://openconnect.netflix.com/
- https://openconnect.netflix.com/Open-Connect-Overview.pdf

Use as a real-world CDN case: localize massive media traffic near viewers/ISPs and reduce upstream network load.

### Google Media CDN (comparison)

- https://docs.cloud.google.com/media-cdn/docs

---

# Day 7 — final transcription capstone

No new reading before the design.

Afterward compare your design against:

- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Google SRE: https://sre.google/sre-book/table-of-contents/
- System Design Primer: https://github.com/donnemartin/system-design-primer

---

# Books for the final phase

- **Designing Data-Intensive Applications, 2nd Edition** — consistency/dataflow depth.
- **System Design Interview Vol. 1/2** — practice comparison after your own attempt.
- **Building Microservices, 2nd Edition** — architecture evolution.
- **Site Reliability Engineering** — production/reliability lens.
- **Release It!, 2nd Edition** — failure behavior.

Every real-world architecture article should end with:

> **“Which parts exist because of that company's actual workload, and which parts would be premature for my system?”**
