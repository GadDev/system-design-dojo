# Optional Lab — RabbitMQ ACKs, Prefetch, Publisher Confirms & DLQ

This lab complements the Redis Streams lab by exposing RabbitMQ's broker model:

```text
Producer
  ↓ publish + confirm
Exchange
  ↓ route
Queue
  ↓ delivery
Consumer
  ↓ manual ACK / reject
DLX → DLQ
```

## Start RabbitMQ

```bash
docker compose up -d
```

Management UI:

```text
http://localhost:15672
```

Credentials:

```text
guest / guest
```

## Install client

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start worker

```bash
python worker.py
```

The worker uses:

```text
manual acknowledgements
prefetch = 1
```

For 30-minute video jobs, this prevents one consumer from hoarding a huge pile of unacknowledged messages.

## Publish

```bash
python producer.py --job-id job-001
```

The producer enables publisher confirms.

Important distinction:

```text
publisher confirm
≠
consumer ACK
```

The first says RabbitMQ accepted publication responsibility. The second says the consumer completed its delivery responsibility.

## DLQ exercise

```bash
python producer.py --job-id job-broken --kind corrupt
```

The worker rejects without requeue. Queue policy sends it through the dead-letter exchange to `transcription.dlq`.

Inspect it in the RabbitMQ management UI.

## Failure experiment

1. Publish several normal messages.
2. Start the worker.
3. Kill the worker during its `sleep(1)` before ACK.
4. Restart it.
5. Observe redelivery.

Now answer:

> What must your real worker do to ensure repeated delivery does not duplicate billing, transcript rows, or provider calls?

## Questions

1. Why is `auto_ack=True` a dangerous default for expensive durable work?
2. How would `prefetch=100` change behavior for 30-minute tasks?
3. Why doesn't a publisher confirm prove a worker completed the job?
4. Why is rejecting a corrupt input different from retrying a 503?
5. What operational process should own `transcription.dlq`?
