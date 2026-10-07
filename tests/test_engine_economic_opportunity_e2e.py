from engine import AIHelixiaEngine


def test_engine_economic_opportunity_end_to_end(tmp_path):
    database_path = tmp_path / "economic_opportunity_e2e.db"

    engine = AIHelixiaEngine(
        database_path=str(database_path),
    )

    # Kein echtes Modell für diesen deterministischen Test notwendig.
    engine.model_provider.status = "loaded"

    engine.start()

    try:
        result = engine.process(
            {
                "economic_discovery": {
                    "procurement": {
                        "annual_volume": 100000,
                        "actual_cost": 12.0,
                        "benchmark_cost": 10.0,
                        "benchmark_source": (
                            "validated_market_benchmark"
                        ),
                        "period": "2026",
                        "supplier_count": 4,
                        "comparable_volume": True,
                        "verified": True,
                        "realization_factor": 0.75,
                    }
                }
            }
        )

        assert result["status"] == "completed"

        # ---------------------------------------------------------
        # Economic Discovery
        # ---------------------------------------------------------

        economic = result["economic_discovery"]

        assert economic["status"] == "analysis_completed"
        assert economic["finding_count"] == 1
        assert economic["critical_count"] == 1
        assert economic["total_economic_impact"] == 200000.0
        assert economic["total_savings_potential"] == 150000.0

        finding = economic["findings"][0]

        assert finding["type"] == "procurement_cost"
        assert finding["economic_impact"] == 200000.0
        assert finding["savings_potential"] == 150000.0
        assert finding["priority"] == "critical"

        # ---------------------------------------------------------
        # Value Prioritization
        # ---------------------------------------------------------

        prioritization = result["value_prioritization"]

        assert prioritization["status"] == (
            "prioritization_completed"
        )
        assert prioritization["finding_count"] == 1
        assert prioritization["critical_count"] == 1

        prioritized = prioritization["findings"][0]

        assert prioritized["type"] == "procurement_cost"
        assert prioritized["value_priority"] == "critical"
        assert prioritized["priority_score"] == 100.0

        # ---------------------------------------------------------
        # Economic Opportunity
        # ---------------------------------------------------------

        opportunity_result = result["economic_opportunity"]

        assert opportunity_result["status"] == (
            "opportunity_analysis_completed"
        )
        assert opportunity_result["version"] == "0.1.0"
        assert opportunity_result["opportunity_count"] == 1
        assert opportunity_result["critical_count"] == 1
        assert opportunity_result["high_count"] == 0

        assert opportunity_result["total_economic_impact"] == (
            200000.0
        )
        assert opportunity_result["total_savings_potential"] == (
            150000.0
        )

        opportunity = opportunity_result["opportunities"][0]

        assert opportunity["rank"] == 1
        assert opportunity["type"] == "procurement_cost"
        assert opportunity["priority"] == "critical"
        assert opportunity["priority_score"] == 100.0

        # Opportunity darf wirtschaftliche Werte
        # nicht neu berechnen oder verändern.
        assert opportunity["economic_impact"] == 200000.0
        assert opportunity["savings_potential"] == 150000.0
        assert opportunity["expected_savings"] == 150000.0

        assert opportunity["recommended_action"] == (
            "review_strategy"
        )
        assert opportunity["status"] == "identified"

        # ---------------------------------------------------------
        # Decision
        # ---------------------------------------------------------

        decision = result["decision"]

        # Bestehende Decision-Semantik bleibt erhalten.
        assert decision["decision_type"] == "economic_priority"
        assert decision["action"] == "review_strategy"

        assert decision["value_prioritization"]["priority"] == (
            "critical"
        )
        assert decision["value_prioritization"][
            "priority_score"
        ] == 100.0

        # ---------------------------------------------------------
        # Action
        # ---------------------------------------------------------

        action = result["action"]

        assert action["status"] == "executed"
        assert action["decision_type"] == "economic_priority"
        assert action["action"] == "review_strategy"

        # ---------------------------------------------------------
        # Persistence / Closed Loop
        # ---------------------------------------------------------

        history = engine.persistence.get_history(
            "ai_results",
            limit=100,
        )

        assert any(
            entry.get("result_type") == "economic_opportunity"
            for entry in history
        )

        events = engine.persistence.get_history(
            "engine_events",
            limit=100,
        )

        closed_loop_events = [
            entry
            for entry in events
            if entry.get("event_type")
            == "closed_loop_completed"
        ]

        assert closed_loop_events

        closed_loop = closed_loop_events[-1]

        assert "economic_opportunity" in closed_loop["data"]

    finally:
        engine.stop()
