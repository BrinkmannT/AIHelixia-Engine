from core.value_prioritization import ValuePrioritization


def test_value_prioritization_ranks_highest_value_first():
    prioritization = ValuePrioritization()
    prioritization.start()

    result = prioritization.prioritize(
        {
            "status": "analysis_completed",
            "findings": [
                {
                    "type": "energy_cost",
                    "category": "cost_optimization",
                    "problem": "Energy costs above benchmark",
                    "economic_impact": 60000.0,
                    "savings_potential": 60000.0,
                    "confidence": 0.90,
                    "priority": "high",
                },
                {
                    "type": "procurement_cost",
                    "category": "cost_optimization",
                    "problem": "Procurement above benchmark",
                    "economic_impact": 200000.0,
                    "savings_potential": 150000.0,
                    "confidence": 0.94,
                    "priority": "critical",
                },
            ],
        }
    )

    assert result["status"] == "prioritization_completed"
    assert result["version"] == "0.1.0"
    assert result["finding_count"] == 2

    assert result["findings"][0]["type"] == "procurement_cost"
    assert result["findings"][0]["rank"] == 1
    assert result["findings"][0]["priority_score"] == 98.5
    assert result["findings"][0]["value_priority"] == "critical"

    assert result["findings"][1]["rank"] == 2


def test_value_prioritization_handles_missing_economic_values():
    prioritization = ValuePrioritization()
    prioritization.start()

    result = prioritization.prioritize(
        {
            "findings": [
                {
                    "type": "unknown",
                    "priority": "unknown",
                    "confidence": 0.0,
                }
            ]
        }
    )

    assert result["finding_count"] == 1
    assert result["findings"][0]["priority_score"] == 0.0
    assert result["findings"][0]["value_priority"] == "low"


def test_value_prioritization_requires_start():
    prioritization = ValuePrioritization()

    try:
        prioritization.prioritize({"findings": []})
    except RuntimeError as exc:
        assert "nicht gestartet" in str(exc)
    else:
        raise AssertionError(
            "Expected RuntimeError"
        )
