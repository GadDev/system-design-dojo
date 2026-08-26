import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

function week(
  base: string,
  title: string,
  days: [string, string][],
  extras: [string, string][] = [],
  options: { cheatSheet?: boolean } = {},
) {
  const { cheatSheet = true } = options;
  return {
    text: title,
    collapsed: true,
    items: [
      { text: "Overview", link: `${base}/README` },
      ...days.map(([slug, label]): { text: string; link: string } => ({
        text: label,
        link: `${base}/${slug}`,
      })),
      ...extras.map(([slug, label]): { text: string; link: string } => ({
        text: label,
        link: `${base}/${slug}`,
      })),
      { text: "Review & quiz", link: `${base}/review-and-quiz` },
      ...(cheatSheet ? [{ text: "Cheat sheet", link: `${base}/cheat-sheet` }] : []),
      { text: "Resources", link: `${base}/resources` },
      { text: "Answer key", link: `${base}/answer-key` },
    ],
  };
}

export default withMermaid(defineConfig({
  title: "System Design Dojo",
  description: "A 12-week system-design study curriculum",
  base: "/system-design-dojo/",
  srcDir: ".",
  srcExclude: ["**/node_modules/**", "**/.changeset/**"],
  cleanUrls: true,
  // Labs link to non-Markdown assets (.py, .sql) that VitePress doesn't
  // render as pages, so it flags them as dead links.
  ignoreDeadLinks: [/\.(py|sql)$/],
  rewrites: {
    "README.md": "index.md",
  },

  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Roadmap", link: "/ROADMAP" },
      { text: "Progress", link: "/PROGRESS" },
    ],

    sidebar: [
      {
        text: "Start here",
        items: [
          { text: "Overview", link: "/" },
          { text: "Roadmap", link: "/ROADMAP" },
          { text: "Progress tracker", link: "/PROGRESS" },
          { text: "Book reading plan", link: "/BOOK-READING-PLAN" },
          { text: "Review notes / editorial standard", link: "/REVIEW-NOTES" },
          { text: "Training ladder", link: "/TRAINING-LADDER" },
          { text: "System design notebook", link: "/SYSTEM-DESIGN-NOTEBOOK" },
        ],
      },
      week("/week-01-foundations", "Week 1 — Foundations", [
        ["day-01-request-lifecycle", "Day 1 — Request lifecycle"],
        ["day-02-http-https", "Day 2 — HTTP/HTTPS"],
        ["day-03-dns-cdn", "Day 3 — DNS & CDN"],
        ["day-04-tcp-udp-websockets", "Day 4 — TCP/UDP/WebSockets"],
        ["day-05-load-balancing-statelessness", "Day 5 — Load balancing & statelessness"],
        ["day-06-design-lab-users-api", "Day 6 — Design lab: Users API"],
        ["day-07-review-and-quiz", "Day 7 — Review & quiz"],
      ]),
      week("/week-02-databases", "Week 2 — Databases", [
        ["day-01-sql-vs-nosql", "Day 1 — SQL vs NoSQL"],
        ["day-02-keys-relationships-constraints", "Day 2 — Keys, relationships, constraints"],
        ["day-03-indexes-query-plans", "Day 3 — Indexes & query plans"],
        ["day-04-transactions-acid-mvcc", "Day 4 — Transactions, ACID, MVCC"],
        ["day-05-connections-pooling", "Day 5 — Connections & pooling"],
        ["day-06-replication-partitioning-sharding", "Day 6 — Replication, partitioning, sharding"],
        ["day-07-design-lab-transcription-data", "Day 7 — Design lab: transcription data"],
      ], [
        ["database-decision-template", "Decision template"],
        ["labs/local-postgres", "Lab: local Postgres"],
      ]),
      week("/week-03-caching", "Week 3 — Caching", [
        ["day-01-cache-fundamentals-redis", "Day 1 — Cache fundamentals & Redis"],
        ["day-02-cache-aside-key-design", "Day 2 — Cache-aside & key design"],
        ["day-03-ttl-expiration-eviction-invalidation", "Day 3 — TTL, expiration, eviction, invalidation"],
        ["day-04-stampede-hot-keys-negative-caching", "Day 4 — Stampede, hot keys, negative caching"],
        ["day-05-distributed-cache-redis-cluster", "Day 5 — Distributed cache & Redis Cluster"],
        ["day-06-reliability-observability-transcription", "Day 6 — Reliability & observability"],
        ["day-07-design-lab-url-shortener", "Day 7 — Design lab: URL shortener"],
      ], [
        ["cache-decision-template", "Decision template"],
        ["labs/local-redis", "Lab: local Redis"],
      ]),
      week("/week-04-horizontal-scaling", "Week 4 — Horizontal scaling", [
        ["day-01-horizontal-vs-vertical-stateless", "Day 1 — Horizontal vs vertical & statelessness"],
        ["day-02-load-balancing-health-sticky-sessions", "Day 2 — Load balancing, health, sticky sessions"],
        ["day-03-autoscaling-capacity-signals", "Day 3 — Autoscaling & capacity signals"],
        ["day-04-rate-limiting-quotas", "Day 4 — Rate limiting & quotas"],
        ["day-05-backpressure-admission-load-shedding", "Day 5 — Backpressure, admission, load shedding"],
        ["day-06-scalable-upload-architecture", "Day 6 — Scalable upload architecture"],
        ["day-07-design-lab-10000-uploads", "Day 7 — Design lab: 10,000 uploads"],
      ], [
        ["scaling-decision-template", "Decision template"],
      ]),
      week("/week-05-queues-workers", "Week 5 — Queues & workers", [
        ["day-01-queue-mental-model", "Day 1 — Queue mental model"],
        ["day-02-delivery-semantics-acks-ordering", "Day 2 — Delivery semantics, acks, ordering"],
        ["day-03-idempotency-outbox", "Day 3 — Idempotency & outbox"],
        ["day-04-redis-rabbitmq-kafka", "Day 4 — Redis, RabbitMQ, Kafka"],
        ["day-05-retries-dlq-poison-messages", "Day 5 — Retries, DLQ, poison messages"],
        ["day-06-transcription-queue-architecture", "Day 6 — Transcription queue architecture"],
        ["day-07-design-lab-async-transcription", "Day 7 — Design lab: async transcription"],
      ], [
        ["queue-decision-template", "Decision template"],
        ["labs/kafka-basics", "Lab: Kafka basics"],
      ]),
      week("/week-06-distributed-processing", "Week 6 — Distributed processing", [
        ["day-01-fan-out-fan-in-parallelism", "Day 1 — Fan-out/fan-in parallelism"],
        ["day-02-work-partitioning-chunk-size", "Day 2 — Work partitioning & chunk size"],
        ["day-03-job-orchestration-bounded-concurrency", "Day 3 — Job orchestration & bounded concurrency"],
        ["day-04-fan-in-aggregation-ordering-stragglers", "Day 4 — Fan-in aggregation, ordering, stragglers"],
        ["day-05-race-conditions-locks-idempotency", "Day 5 — Race conditions, locks, idempotency"],
        ["day-06-orchestration-tools-transcription", "Day 6 — Orchestration tools & transcription"],
        ["day-07-design-lab-90-minute-transcription", "Day 7 — Design lab: 90-minute transcription"],
      ], [
        ["distributed-processing-decision-template", "Decision template"],
        ["labs/README", "Labs overview"],
      ]),
      week("/week-07-reliability", "Week 7 — Reliability", [
        ["day-01-failure-models-timeouts", "Day 1 — Failure models & timeouts"],
        ["day-02-retries-backoff-jitter", "Day 2 — Retries, backoff, jitter"],
        ["day-03-circuit-breakers-bulkheads", "Day 3 — Circuit breakers & bulkheads"],
        ["day-04-graceful-degradation-health-shutdown", "Day 4 — Graceful degradation, health, shutdown"],
        ["day-05-failover-rto-rpo", "Day 5 — Failover, RTO, RPO"],
        ["day-06-transcription-recovery-playbook", "Day 6 — Transcription recovery playbook"],
        ["day-07-chaos-design-lab", "Day 7 — Chaos design lab"],
      ], [
        ["reliability-decision-template", "Decision template"],
        ["failure-matrix-template", "Failure matrix template"],
        ["game-day-template", "Game day template"],
        ["labs/README", "Labs overview"],
      ]),
      week("/week-08-observability", "Week 8 — Observability", [
        ["day-01-structured-logs-correlation", "Day 1 — Structured logs & correlation"],
        ["day-02-metrics-prometheus-cardinality", "Day 2 — Metrics, Prometheus, cardinality"],
        ["day-03-distributed-tracing-opentelemetry", "Day 3 — Distributed tracing & OpenTelemetry"],
        ["day-04-sli-slo-sla-error-budgets", "Day 4 — SLI, SLO, SLA, error budgets"],
        ["day-05-grafana-dashboards-alerting", "Day 5 — Grafana dashboards & alerting"],
        ["day-06-incident-lab-stuck-job", "Day 6 — Incident lab: stuck job"],
        ["day-07-review-observability-scorecard", "Day 7 — Review: observability scorecard"],
      ], [
        ["observability-decision-template", "Decision template"],
        ["alert-runbook-template", "Alert runbook template"],
        ["dashboard-plan", "Dashboard plan"],
        ["incident-investigation-template", "Incident investigation template"],
        ["labs/README", "Labs overview"],
      ]),
      week("/week-09-consistency-distributed-data", "Week 9 — Consistency & distributed data", [
        ["day-01-strong-vs-eventual-consistency", "Day 1 — Strong vs eventual consistency"],
        ["day-02-cap-partitions-replica-lag", "Day 2 — CAP, partitions, replica lag"],
        ["day-03-optimistic-concurrency", "Day 3 — Optimistic concurrency"],
        ["day-04-distributed-transactions-2pc", "Day 4 — Distributed transactions & 2PC"],
        ["day-05-event-driven-consistency", "Day 5 — Event-driven consistency"],
        ["day-06-sagas-source-of-truth-reconciliation", "Day 6 — Sagas, source of truth, reconciliation"],
        ["day-07-design-lab-consistency-contract", "Day 7 — Design lab: consistency contract"],
      ], [
        ["consistency-decision-template", "Decision template"],
        ["consistency-contract-template", "Consistency contract template"],
        ["source-of-truth-matrix-template", "Source of truth matrix template"],
        ["labs/README", "Labs overview"],
      ]),
      week("/week-10-architecture-patterns", "Week 10 — Architecture patterns", [
        ["day-01-modular-monolith", "Day 1 — Modular monolith"],
        ["day-02-microservices-extraction", "Day 2 — Microservices extraction"],
        ["day-03-event-driven-architecture", "Day 3 — Event-driven architecture"],
        ["day-04-cqrs", "Day 4 — CQRS"],
        ["day-05-event-sourcing", "Day 5 — Event sourcing"],
        ["day-06-saga-pattern", "Day 6 — Saga pattern"],
        ["day-07-design-lab-evolve-transcription-saas", "Day 7 — Design lab: evolve transcription SaaS"],
      ], [
        ["architecture-pattern-decision-template", "Decision template"],
        ["pattern-decision-matrix", "Pattern decision matrix"],
        ["event-contract-template", "Event contract template"],
        ["service-extraction-scorecard", "Service extraction scorecard"],
        ["labs/README", "Labs overview"],
      ]),
      week("/week-11-system-design-interview", "Week 11 — System design interview", [
        ["day-01-requirements-scope", "Day 1 — Requirements & scope"],
        ["day-02-estimation-capacity", "Day 2 — Estimation & capacity"],
        ["day-03-api-data-model", "Day 3 — API & data model"],
        ["day-04-architecture-bottlenecks", "Day 4 — Architecture & bottlenecks"],
        ["day-05-tradeoffs-communication", "Day 5 — Tradeoffs & communication"],
        ["day-06-training-ladder-1-6", "Day 6 — Training ladder 1–6"],
        ["day-07-full-mock-self-review", "Day 7 — Full mock & self-review"],
      ], [
        ["interview-template", "Interview template"],
        ["design-notebook-template", "Design notebook template"],
        ["estimation-cheat-sheet", "Estimation cheat sheet"],
        ["scoring-rubric", "Scoring rubric"],
        ["practice/README", "Practice: overview"],
        ["practice/01-url-shortener", "Practice: URL shortener"],
        ["practice/02-pastebin", "Practice: Pastebin"],
        ["practice/03-rate-limiter", "Practice: Rate limiter"],
        ["practice/04-notification-system", "Practice: Notification system"],
        ["practice/05-file-upload-service", "Practice: File upload service"],
        ["practice/06-chat-system", "Practice: Chat system"],
      ], { cheatSheet: false }),
      week("/week-12-capstone-mastery", "Week 12 — Capstone mastery", [
        ["day-01-video-transcription", "Day 1 — Video transcription"],
        ["day-02-youtube-lite", "Day 2 — YouTube lite"],
        ["day-03-twitter-feed", "Day 3 — Twitter feed"],
        ["day-04-uber-geospatial", "Day 4 — Uber geospatial"],
        ["day-05-dropbox-sync", "Day 5 — Dropbox sync"],
        ["day-06-netflix-streaming", "Day 6 — Netflix streaming"],
        ["day-07-final-boss-100k-hours", "Day 7 — Final boss: 100k hours"],
      ], [
        ["portfolio-case-study-template", "Portfolio case study template"],
        ["graduation-rubric", "Graduation rubric"],
        ["practice/07-video-transcription", "Practice: Video transcription"],
        ["practice/08-youtube", "Practice: YouTube"],
        ["practice/09-twitter-feed", "Practice: Twitter feed"],
        ["practice/10-uber", "Practice: Uber"],
        ["practice/11-dropbox", "Practice: Dropbox"],
        ["practice/12-netflix", "Practice: Netflix"],
      ]),
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/GadDev/system-design-dojo" },
    ],

    search: {
      provider: "local",
    },
  },
}));
