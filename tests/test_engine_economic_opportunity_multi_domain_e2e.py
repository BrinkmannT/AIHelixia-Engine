from engine import AIHelixiaEngine


def test_engine_economic_opportunity_multi_domain_end_to_end(tmp_path):
    database_path = tmp_path / "economic_opportunity_multi_domain.db"

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
                    },
                    "energy": {
                        "annual_kwh": 1000000,
                        "actual_cost_per_kwh": 0.18,
                        "benchmark_cost_per_kwh": 0.14,
                        "benchmark_source": (
                            "validated_energy_benchmark"
                        ),
                        "period": "2026",
                        "verified": True,
                        "realization_factor": 0.75,
                    },
                    "maintenance": {
                        "annual_maintenance_cost": 500000,
                        "benchmark_maintenance_cost": 400000,
                        "benchmark_source": (
                            "validated_maintenance_benchmark"
                        ),
                        "period": "2026",
                        "verified": True,
                        "realization_factor": 0.75,
                    },
                    "inventory": {
                        "average_inventory_value": 2000000,
                        "target_inventory_value": 1500000,
                        "carrying_cost_rate": 0.20,
                        "benchmark_source": (
                            "validated_inventory_model"
                        ),
                        "period": "2026",
                        "verified": True,
                        "realization_factor": 0.75,
                    },
                }
            }
        )

        # ---------------------------------------------------------
        # Engine
        # ---------------------------------------------------------

        assert result["status"] == "completed"

        # ---------------------------------------------------------
        # Economic Discovery
        # ---------------------------------------------------------

        economic = result["economic_discovery"]

        assert economic["status"] == "analysis_completed"
        assert economic["finding_count"] == 4
        assert economic["critical_count"] >= 1

        assert economic["total_economic_impact"] == 440000.0

        assert economic["total_savings_potential"] == 330000.0

        finding_types = {
            finding["type"]
            for finding in economic["findings"]
        }

        assert finding_types == {
            "procurement_cost",
            "energy_cost",
            "maintenance_cost",
            "inventory_carrying_cost",
        }

        # ---------------------------------------------------------
        # Value Prioritization
        # ---------------------------------------------------------

        prioritization = result["value_prioritization"]

        assert prioritization["status"] == (
            "prioritization_completed"
        )
        assert prioritization["finding_count"] == 4
        assert len(prioritization["findings"]) == 4

        prioritized_types = {
            finding["type"]
            for finding in prioritization["findings"]
        }

        assert prioritized_types == {
            "procurement_cost",
            "energy_cost",
            "maintenance_cost",
            "inventory_carrying_cost",
        }

        # ---------------------------------------------------------
        # Economic Opportunity
        # ---------------------------------------------------------

        opportunity_result = result["economic_opportunity"]

        assert opportunity_result["status"] == (
            "opportunity_analysis_completed"
        )
        assert opportunity_result["version"] == "0.1.0"
        assert opportunity_result["opportunity_count"] == 4
        assert opportunity_result["critical_count"] >= 1

        assert opportunity_result["total_economic_impact"] == 440000.0

        assert opportunity_result["total_savings_potential"] == 330000.0

        opportunities = opportunity_result["opportunities"]

        assert len(opportunities) == 4

        opportunity_types = {
            opportunity["type"]
            for opportunity in opportunities
        }

        assert opportunity_types == {
            "procurement_cost",
            "energy_cost",
            "maintenance_cost",
            "inventory_carrying_cost",
        }

        # Ranks müssen eindeutig und vollständig sein.
        assert [
            opportunity["rank"]
            for opportunity in opportunities
        ] == [1, 2, 3, 4]

        for opportunity in opportunities:
            assert opportunity["status"] == "identified"
            assert opportunity["priority_score"] is not None
            assert opportunity["economic_impact"] is not None
            assert opportunity["savings_potential"] is not None
            assert (
                opportunity["expected_savings"]
                == opportunity["savings_potential"]
            )
            assert opportunity["recommended_action"] == (
                "review_strategy"
            )

        # ---------------------------------------------------------
        # Decision
        # ---------------------------------------------------------

        decision = result["decision"]

        assert decision["decision_type"] == "economic_priority"
        assert decision["action"] == "review_strategy"

        assert decision["value_prioritization"][
            "priority"
        ] in {
            "critical",
            "high",
            "medium",
            "low",
        }

        # ---------------------------------------------------------
        # Autonomy
        # ---------------------------------------------------------

        autonomy = result["autonomy"]

        assert autonomy["status"] == "autonomy_evaluated"
        assert autonomy["autonomy"] == "approval_required"
        assert autonomy["execution_allowed"] is False
        assert autonomy["approval_required"] is True

        # ---------------------------------------------------------
        # Action
        # ---------------------------------------------------------

        action = result["action"]

        # review_strategy darf ohne menschliche Freigabe
        # nicht ausgeführt werden.
        assert action["status"] == "approval_required"
        assert action["execution_id"] is None
        assert action["result"]["success"] is False
        assert action["result"]["type"] == "approval_required"
        assert action["decision_type"] == "economic_priority"
        assert action["action"] == "review_strategy"

        # ---------------------------------------------------------
        # Persistence
        # ---------------------------------------------------------

        history = engine.persistence.get_history(
            "ai_results",
            limit=100,
        )

        economic_opportunity_entries = [
            entry
            for entry in history
            if entry.get("result_type")
            == "economic_opportunity"
        ]

        assert economic_opportunity_entries

        persisted_opportunity = economic_opportunity_entries[-1]

        assert (
            persisted_opportunity.get("result_type")
            == "economic_opportunity"
        )

        assert (
            persisted_opportunity.get("data", {}).get(
                "opportunity_count"
            )
            == 4
        )

        # ---------------------------------------------------------
        # Closed Loop
        # ---------------------------------------------------------

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

        closed_loop_opportunity = closed_loop["data"][
            "economic_opportunity"
        ]

        assert (
            closed_loop_opportunity["opportunity_count"]
            == 4
        )

    finally:
        engine.stop()
