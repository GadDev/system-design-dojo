# Lab — Redis Streams At-Least-Once Worker

This lab makes the Week 5 lifecycle visible:

```text
XADD
 ↓
XREADGROUP
 ↓
pending entry
 ↓
durable business effect
 ↓
XACK
```

It also demonstrates the classic failure window:

```text
DB COMMIT ✅
worker crashes ❌
XACK never happens
```

The message remains pending and can be reclaimed/redelivered. The local SQLite unique records make the durable effect idempotent.

## 1. Start Redis

```bash
docker compose up -d
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Start worker

```bash
python worker.py --consumer worker-a
```

## 4. Publish a normal job

In another terminal:

```bash
python producer.py --job-id job-001 --media-key uploads/demo.mp4
```

Observe:

```text
receive
processing
durable commit
ACK
```

## 5. Inspect queue

```bash
python inspect_queue.py
```

## 6. Demonstrate crash after commit

Stop the worker, then:

```bash
CRASH_AFTER_COMMIT=1 python worker.py --consumer crashy-worker
```

Publish:

```bash
python producer.py --job-id job-002
```

The worker exits after the SQLite transaction but before `XACK`.

Inspect:

```bash
python inspect_queue.py
```

You should see pending work.

## 7. Reclaim abandoned work

After at least one second:

```bash
python reclaim.py --idle-ms 1000
```

`XAUTOCLAIM` transfers ownership of stale pending work.

For the exercise, now reason how your production recovery worker would process claimed messages and ACK them. You can also modify `worker.py` to read pending entries for its consumer before requesting `>` new entries.

The key lesson is not the exact recovery loop. It is:

> A worker can die after the business effect committed and before the broker learned that it finished.

Therefore duplicate-safe processing is mandatory.

## 8. Permanent failure → DLQ

```bash
python producer.py --job-id job-broken --kind corrupt
```

The worker publishes a small failure record to:

```text
transcription:dlq
```

and acknowledges the original message.

Inspect:

```bash
python inspect_queue.py
```

## 9. Run multiple workers

Open two terminals:

```bash
python worker.py --consumer worker-a
python worker.py --consumer worker-b
```

Publish several jobs and observe the consumer group distribute work.

## Questions

1. What would happen if `persist_success()` performed a credit-card charge instead of a local DB insert?
2. Why does `INSERT OR IGNORE` help this lab but not solve arbitrary external side effects?
3. What threshold should production use before reclaiming a pending message?
4. What happens if processing legitimately takes longer than the reclaim idle threshold?
5. What metrics would you export instead of running `inspect_queue.py` manually?
