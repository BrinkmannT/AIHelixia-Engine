from engine import AIHelixiaEngine


def test_outcome_learning_is_reused_by_reasoning():
    engine = AIHelixiaEngine()
    engine.start()

    previous_state = {
        "temperature": 85,
        "vibration": 7.5,
        "production": 80,
        "energy": 120,
    }

    observed_state = {
        "temperature": 75,
        "vibration": 5.0,
        "production": 90,
        "energy": 105,
    }

    action_result = {
        "status": "executed",
        "execution_id": 1,
        "decision_type": "monitor",
        "action": "continue_monitoring",
        "result": {
            "success": True,
            "type": "monitoring",
        },
    }

    outcome_result = engine.evaluate_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        action_result=action_result,
    )

    assert outcome_result["outcome"]["outcome"] == "improved"
    assert outcome_result["feedback"]["signal"] == "reinforce"
    assert outcome_result["learning_memory"]["type"] == "outcome_learning"

    memory_entries = engine.memory.retrieve()

    outcome_entries = [
        entry
        for entry in memory_entries
        if isinstance(entry, dict)
        and entry.get("type") == "outcome_learning"
    ]

    assert len(outcome_entries) >= 1

    reasoning_world_state = {
        "temperature": 75,
        "vibration": 5.0,
        "production": 90,
        "energy": 105,
    }

    reasoning_result = engine.reasoning.analyze(
        reasoning_world_state,
        memory_entries,
    )

    assert "historical_outcome_analysis" in reasoning_result

    historical = reasoning_result["historical_outcome_analysis"]

    assert historical["status"] == "positive_history"
    assert historical["known_outcome_count"] >= 1
    assert historical["improved_count"] >= 1
    assert historical["dominant_outcome"] == "improved"

    engine.stop()
