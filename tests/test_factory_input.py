from core.factory_input import FactoryInput
from core.world_state import WorldState


def valid_factory_data():
    return {
        "factory": {
            "id": "FACTORY-001",
            "name": "Test Factory",
            "location": "Schwedt",
            "status": "running",
        },
        "production_lines": [
            {
                "id": "LINE-001",
                "name": "Production Line 1",
                "status": "running",
            }
        ],
        "machines": [
            {
                "id": "MACHINE-001",
                "name": "Machine 1",
                "production_line_id": "LINE-001",
                "status": "running",
            }
        ],
        "sensors": [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
            }
        ],
        "production": {
            "output": 500,
            "target": 500,
            "status": "running",
        },
        "energy": {
            "consumption": 120,
            "unit": "kWh",
            "status": "normal",
        },
        "maintenance": {
            "machine_id": "MACHINE-001",
            "status": "scheduled",
            "type": "preventive",
        },
        "alarms": [
            {
                "id": "ALARM-001",
                "timestamp": "2026-09-26T18:00:00+00:00",
                "machine_id": "MACHINE-001",
                "severity": "warning",
                "type": "temperature",
                "message": "Temperature above threshold",
            }
        ],
    }


def test_factory_input_lifecycle():
    factory_input = FactoryInput()

    assert factory_input.get_status()["status"] == "created"

    factory_input.start()

    assert factory_input.get_status()["status"] == "running"

    factory_input.stop()

    assert factory_input.get_status()["status"] == "stopped"


def test_validate_complete_factory_input():
    factory_input = FactoryInput()

    result = factory_input.validate(valid_factory_data())

    assert result["valid"] is True
    assert result["version"] == "0.2.0"


def test_validate_rejects_non_dictionary():
    factory_input = FactoryInput()

    try:
        factory_input.validate(None)
        assert False
    except TypeError as exc:
        assert "Dictionary" in str(exc)


def test_validate_rejects_unknown_field():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["unknown_field"] = True

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "Unbekannte FactoryIQ Felder" in str(exc)


def test_validate_rejects_wrong_list_type():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["machines"] = {}

    try:
        factory_input.validate(data)
        assert False
    except TypeError as exc:
        assert "muss eine Liste sein" in str(exc)


def test_validate_rejects_invalid_machine_id():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["machines"][0]["id"] = ""

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "gültiges 'id' Feld" in str(exc)


def test_validate_rejects_invalid_machine_status():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["machines"][0]["status"] = "invalid"

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "ungültigen Status" in str(exc)


def test_validate_rejects_invalid_sensor_id():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["sensors"][0]["id"] = ""

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "gültiges 'id' Feld" in str(exc)


def test_validate_rejects_invalid_alarm_id():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["alarms"][0]["id"] = ""

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "gültiges 'id' Feld" in str(exc)


def test_validate_rejects_invalid_alarm_severity():
    factory_input = FactoryInput()

    data = valid_factory_data()
    data["alarms"][0]["severity"] = "invalid"

    try:
        factory_input.validate(data)
        assert False
    except ValueError as exc:
        assert "ungültige severity" in str(exc)


def test_ingest_requires_running_factory_input():
    factory_input = FactoryInput()
    world_state = WorldState()

    world_state.start()

    try:
        factory_input.ingest(
            valid_factory_data(),
            world_state,
        )
        assert False
    except RuntimeError as exc:
        assert "FactoryInput ist nicht gestartet" in str(exc)


def test_ingest_requires_running_world_state():
    factory_input = FactoryInput()
    world_state = WorldState()

    factory_input.start()

    try:
        factory_input.ingest(
            valid_factory_data(),
            world_state,
        )
        assert False
    except RuntimeError as exc:
        assert "World State ist nicht gestartet" in str(exc)


def test_ingest_complete_factory_input():
    factory_input = FactoryInput()
    world_state = WorldState()

    factory_input.start()
    world_state.start()

    result = factory_input.ingest(
        valid_factory_data(),
        world_state,
    )

    assert result["status"] == "processed"
    assert result["version"] == "0.2.0"
    assert result["processed_count"] == 1
    assert result["processed"]["factory"] is True
    assert result["processed"]["production_lines"] == 1
    assert result["processed"]["machines"] == 1
    assert result["processed"]["sensors"] == 1
    assert result["processed"]["production"] is True
    assert result["processed"]["energy"] is True
    assert result["processed"]["maintenance"] is True
    assert result["processed"]["alarms"] == 1
