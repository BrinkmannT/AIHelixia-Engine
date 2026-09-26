from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def ensure_engine_stopped() -> None:
    response = client.get("/status")
    assert response.status_code == 200

    if response.json()["status"] == "running":
        response = client.post("/engine/stop")
        assert response.status_code == 200


def start_engine() -> None:
    ensure_engine_stopped()

    response = client.post("/engine/start")

    assert response.status_code == 200
    assert response.json()["status"] == "started"


def stop_engine() -> None:
    response = client.get("/status")
    assert response.status_code == 200

    if response.json()["status"] == "running":
        response = client.post("/engine/stop")

        assert response.status_code == 200
        assert response.json()["status"] == "stopped"


def test_health():
    ensure_engine_stopped()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "AIHelixia Intelligence Engine API"
    assert data["version"] == "0.2.0"


def test_root():
    ensure_engine_stopped()

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "AIHelixia Intelligence Engine API"
    assert data["version"] == "0.2.0"
    assert data["engine_version"] == "0.5.2"
    assert data["status"] == "online"


def test_engine_lifecycle():
    ensure_engine_stopped()

    start_engine()

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "running"

    stop_engine()

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "stopped"


def test_process_requires_running_engine():
    ensure_engine_stopped()

    response = client.post(
        "/process",
        json={"test": True},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Engine ist nicht gestartet."


def test_process_empty_input():
    start_engine()

    try:
        response = client.post(
            "/process",
            json={},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "processed"
        assert data["result"]["status"] == "completed"

    finally:
        stop_engine()


def test_outcome_successful_closed_loop():
    start_engine()

    try:
        payload = {
            "previous_state": {
                "temperature": 86,
                "vibration": 4.2,
                "production": 490,
                "energy": 128,
            },
            "observed_state": {
                "temperature": 68,
                "vibration": 2.1,
                "production": 490,
                "energy": 128,
            },
            "action_result": {
                "status": "executed",
                "result": {
                    "success": True,
                },
            },
        }

        response = client.post(
            "/outcome",
            json=payload,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "evaluated"

        result = data["result"]

        assert result["outcome"]["outcome"] == "improved"
        assert result["outcome"]["success"] is True

        # Die aktuelle Outcome-Engine bewertet die vier
        # vorhandenen Metriken. Zwei verbessern sich,
        # zwei bleiben unverändert.
        assert result["outcome"]["confidence"] == 0.5

        assert result["evaluation"]["evaluation"] == "successful"
        assert result["evaluation"]["outcome_known"] is True

        assert result["feedback"]["feedback_type"] == "positive"
        assert result["feedback"]["signal"] == "reinforce"

        assert (
            result["learning_memory"]["type"]
            == "outcome_learning"
        )

    finally:
        stop_engine()


def test_outcome_validation():
    start_engine()

    try:
        response = client.post(
            "/outcome",
            json={},
        )

        assert response.status_code == 422

    finally:
        stop_engine()


def test_outcome_type_validation():
    start_engine()

    try:
        response = client.post(
            "/outcome",
            json={
                "previous_state": "invalid",
                "observed_state": {},
                "action_result": {},
            },
        )

        assert response.status_code == 422

    finally:
        stop_engine()


def test_invalid_history_limit():
    ensure_engine_stopped()

    response = client.get("/alarms?limit=0")

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "limit muss größer als 0 sein."
    )


def test_factory_process_requires_running_engine():
    ensure_engine_stopped()

    response = client.post(
        "/factory/process",
        json={},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Engine ist nicht gestartet."
