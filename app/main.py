from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import render_api_summary, render_fix_queue, render_manifest, render_overview
from app.services.schema_service import build_service

app = FastAPI(
    title="Property Schema Publisher",
    version="0.1.0",
    description=(
        "Real estate structured-data publisher for listing schema, entity manifests, and AI-readable property content outputs."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/manifest", response_class=HTMLResponse)
def manifest_page() -> str:
    return render_manifest()


@app.get("/fix-queue", response_class=HTMLResponse)
def fix_queue_page() -> str:
    return render_fix_queue()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/listings")
def listings() -> list[dict]:
    return service.listings()


@app.get("/api/brokerage-schema")
def brokerage_schema() -> dict:
    return service.brokerage_schema()


@app.get("/api/listings/{listing_id}")
def listing(listing_id: str) -> dict:
    value = service.listing(listing_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return value


@app.get("/api/sample")
def sample() -> dict:
    return service.sample_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", "4784"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
