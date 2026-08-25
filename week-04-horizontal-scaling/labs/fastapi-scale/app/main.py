import asyncio
import os
import socket

from fastapi import FastAPI, Query

app = FastAPI(title="Week 4 Scaling Lab")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/instance")
def instance() -> dict[str, str | int]:
    return {
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
    }


@app.get("/slow")
async def slow(seconds: float = Query(default=1.0, ge=0.0, le=10.0)) -> dict[str, float | str]:
    await asyncio.sleep(seconds)
    return {
        "hostname": socket.gethostname(),
        "seconds": seconds,
    }
