#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import uuid

import pika

MAIN_EXCHANGE = "transcription"
MAIN_QUEUE = "transcription.jobs"
DLX = "transcription.dlx"
DLQ = "transcription.dlq"


def declare(ch: pika.adapters.blocking_connection.BlockingChannel) -> None:
    ch.exchange_declare(exchange=MAIN_EXCHANGE, exchange_type="direct", durable=True)
    ch.exchange_declare(exchange=DLX, exchange_type="direct", durable=True)
    ch.queue_declare(queue=DLQ, durable=True)
    ch.queue_bind(queue=DLQ, exchange=DLX, routing_key="dead")
    ch.queue_declare(
        queue=MAIN_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DLX,
            "x-dead-letter-routing-key": "dead",
        },
    )
    ch.queue_bind(queue=MAIN_QUEUE, exchange=MAIN_EXCHANGE, routing_key="job")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", default=f"job_{uuid.uuid4().hex[:8]}")
    parser.add_argument("--kind", choices=["normal", "corrupt"], default="normal")
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = connection.channel()
    declare(ch)

    ch.confirm_delivery()
    body = json.dumps(
        {
            "message_id": f"msg_{uuid.uuid4().hex}",
            "job_id": args.job_id,
            "kind": args.kind,
        }
    )
    ok = ch.basic_publish(
        exchange=MAIN_EXCHANGE,
        routing_key="job",
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
            content_type="application/json",
        ),
        mandatory=True,
    )
    print(f"publisher-confirmed={ok} body={body}")
    connection.close()


if __name__ == "__main__":
    main()
