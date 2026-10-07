from core.decision import Decision


def test_decision_waits_without_observations():
    decision = Decision()
    decision.start()

    reasoning = {
        "state_assessment": "no_observations",
        "learning_signal": {
            "action": "review",
            "priority": "normal",
        },
    }

    prediction = {
        "scenarios": [],
    }

    result = decision.decide(
        reasoning=reasoning,
        prediction=prediction,
    )

    assert result["status"] == "decided"
    assert result["decision_type"] == "wait"
    assert result["action"] == "observe"
    assert result["scenario_count"] == 0

    decision.stop()


def test_decision_monitors_available_scenario():
    decision = Decision()
    decision.start()

    reasoning = {
        "state_assessment": "observed",
        "learning_signal": {
            "action": "reinforce",
            "priority": "normal",
        },
    }

    prediction = {
        "scenarios": [
            {
                "type": "potential_machine_degradation",
                "evidence": {
                    "evidence_count": 3,
                    "evidence_strength": "strong",
                },
            }
        ],
    }

    result = decision.decide(
        reasoning=reasoning,
        prediction=prediction,
    )

    assert result["status"] == "decided"
    assert result["decision_type"] == "reinforce"
    assert result["action"] == "continue_monitoring"
    assert result["scenario_count"] == 1

    decision.stop()


def test_decision_adjusts_when_learning_signal_requires_adjustment():
    decision = Decision()
    decision.start()

    reasoning = {
        "state_assessment": "observed",
        "learning_signal": {
            "action": "adjust",
            "priority": "high",
        },
    }

    prediction = {
        "scenarios": [
            {
                "type": "potential_machine_degradation",
            }
        ],
    }

    result = decision.decide(
        reasoning=reasoning,
        prediction=prediction,
    )

    assert result["status"] == "decided"
    assert result["decision_type"] == "adjust"
    assert result["action"] == "review_strategy"
    assert result["learning_signal"]["type"] == "adjust"
    assert result["learning_signal"]["priority"] == "high"

    decision.stop()


def test_decision_uses_critical_root_cause():
    decision = Decision()
    decision.start()

    reasoning = {
        "state_assessment": "observed",
        "learning_signal": {
            "action": "review",
            "priority": "normal",
        },
    }

    prediction = {
        "scenarios": [
            {
                "type": "potential_machine_degradation",
            }
        ],
    }

    root_cause = {
        "status": "analysis_completed",
        "hypothesis_count": 2,
        "primary_hypothesis": {
            "type": "critical_alarm_condition",
            "priority": "critical",
            "confidence": "high",
            "evidence": {
                "evidence_count": 4,
                "evidence_strength": "strong",
                "supporting_signals": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "correlated_machines": [
                    "M-001",
                ],
                "supporting_predictions": [
                    "potential_machine_degradation",
                ],
            },
        },
    }

    result = decision.decide(
        reasoning=reasoning,
        prediction=prediction,
        root_cause=root_cause,
    )

    assert result["status"] == "decided"
    assert result["decision_type"] == "root_cause_review"
    assert result["action"] == "review_strategy"
    assert result["root_cause"]["primary_type"] == "critical_alarm_condition"
    assert result["root_cause"]["priority"] == "critical"
    assert result["root_cause"]["confidence"] == "high"

    decision.stop()


def test_decision_preserves_historical_support_evidence():
    decision = Decision()
    decision.start()

    reasoning = {
        "state_assessment": "observed",
        "learning_signal": {
            "action": "review",
            "priority": "normal",
        },
    }

    prediction = {
        "scenarios": [
            {
                "type": "potential_machine_degradation",
            }
        ],
    }

    root_cause = {
        "status": "analysis_completed",
        "hypothesis_count": 1,
        "primary_hypothesis": {
            "type": "thermal_mechanical_stress",
            "priority": "high",
            "confidence": "medium",
            "evidence": {
                "evidence_count": 4,
                "evidence_strength": "strong",
                "supporting_signals": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "correlated_machines": [
                    "M-001",
                ],
                "supporting_predictions": [
                    "potential_machine_degradation",
                ],
            },
            "historical_support": {
                "status": "available",
                "strength": "moderate",
                "known_outcome_count": 5,
                "average_confidence": 0.9,
                "dominant_outcome": "degraded",
            },
        },
    }

    result = decision.decide(
        reasoning=reasoning,
        prediction=prediction,
        root_cause=root_cause,
    )

    assert result["status"] == "decided"

    historical_support = result["evidence"]["historical_support"]

    assert historical_support["status"] == "available"
    assert historical_support["strength"] == "moderate"
    assert historical_support["known_outcome_count"] == 5
    assert historical_support["average_confidence"] == 0.9
    assert historical_support["dominant_outcome"] == "degraded"

    decision.stop()
