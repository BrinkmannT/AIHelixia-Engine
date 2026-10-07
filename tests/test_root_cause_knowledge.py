from core.root_cause import RootCause


def test_root_cause_exposes_knowledge_support():
    root_cause = RootCause()
    root_cause.start()

    reasoning = {
        "anomaly_analysis": {
            "status": "anomaly_detected",
            "severity": "medium",
            "signals": [
                "temperature_elevated",
                "vibration_elevated",
            ],
        }
    }

    prediction = {
        "status": "prediction_available",
    }

    knowledge = {
        "status": "knowledge_available",
        "support_count": 4,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 0.75,
        "evidence_strength": "moderate",
        "matched_case_count": 5,
    }

    result = root_cause.analyze(
        reasoning=reasoning,
        prediction=prediction,
        knowledge=knowledge,
    )

    assert result["status"] == "analysis_completed"
    assert result["knowledge_evidence"] == knowledge

    support = result["primary_hypothesis"]["evidence"]["knowledge_support"]

    assert support["available"] is True
    assert support["support_count"] == 4
    assert support["dominant_outcome"] == "degraded"
    assert support["dominant_outcome_ratio"] == 0.75
    assert support["evidence_strength"] == "moderate"
