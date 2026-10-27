"""
FastAPI app — Fast Draw reflex game.

Run: uvicorn main:app --reload --port 3023
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from fast_draw_core import config_for_client, evaluate_reaction, random_wait_seconds  # noqa: E402

app = FastAPI(title="Fast Draw")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class EvaluateRequest(BaseModel):
    elapsed_sec: float = Field(..., ge=0, le=30)
    early: bool = False


class WaitResponse(BaseModel):
    wait_sec: float


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.get("/api/config")
async def api_config() -> JSONResponse:
    return JSONResponse(config_for_client())


@app.get("/api/wait")
async def api_wait() -> JSONResponse:
    return JSONResponse({"wait_sec": random_wait_seconds()})


@app.post("/api/evaluate")
async def api_evaluate(body: EvaluateRequest) -> JSONResponse:
    try:
        return JSONResponse(
            evaluate_reaction(body.elapsed_sec, early=body.early),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
