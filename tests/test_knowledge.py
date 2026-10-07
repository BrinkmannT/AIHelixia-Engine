from core.knowledge import Knowledge


def test_query_all_outcomes_consistent():
    knowledge = Knowledge()
    knowledge.start()

    memory_entries = [
        {
            "data": {
                "machine_id": "M-001",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "degraded",
            }
        },
        {
            "data": {
                "machine_id": "M-002",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "degraded",
            }
        },
    ]

    result = knowledge.query(
        memory_entries=memory_entries,
        signal_types=[
            "temperature_elevated",
            "vibration_elevated",
        ],
    )

    assert result["matched_case_count"] == 2
    assert result["support_count"] == 2
    assert result["outcomes"] == {"degraded": 2}
    assert result["dominant_outcome"] == "degraded"
    assert result["dominant_outcome_ratio"] == 1.0
    assert result["evidence_strength"] == "moderate"

    knowledge.stop()


def test_query_mixed_outcomes():
    knowledge = Knowledge()
    knowledge.start()

    memory_entries = [
        {
            "data": {
                "machine_id": f"M-{index:03d}",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": outcome,
            }
        }
        for index, outcome in enumerate(
            [
                "degraded",
                "degraded",
                "degraded",
                "improved",
                "improved",
            ],
            start=1,
        )
    ]

    result = knowledge.query(
        memory_entries=memory_entries,
        signal_types=[
            "temperature_elevated",
            "vibration_elevated",
        ],
    )

    assert result["matched_case_count"] == 5
    assert result["support_count"] == 5
    assert result["outcomes"] == {
        "degraded": 3,
        "improved": 2,
    }
    assert result["dominant_outcome"] == "degraded"
    assert result["dominant_outcome_ratio"] == 0.6
    assert result["evidence_strength"] == "strong"

    knowledge.stop()


def test_query_unknown_outcome_is_not_counted_as_support():
    knowledge = Knowledge()
    knowledge.start()

    memory_entries = [
        {
            "data": {
                "machine_id": "M-001",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "degraded",
            }
        },
        {
            "data": {
                "machine_id": "M-002",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "degraded",
            }
        },
        {
            "data": {
                "machine_id": "M-003",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "degraded",
            }
        },
        {
            "data": {
                "machine_id": "M-004",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "outcome": "improved",
            }
        },
        {
            "data": {
                "machine_id": "M-005",
                "signal_types": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
            }
        },
    ]

    result = knowledge.query(
        memory_entries=memory_entries,
        signal_types=[
            "temperature_elevated",
            "vibration_elevated",
        ],
    )

    assert result["matched_case_count"] == 5
    assert result["support_count"] == 4
    assert result["outcomes"] == {
        "degraded": 3,
        "improved": 1,
    }
    assert result["dominant_outcome"] == "degraded"
    assert result["dominant_outcome_ratio"] == 0.75
    assert result["evidence_strength"] == "moderate"

    knowledge.stop()
