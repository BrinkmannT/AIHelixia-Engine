from core.root_cause import RootCause


def test_root_cause_identifies_thermal_mechanical_hypothesis():
    root_cause = RootCause()
    root_cause.start()

    reasoning = {
        "anomaly_analysis": {
            "status": "anomaly_detected",
            "severity": "medium",
            "signals": [
                {"type": "temperature_elevated"},
                {"type": "vibration_elevated"},
            ],
        }
    }

    prediction = {
        "status": "prediction_available",
    }

    result = root_cause.analyze(
        reasoning=reasoning,
        prediction=prediction,
    )

    assert result["status"] == "analysis_completed"
    assert result["hypothesis_count"] >= 1
    assert result["primary_hypothesis"]["type"] == "thermal_mechanical_stress"
