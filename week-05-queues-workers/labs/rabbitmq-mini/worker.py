#!/usr/bin/env python3
from __future__ import annotations

import json
import time

import pika

from producer import DLQ, DLX, MAIN_EXCHANGE, MAIN_QUEUE, declare


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = connection.channel()
    declare(ch)

    # Keep at most one unacknowledged long-running job in flight for this demo.
    ch.basic_qos(prefetch_count=1)

    def handle(channel, method, properties, body: bytes) -> None:
        message = json.loads(body)
        print("received", message, "redelivered=", method.redelivered)

        if message.get("kind") == "corrupt":
            print("permanent failure → reject without requeue → DLX/DLQ")
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            return

        time.sleep(1)
        print("durable business work would commit here")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print("ACK", message["job_id"])

    ch.basic_consume(queue=MAIN_QUEUE, on_message_callback=handle, auto_ack=False)
    print("waiting; Ctrl+C to exit")
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        ch.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
