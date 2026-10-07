from engine import AIHelixiaEngine


def test_engine_closed_loop_returns_all_layers():
    engine = AIHelixiaEngine()
    engine.start()

    input_data = {
        "machine_id": "M-001",
        "temperature": 85,
        "vibration": 7.5,
        "energy_consumption": 120,
        "production_output": 80,
    }

    result = engine.process(input_data)

    assert result["status"] == "completed"

    assert "perception" in result
    assert "world_state" in result
    assert "memory" in result
    assert "knowledge" in result
    assert "knowledge_query" in result
    assert "reasoning" in result
    assert "prediction" in result
    assert "root_cause" in result
    assert "decision" in result
    assert "action" in result
    assert "evaluation" in result
    assert "feedback" in result

    assert result["decision"]["status"] == "decided"
    assert result["action"]["status"] == "executed"
    assert result["evaluation"]["status"] == "evaluated"
    assert result["feedback"]["status"] == "processed"

    engine.stop()
