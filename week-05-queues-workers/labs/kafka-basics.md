# Lab Notes — Kafka Basics Without Hiding the Model

This is a conceptual/CLI lab rather than a full local Kafka stack.

The goal is to understand:

```text
topic
partition
record key
offset
consumer group
replay
```

## Model

Imagine:

```text
topic: transcription-events
partitions: 4
```

Publish:

```text
key=job_001 value=JobRequested
key=job_002 value=JobRequested
key=job_001 value=JobCompleted
```

A stable key can keep events for `job_001` in the same partition, which gives an ordering scope for that job.

## Consumer groups

Create two logical groups:

```text
transcription-workers
analytics
```

Both groups can independently consume the same retained events.

Within `transcription-workers`, partitions are distributed across consumers.

If there are:

```text
4 partitions
10 consumers
```

at most four consumers can actively own those four partitions for that group at one time.

## Offset exercise

Suppose partition 2 contains:

```text
offset 100 JobRequested(job_9)
offset 101 JobStarted(job_9)
offset 102 JobCompleted(job_9)
```

Consumer commits offset after 102.

Later a bug is discovered.

Kafka-style retention/replay lets you reset the consumer position and reprocess old records.

Ask:

> Would replaying `JobCompleted` send duplicate emails or charges in your consumers?

If yes, replayability makes idempotency **more**, not less, important.

## Commands to investigate on a Kafka installation

Exact scripts vary by distribution/version, but learn the operations conceptually:

```text
create topic
produce keyed records
consume with group A
consume with group B
describe topic partitions
describe consumer-group offsets
reset group offsets for replay
```

Use the official Kafka documentation for the current CLI syntax of your installation:

- https://kafka.apache.org/documentation/

## Design questions

1. Why might Kafka be useful if billing, analytics, audit, and notifications all need `JobCompleted`?
2. Why might RabbitMQ/Redis still be simpler if only one worker pool needs the job?
3. What key would you choose if order matters per job?
4. What throughput/parallelism constraint does partition count create?
5. Why doesn't Kafka retention itself guarantee safe replay?
