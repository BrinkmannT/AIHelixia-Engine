import pytest

from engine import AIHelixiaEngine


def test_engine_economic_finding_flows_into_action_and_evaluation(tmp_path):
    database_path = tmp_path / "economic_action_outcome.db"

    engine = AIHelixiaEngine(database_path=str(database_path))
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
                        "benchmark_source": "validated_market_benchmark",
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
        autonomy = result["autonomy"]
        action = result["action"]
        evaluation = result["evaluation"]

        assert result["status"] == "completed"

        assert economic["finding_count"] == 1
        assert economic["critical_count"] == 1
        assert economic["total_economic_impact"] == 200000.0
        assert economic["total_savings_potential"] == 150000.0

        assert decision["decision_type"] == "economic_priority"
        assert decision["action"] == "review_strategy"
        assert decision["economic"]["finding_count"] == 1
        assert decision["economic"]["total_economic_impact"] == 200000.0

        # Autonomy Gate: strategy changes require human approval.
        assert autonomy["status"] == "autonomy_evaluated"
        assert autonomy["autonomy"] == "approval_required"
        assert autonomy["execution_allowed"] is False
        assert autonomy["approval_required"] is True

        # Action is intentionally not executed while approval is pending.
        assert action["status"] == "approval_required"
        assert action["action"] == "review_strategy"
        assert action["execution_id"] is None
        assert action["result"]["success"] is False
        assert action["result"]["type"] == "approval_required"

        assert evaluation["status"] == "evaluated"
        assert evaluation["action_status"] == "approval_required"

    finally:
        engine.stop()


def test_engine_economic_action_can_be_evaluated_against_observed_outcome(
    tmp_path,
):
    database_path = tmp_path / "economic_outcome_learning.db"

    engine = AIHelixiaEngine(database_path=str(database_path))
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
                        "benchmark_source": "validated_market_benchmark",
                        "period": "2026",
                        "supplier_count": 4,
                        "comparable_volume": True,
                        "verified": True,
                        "realization_factor": 0.75,
                    }
                }
            }
        )

        # Simulate an explicitly approved safe internal action.
        action_result = engine.action.execute(
            {
                "decision_type": "economic_priority",
                "action": "observe",
            }
        )

        outcome_result = engine.evaluate_outcome(
            previous_state={
                "actual_cost": 12.0,
            },
            observed_state={
                "actual_cost": 10.63,
            },
            action_result=action_result,
            economic_context=result["economic_discovery"],
        )

        assert outcome_result["outcome"]["outcome"] == "improved"
        assert outcome_result["outcome"]["success"] is True
        assert outcome_result["outcome"]["confidence"] > 0

        evaluation = outcome_result["evaluation"]
        feedback = outcome_result["feedback"]
        learning_memory = outcome_result["learning_memory"]

        assert evaluation["status"] == "evaluated"
        assert evaluation["evaluation"] == "successful"
        assert evaluation["execution_evaluation"] == "successful"
        assert evaluation["outcome_evaluation"] == "successful"
        assert evaluation["outcome_status"] == "improved"
        assert evaluation["outcome_known"] is True

        assert feedback["status"] == "processed"
        assert feedback["feedback_type"] == "positive"
        assert feedback["signal"] == "reinforce"

        assert learning_memory["type"] == "outcome_learning"
        assert learning_memory["outcome"] == "improved"
        assert learning_memory["outcome_success"] is True
        assert learning_memory["evaluation"] == "successful"
        assert learning_memory["feedback_type"] == "positive"
        assert learning_memory["learning_signal"] == "reinforce"

        economic_outcome = outcome_result["economic_outcome"]

        assert economic_outcome["status"] == "calculated"
        assert economic_outcome["calculation_status"] == "realized"
        assert economic_outcome["economic_type"] == "procurement_cost"

        assert economic_outcome["realized_savings"] == 137000.0

        assert economic_outcome["realization_rate"] == pytest.approx(
            137000.0 / 150000.0
        )

        assert economic_outcome["remaining_gap"] == 63000.0

        assert economic_outcome["implementation_cost"] is None
        assert economic_outcome["roi"] is None

        assert learning_memory["economic_outcome"] == economic_outcome

    finally:
        engine.stop()
