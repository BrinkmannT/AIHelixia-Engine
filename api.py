"""
AIHelixia Intelligence Engine
REST API
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException

from engine import AIHelixiaEngine


VERSION = "0.1.0"


app = FastAPI(
    title="AIHelixia Intelligence Engine API",
    version=VERSION,
    description="REST API für die AIHelixia Intelligence Engine und FactoryIQ.",
)


engine = AIHelixiaEngine()


def ensure_persistence() -> None:
    """Stellt sicher, dass Persistence verfügbar ist."""
    if engine.persistence.status != "running":
        engine.persistence.start()


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

        result = engine.ingest_factory_data(factory_data)

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

        result = engine.process(input_data)

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
