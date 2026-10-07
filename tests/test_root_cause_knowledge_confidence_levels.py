from core.root_cause import RootCause


def _run_root_cause(knowledge):
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
        "scenarios": [],
    }

    result = root_cause.analyze(
        reasoning=reasoning,
        prediction=prediction,
        knowledge=knowledge,
    )

    return result["primary_hypothesis"]["confidence"]


def test_moderate_knowledge_raises_low_to_medium():
    knowledge = {
        "status": "knowledge_available",
        "support_count": 2,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 1.0,
        "evidence_strength": "moderate",
        "matched_case_count": 2,
    }

    assert _run_root_cause(knowledge) == "medium"


def test_strong_knowledge_raises_low_to_medium():
    knowledge = {
        "status": "knowledge_available",
        "support_count": 5,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 1.0,
        "evidence_strength": "strong",
        "matched_case_count": 5,
    }

    assert _run_root_cause(knowledge) == "medium"
