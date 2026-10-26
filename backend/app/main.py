from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.reports import router as reports_router

app = FastAPI(title="Indian Market Morning Scanner", version="0.1.0")

app.include_router(reports_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Indian Market Morning Scanner Backend"}
