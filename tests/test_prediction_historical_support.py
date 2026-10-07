from core.prediction import Prediction


def test_prediction_uses_historical_support():
    prediction = Prediction()
    prediction.start()

    world_state = {
        "machines": [
            {
                "id": "M-001",
                "status": "degraded",
            }
        ]
    }

    reasoning = {
        "industrial_analysis": {},
        "anomaly_analysis": {
            "status": "anomaly_detected",
            "severity": "medium",
            "signals": [
                {"type": "temperature_elevated"},
                {"type": "vibration_elevated"},
            ],
            "correlated_machines": ["M-001"],
        },
        "historical_outcome_analysis": {
            "status": "available",
            "known_outcome_count": 5,
            "average_confidence": 0.9,
            "dominant_outcome": "degraded",
            "success_rate": 0.8,
            "improved_count": 1,
            "degraded_count": 4,
            "unchanged_count": 0,
        },
    }

    result = prediction.predict(world_state, reasoning)

    assert result["status"] == "prediction_completed"

    historical_support = result["historical_support"]

    assert historical_support["status"] == "available"
    assert historical_support["known_outcome_count"] == 5
    assert historical_support["average_confidence"] == 0.9
    assert historical_support["dominant_outcome"] == "degraded"

    degradation_scenario = next(
        scenario
        for scenario in result["scenarios"]
        if scenario["type"] == "potential_machine_degradation"
    )

    evidence = degradation_scenario["evidence"]

    assert evidence["historical_evidence_available"] is True
    assert evidence["historical_outcome_count"] == 5
    assert evidence["historical_average_confidence"] == 0.9
    assert evidence["historical_support"]["dominant_outcome"] == "degraded"

    prediction.stop()
