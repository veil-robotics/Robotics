from __future__ import annotations

from fastapi import FastAPI

from ..core.job_runner import JobRunner
from ..core.job_store import InMemoryJobStore
from .routes.jobs import router as jobs_router
from .routes.output import router as output_router


def create_app() -> FastAPI:
    app = FastAPI(title="Video Anonymization API")
    store = InMemoryJobStore()
    runner = JobRunner(store)
    app.state.store = store
    app.state.runner = runner
    app.include_router(jobs_router)
    app.include_router(output_router)
    return app


app = create_app()
