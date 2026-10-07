from core.autonomy import Autonomy


def _economic_context(
    *,
    critical_count=0,
    priority="high",
    score=70.0,
    verified=True,
    confidence=0.95,
):
    return {
        "status": "analysis_completed",
        "finding_count": 1,
        "critical_count": critical_count,
        "confidence": confidence,
        "findings": [
            {
                "type": "procurement_cost",
                "priority": priority,
                "economic_impact": 100000.0,
                "savings_potential": 75000.0,
                "evidence": {
                    "verified": verified,
                },
            }
        ],
    }


def test_autonomy_starts_and_stops():
    autonomy = Autonomy()

    assert autonomy.status == "created"

    autonomy.start()

    assert autonomy.status == "running"

    autonomy.stop()

    assert autonomy.status == "stopped"


def test_observe_is_autonomous():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "wait",
            "action": "observe",
        }
    )

    assert result["autonomy"] == "auto"
    assert result["execution_allowed"] is True
    assert result["approval_required"] is False


def test_continue_monitoring_is_autonomous():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "monitor",
            "action": "continue_monitoring",
        }
    )

    assert result["autonomy"] == "auto"
    assert result["execution_allowed"] is True
    assert result["approval_required"] is False


def test_review_strategy_requires_approval():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "economic_priority",
            "action": "review_strategy",
            "economic": _economic_context(
                critical_count=0,
                priority="high",
                score=70.0,
            ),
            "value_prioritization": {
                "priority": "high",
                "priority_score": 70.0,
            },
        }
    )

    assert result["autonomy"] == "approval_required"
    assert result["execution_allowed"] is False
    assert result["approval_required"] is True


def test_critical_economic_finding_requires_approval():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "economic_priority",
            "action": "review_strategy",
            "economic": _economic_context(
                critical_count=1,
                priority="critical",
                score=100.0,
            ),
            "value_prioritization": {
                "priority": "critical",
                "priority_score": 100.0,
            },
        }
    )

    assert result["autonomy"] == "approval_required"
    assert result["execution_allowed"] is False
    assert result["approval_required"] is True
    assert (
        result["reason"]
        == "critical_economic_finding_requires_approval"
    )


def test_unverified_economic_evidence_requires_approval():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "economic_priority",
            "action": "review_strategy",
            "economic": _economic_context(
                critical_count=0,
                priority="high",
                score=70.0,
                verified=False,
            ),
            "value_prioritization": {
                "priority": "high",
                "priority_score": 70.0,
            },
        }
    )

    assert result["autonomy"] == "approval_required"
    assert result["execution_allowed"] is False
    assert result["approval_required"] is True


def test_unknown_action_is_blocked():
    autonomy = Autonomy()
    autonomy.start()

    result = autonomy.evaluate(
        {
            "decision_type": "unknown",
            "action": "send_money",
        }
    )

    assert result["autonomy"] == "blocked"
    assert result["execution_allowed"] is False
    assert result["approval_required"] is False
    assert result["reason"] == "unknown_action"


def test_autonomy_requires_running_state():
    autonomy = Autonomy()

    try:
        autonomy.evaluate(
            {
                "decision_type": "wait",
                "action": "observe",
            }
        )
    except RuntimeError as exc:
        assert "nicht gestartet" in str(exc)
    else:
        raise AssertionError(
            "RuntimeError wurde nicht ausgelöst."
        )
