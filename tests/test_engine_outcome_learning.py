from engine import AIHelixiaEngine


def test_engine_evaluate_outcome_creates_learning_memory():
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

    result = engine.evaluate_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        action_result=action_result,
    )

    assert "outcome" in result
    assert "evaluation" in result
    assert "feedback" in result
    assert "learning_memory" in result

    outcome = result["outcome"]
    evaluation = result["evaluation"]
    feedback = result["feedback"]
    learning_memory = result["learning_memory"]

    assert outcome["outcome"] == "improved"
    assert outcome["success"] is True
    assert outcome["confidence"] == 1.0
    assert outcome["summary"]["improved"] == 4
    assert outcome["summary"]["degraded"] == 0
    assert outcome["summary"]["unchanged"] == 0
    assert outcome["summary"]["total"] == 4

    assert evaluation["status"] == "evaluated"
    assert evaluation["evaluation"] == "successful"
    assert evaluation["execution_evaluation"] == "successful"
    assert evaluation["outcome_evaluation"] == "successful"
    assert evaluation["outcome_status"] == "improved"
    assert evaluation["outcome_known"] is True
    assert evaluation["outcome_confidence"] == 1.0

    assert feedback["status"] == "processed"
    assert feedback["feedback_type"] == "positive"
    assert feedback["signal"] == "reinforce"
    assert feedback["outcome_status"] == "improved"
    assert feedback["outcome_confidence"] == 1.0

    assert learning_memory["type"] == "outcome_learning"
    assert learning_memory["outcome"] == "improved"
    assert learning_memory["outcome_success"] is True
    assert learning_memory["outcome_confidence"] == 1.0
    assert learning_memory["evaluation"] == "successful"
    assert learning_memory["feedback_type"] == "positive"
    assert learning_memory["learning_signal"] == "reinforce"

    engine.stop()
