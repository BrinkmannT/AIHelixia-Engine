from core.economic_opportunity import EconomicOpportunity


def _economic_discovery():
    return {
        "status": "analysis_completed",
        "version": "0.3.0",
        "finding_count": 2,
        "critical_count": 1,
        "total_economic_impact": 300000.0,
        "total_savings_potential": 220000.0,
        "findings": [
            {
                "status": "finding_detected",
                "type": "procurement_cost",
                "category": "cost_optimization",
                "problem": "Procurement costs exceed benchmark.",
                "priority": "critical",
                "economic_impact": 200000.0,
                "savings_potential": 150000.0,
                "confidence": 0.94,
                "evidence": {
                    "verified": True,
                },
            },
            {
                "status": "finding_detected",
                "type": "energy_cost",
                "category": "cost_optimization",
                "problem": "Energy costs exceed benchmark.",
                "priority": "high",
                "economic_impact": 100000.0,
                "savings_potential": 70000.0,
                "confidence": 0.90,
                "evidence": {
                    "verified": True,
                },
            },
        ],
    }


def _value_prioritization():
    return {
        "status": "prioritization_completed",
        "version": "0.1.0",
        "finding_count": 2,
        "critical_count": 1,
        "high_count": 1,
        "top_finding": {
            "type": "procurement_cost",
            "priority_score": 98.5,
            "value_priority": "critical",
            "reason": (
                "Savings Potential: 150,000.00 EUR | "
                "Economic Impact: 200,000.00 EUR"
            ),
        },
        "findings": [
            {
                "type": "procurement_cost",
                "priority_score": 98.5,
                "value_priority": "critical",
                "reason": (
                    "Savings Potential: 150,000.00 EUR | "
                    "Economic Impact: 200,000.00 EUR"
                ),
            },
            {
                "type": "energy_cost",
                "priority_score": 82.5,
                "value_priority": "high",
                "reason": (
                    "Savings Potential: 70,000.00 EUR | "
                    "Economic Impact: 100,000.00 EUR"
                ),
            },
        ],
    }


def test_requires_start():
    opportunity = EconomicOpportunity()

    try:
        opportunity.build(
            _economic_discovery(),
            _value_prioritization(),
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "EconomicOpportunity must require start()."
        )


def test_builds_opportunities_from_existing_findings():
    opportunity = EconomicOpportunity()
    opportunity.start()

    result = opportunity.build(
        _economic_discovery(),
        _value_prioritization(),
    )

    assert result["status"] == (
        "opportunity_analysis_completed"
    )
    assert result["version"] == "0.1.0"
    assert result["opportunity_count"] == 2
    assert result["critical_count"] == 1
    assert result["high_count"] == 1

    assert result["total_economic_impact"] == 300000.0
    assert result["total_savings_potential"] == 220000.0

    top = result["top_opportunity"]

    assert top is not None
    assert top["type"] == "procurement_cost"
    assert top["priority"] == "critical"
    assert top["priority_score"] == 98.5
    assert top["savings_potential"] == 150000.0
    assert top["expected_savings"] == 150000.0
    assert top["recommended_action"] == "review_strategy"
    assert top["status"] == "identified"


def test_preserves_existing_economic_values():
    opportunity = EconomicOpportunity()
    opportunity.start()

    result = opportunity.build(
        _economic_discovery(),
        _value_prioritization(),
    )

    findings = result["opportunities"]

    procurement = next(
        item
        for item in findings
        if item["type"] == "procurement_cost"
    )

    energy = next(
        item
        for item in findings
        if item["type"] == "energy_cost"
    )

    assert procurement["economic_impact"] == 200000.0
    assert procurement["savings_potential"] == 150000.0

    assert energy["economic_impact"] == 100000.0
    assert energy["savings_potential"] == 70000.0


def test_handles_missing_prioritization_for_finding():
    opportunity = EconomicOpportunity()
    opportunity.start()

    prioritization = _value_prioritization()

    prioritization["findings"] = [
        prioritization["findings"][0]
    ]

    result = opportunity.build(
        _economic_discovery(),
        prioritization,
    )

    energy = next(
        item
        for item in result["opportunities"]
        if item["type"] == "energy_cost"
    )

    assert energy["priority"] == "high"
    assert energy["priority_score"] is None
    assert energy["recommended_action"] == "review_strategy"


def test_invalid_input_types():
    opportunity = EconomicOpportunity()
    opportunity.start()

    try:
        opportunity.build(
            [],
            _value_prioritization(),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Economic Discovery must require a dictionary."
        )

    try:
        opportunity.build(
            _economic_discovery(),
            [],
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Value Prioritization must require a dictionary."
        )
