from core.root_cause import RootCause


def _run_root_cause_with_knowledge(knowledge):
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

    return root_cause.analyze(
        reasoning=reasoning,
        prediction=prediction,
        knowledge=knowledge,
    )


def test_moderate_knowledge_adds_moderate_confidence_factor():
    knowledge = {
        "status": "knowledge_available",
        "support_count": 5,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 1.0,
        "evidence_strength": "moderate",
        "matched_case_count": 5,
    }

    result = _run_root_cause_with_knowledge(knowledge)

    factors = result["primary_hypothesis"]["confidence_factors"]

    assert "knowledge_support_moderate" in factors
    assert "knowledge_support_strong" not in factors


def test_strong_knowledge_adds_strong_confidence_factor():
    knowledge = {
        "status": "knowledge_available",
        "support_count": 5,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 1.0,
        "evidence_strength": "strong",
        "matched_case_count": 5,
    }

    result = _run_root_cause_with_knowledge(knowledge)

    factors = result["primary_hypothesis"]["confidence_factors"]

    assert "knowledge_support_strong" in factors
    assert "knowledge_support_moderate" not in factors


def test_limited_knowledge_does_not_add_confidence_factor():
    knowledge = {
        "status": "knowledge_available",
        "support_count": 1,
        "dominant_outcome": "degraded",
        "dominant_outcome_ratio": 1.0,
        "evidence_strength": "limited",
        "matched_case_count": 1,
    }

    result = _run_root_cause_with_knowledge(knowledge)

    factors = result["primary_hypothesis"]["confidence_factors"]

    assert "knowledge_support_moderate" not in factors
    assert "knowledge_support_strong" not in factors


def test_no_knowledge_does_not_add_confidence_factor():
    result = _run_root_cause_with_knowledge(None)

    factors = result["primary_hypothesis"]["confidence_factors"]

    assert "knowledge_support_moderate" not in factors
    assert "knowledge_support_strong" not in factors
