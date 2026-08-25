# Lab — Run PostgreSQL Locally

This lab gives you a disposable PostgreSQL 18 instance for Week 2.

## Option A — Docker

```bash
docker run --name system-design-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=system_design \
  -p 5432:5432 \
  -d postgres:18
```

Connect:

```bash
docker exec -it system-design-postgres \
  psql -U postgres -d system_design
```

Stop:

```bash
docker stop system-design-postgres
```

Start again:

```bash
docker start system-design-postgres
```

Delete the lab:

```bash
docker rm -f system-design-postgres
```

---

# Load the sample schema

From the repository root:

```bash
docker exec -i system-design-postgres \
  psql -U postgres -d system_design \
  < week-02-databases/labs/transcription-schema.sql
```

---

# Useful psql commands

```text
\dt          list tables
\d jobs      describe table
\di          list indexes
\x           expanded display
\timing      show query timing
```

---

# Day 3 experiment

1. Insert/generated sample job rows.
2. Run a job-history query.
3. `EXPLAIN (ANALYZE, BUFFERS)` it.
4. Create the recommended composite index.
5. Run the plan again.
6. Compare scan type, estimates, actual time, buffers.

Do not obsess over tiny local timings. Focus on the plan shape.

---

# Day 4 transaction experiment

Open two terminal sessions.

Session A:

```sql
BEGIN;
UPDATE jobs
SET completed_chunks = completed_chunks + 1
WHERE id = '<job id>';
```

Do not commit yet.

Session B:

Try another update on the same row.

Observe waiting/locking behavior.

Then commit A.

The point is to make concurrency visible instead of abstract.

---

# Day 5 connection observation

Run:

```sql
SELECT pid, usename, state, query
FROM pg_stat_activity
ORDER BY state, pid;
```

Observe database sessions while opening multiple `psql` clients.

A pooler is easier to understand after you have seen that "connection" is a real server-side resource.
