from engine import AIHelixiaEngine


def test_engine_processes_economic_discovery_into_decision(
    tmp_path,
):
    database_path = tmp_path / "economic_discovery.db"

    engine = AIHelixiaEngine(
        database_path=str(database_path),
    )

    # Der Integrationstest benötigt kein echtes Modell.
    # Wir ersetzen nur den Provider-Ladevorgang durch
    # einen kontrollierten Testzustand.
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

        economic = result["economic_discovery"]
        decision = result["decision"]

        assert result["status"] == "completed"

        assert economic["status"] == (
            "analysis_completed"
        )
        assert economic["version"] == "0.3.0"
        assert economic["finding_count"] == 1
        assert economic["critical_count"] == 1
        assert economic["total_economic_impact"] == 200000.0
        assert economic["total_savings_potential"] == 150000.0

        finding = economic["findings"][0]

        assert finding["type"] == "procurement_cost"
        assert finding["priority"] == "critical"
        assert finding["economic_impact"] == 200000.0
        assert finding["savings_potential"] == 150000.0
        assert finding["evidence"]["verified"] is True

        assert decision["economic"]["finding_count"] == 1
        assert decision["economic"]["critical_count"] == 1
        assert (
            decision["economic"]["total_economic_impact"]
            == 200000.0
        )

        assert decision["decision_type"] == (
            "economic_priority"
        )
        assert decision["action"] == "review_strategy"

    finally:
        engine.stop()
