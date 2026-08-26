import { defineConfig } from "vitepress";

function week(
  base: string,
  title: string,
  days: [string, string][],
  extras: [string, string][] = [],
) {
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
      { text: "Cheat sheet", link: `${base}/cheat-sheet` },
      { text: "Resources", link: `${base}/resources` },
      { text: "Answer key", link: `${base}/answer-key` },
    ],
  };
}

export default defineConfig({
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
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/GadDev/system-design-dojo" },
    ],

    search: {
      provider: "local",
    },
  },
});
