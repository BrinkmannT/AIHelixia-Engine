"""
AIHelixia Intelligence Engine
REST API
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from engine import AIHelixiaEngine
from factoryiq.pilot import FactoryIQPilot


VERSION = "0.2.0"


app = FastAPI(
    title="AIHelixia Intelligence Engine API",
    version=VERSION,
    description=(
        "REST API für die AIHelixia Intelligence Engine "
        "und FactoryIQ."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


engine = AIHelixiaEngine()
pilot = FactoryIQPilot(engine)


# ----------------------------------------------------------------------
# API Models
# ----------------------------------------------------------------------


class OutcomeRequest(BaseModel):
    """
    Request für die nachgelagerte Outcome-Bewertung.

    previous_state:
        Zustand vor der Action.

    observed_state:
        Beobachteter Zustand nach der Action.

    action_result:
        Ergebnis der zuvor ausgeführten Action.
    """

    previous_state: dict[str, Any] = Field(
        ...,
        description="Zustand vor der ausgeführten Action.",
    )

    observed_state: dict[str, Any] = Field(
        ...,
        description="Beobachteter Zustand nach der Action.",
    )

    action_result: dict[str, Any] = Field(
        ...,
        description="Ergebnis der ausgeführten Action.",
    )


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def ensure_persistence() -> None:
    """Stellt sicher, dass Persistence verfügbar ist."""
    if engine.persistence.status != "running":
        engine.persistence.start()


# ----------------------------------------------------------------------
# Core
# ----------------------------------------------------------------------


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "AIHelixia Intelligence Engine API",
        "version": VERSION,
        "engine_version": engine.VERSION,
        "status": "online",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "AIHelixia Intelligence Engine API",
        "version": VERSION,
    }


@app.get("/status")
def status() -> dict[str, Any]:
    return engine.get_status()


# ----------------------------------------------------------------------
# Engine lifecycle
# ----------------------------------------------------------------------


@app.post("/engine/start")
def start_engine() -> dict[str, Any]:
    try:
        engine.start()

        return {
            "status": "started",
            "engine": engine.get_status(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/engine/stop")
def stop_engine() -> dict[str, Any]:
    try:
        engine.stop()

        return {
            "status": "stopped",
            "engine": engine.get_status(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ----------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------


@app.get("/factory/overview")
@app.get("/factory/intelligence")
@app.get("/factory/dashboard")
def factory_dashboard() -> dict[str, Any]:
    try:
        if engine.status != "running":
            raise HTTPException(
                status_code=409,
                detail="Engine ist nicht gestartet.",
            )

        return pilot.build_dashboard()

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/factory/ingest")
def ingest_factory(
    factory_data: dict[str, Any],
) -> dict[str, Any]:
    try:
        if engine.status != "running":
            raise HTTPException(
                status_code=409,
                detail="Engine ist nicht gestartet.",
            )

        result = engine.ingest_factory_data(
            factory_data
        )

        return {
            "status": "processed",
            "result": result,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/factory/process")
def process_factory(
    factory_data: dict[str, Any],
) -> dict[str, Any]:
    try:
        if engine.status != "running":
            raise HTTPException(
                status_code=409,
                detail="Engine ist nicht gestartet.",
            )

        process_result = engine.process(
            factory_data
        )

        return {
            "status": "processed",
            "process": process_result,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ----------------------------------------------------------------------
# Intelligence
# ----------------------------------------------------------------------


@app.post("/process")
def process(
    input_data: dict[str, Any],
) -> dict[str, Any]:
    try:
        if engine.status != "running":
            raise HTTPException(
                status_code=409,
                detail="Engine ist nicht gestartet.",
            )

        result = engine.process(
            input_data
        )

        return {
            "status": "processed",
            "result": result,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/outcome")
def evaluate_outcome(
    request: OutcomeRequest,
) -> dict[str, Any]:
    """
    Schließt den Intelligence Closed Loop.

    Action
        ↓
    Observed State
        ↓
    Outcome
        ↓
    Evaluation
        ↓
    Feedback
        ↓
    Outcome Learning
    """

    try:
        if engine.status != "running":
            raise HTTPException(
                status_code=409,
                detail="Engine ist nicht gestartet.",
            )

        result = engine.evaluate_outcome(
            previous_state=request.previous_state,
            observed_state=request.observed_state,
            action_result=request.action_result,
        )

        return {
            "status": "evaluated",
            "result": result,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except TypeError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ----------------------------------------------------------------------
# Persistence
# ----------------------------------------------------------------------


@app.get("/history/{table}")
def history(
    table: str,
    limit: int = 100,
) -> dict[str, Any]:
    """
    Gibt historische Persistence-Daten zurück.

    Erlaubte Tabellen:
    - factory_states
    - measurements
    - alarms
    - engine_events
    - ai_results
    """

    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            table,
            limit,
        )

        return {
            "status": "ok",
            "table": table,
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/factory/history")
def factory_history(
    factory_id: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            "factory_states",
            limit,
        )

        if factory_id is not None:
            records = [
                record
                for record in records
                if record.get("factory_id") == factory_id
            ]

        return {
            "status": "ok",
            "factory_id": factory_id,
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/alarms")
def alarms(
    limit: int = 100,
) -> dict[str, Any]:
    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            "alarms",
            limit,
        )

        return {
            "status": "ok",
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/measurements")
def measurements(
    limit: int = 100,
) -> dict[str, Any]:
    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            "measurements",
            limit,
        )

        return {
            "status": "ok",
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/ai-results")
def ai_results(
    limit: int = 100,
) -> dict[str, Any]:
    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            "ai_results",
            limit,
        )

        return {
            "status": "ok",
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/engine-events")
def engine_events(
    limit: int = 100,
) -> dict[str, Any]:
    try:
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit muss größer als 0 sein.",
            )

        ensure_persistence()

        records = engine.persistence.get_history(
            "engine_events",
            limit,
        )

        return {
            "status": "ok",
            "count": len(records),
            "records": records,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
