from core.value_prioritization import ValuePrioritization


def test_value_prioritization_selects_highest_economic_value():
    prioritization = ValuePrioritization()
    prioritization.start()

    economic_discovery = {
        "status": "analysis_completed",
        "version": "0.3.0",
        "finding_count": 3,
        "findings": [
            {
                "type": "energy_cost",
                "category": "cost_optimization",
                "problem": "Energy costs above benchmark",
                "economic_impact": 600000.0,
                "savings_potential": 450000.0,
                "confidence": 0.91,
                "priority": "critical",
            },
            {
                "type": "procurement_cost",
                "category": "cost_optimization",
                "problem": "Procurement costs above benchmark",
                "economic_impact": 2000000.0,
                "savings_potential": 1500000.0,
                "confidence": 0.94,
                "priority": "critical",
            },
            {
                "type": "inventory_value",
                "category": "working_capital",
                "problem": "Inventory above target",
                "economic_impact": 160000.0,
                "savings_potential": 80000.0,
                "confidence": 0.82,
                "priority": "high",
            },
        ],
    }

    result = prioritization.prioritize(
        economic_discovery
    )

    assert result["status"] == "prioritization_completed"
    assert result["finding_count"] == 3

    top = result["top_finding"]

    assert top is not None
    assert top["type"] == "procurement_cost"
    assert top["rank"] == 1
    assert top["savings_potential"] == 1500000.0
    assert top["value_priority"] == "critical"

    assert result["findings"][1]["rank"] == 2
    assert result["findings"][2]["rank"] == 3


def test_value_prioritization_produces_actionable_reason():
    prioritization = ValuePrioritization()
    prioritization.start()

    result = prioritization.prioritize(
        {
            "findings": [
                {
                    "type": "maintenance_cost",
                    "economic_impact": 200000.0,
                    "savings_potential": 120000.0,
                    "confidence": 0.90,
                    "priority": "critical",
                }
            ]
        }
    )

    finding = result["top_finding"]

    assert finding is not None
    assert finding["reason"]
    assert "Savings Potential" in finding["reason"]
    assert "120,000.00" in finding["reason"]


def test_value_prioritization_handles_multiple_industries_independently():
    prioritization = ValuePrioritization()
    prioritization.start()

    result = prioritization.prioritize(
        {
            "findings": [
                {
                    "type": "procurement_cost",
                    "economic_impact": 1000000.0,
                    "savings_potential": 700000.0,
                    "confidence": 0.95,
                    "priority": "critical",
                },
                {
                    "type": "energy_cost",
                    "economic_impact": 800000.0,
                    "savings_potential": 600000.0,
                    "confidence": 0.90,
                    "priority": "critical",
                },
                {
                    "type": "maintenance_cost",
                    "economic_impact": 500000.0,
                    "savings_potential": 300000.0,
                    "confidence": 0.88,
                    "priority": "high",
                },
            ]
        }
    )

    assert result["finding_count"] == 3

    types = [
        finding["type"]
        for finding in result["findings"]
    ]

    assert set(types) == {
        "procurement_cost",
        "energy_cost",
        "maintenance_cost",
    }
