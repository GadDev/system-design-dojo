import json
import logging
import os
import random
import time
import uuid

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": record.levelname.lower(),
            "service": "demo-api",
            "event": getattr(record, "event", "application.log"),
            "message": record.getMessage(),
        }
        for field in ("job_id", "chunk_index", "trace_id"):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("demo")
logger.handlers = [handler]
logger.setLevel(logging.INFO)

resource = Resource.create({"service.name": "transcription-demo-api"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
            insecure=True,
        )
    )
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("transcription-demo")

REQUESTS = Counter(
    "demo_http_requests_total",
    "Demo HTTP requests",
    ["route", "status_class"],
)
DURATION = Histogram(
    "demo_http_request_duration_seconds",
    "Demo request duration",
    ["route"],
)
QUEUE_DEPTH = Gauge("demo_transcription_queue_depth", "Synthetic queue depth")

app = FastAPI()
QUEUE_DEPTH.set(7)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    started = time.perf_counter()
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    with tracer.start_as_current_span("transcription.job.accept") as span:
        span.set_attribute("transcription.stage", "accept")
        span.set_attribute("transcription.job_id", job_id)
        trace_id = format(span.get_span_context().trace_id, "032x")
        time.sleep(random.uniform(0.01, 0.08))
        logger.info(
            "job accepted",
            extra={"event": "job.accepted", "job_id": job_id, "trace_id": trace_id},
        )
    REQUESTS.labels(route="/jobs", status_class="2xx").inc()
    DURATION.labels(route="/jobs").observe(time.perf_counter() - started)
    return {"job_id": job_id, "status": "queued"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
