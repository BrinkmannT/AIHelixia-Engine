from engine import AIHelixiaEngine


def test_engine_reuses_previous_outcome_in_next_cycle():
    engine = AIHelixiaEngine()
    engine.start()

    # ---------------------------------------------------------
    # 1. Erster Durchlauf
    # ---------------------------------------------------------

    first_input = {
        "machine_id": "M-001",
        "temperature": 85,
        "vibration": 7.5,
        "energy_consumption": 120,
        "production_output": 80,
    }

    first_result = engine.process(first_input)

    assert first_result["status"] == "completed"
    assert first_result["action"]["status"] == "executed"
    assert first_result["evaluation"]["status"] == "evaluated"
    assert first_result["feedback"]["status"] == "processed"

    # ---------------------------------------------------------
    # 2. Tatsächlichen Outcome erzeugen
    # ---------------------------------------------------------

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

    outcome_result = engine.evaluate_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        action_result=first_result["action"],
    )

    assert outcome_result["outcome"]["outcome"] == "improved"
    assert outcome_result["outcome"]["success"] is True
    assert outcome_result["feedback"]["signal"] == "reinforce"
    assert outcome_result["learning_memory"]["type"] == "outcome_learning"

    # ---------------------------------------------------------
    # 3. Zweiter Engine-Durchlauf
    # ---------------------------------------------------------

    second_input = {
        "machine_id": "M-001",
        "temperature": 78,
        "vibration": 5.5,
        "energy_consumption": 108,
        "production_output": 88,
    }

    second_result = engine.process(second_input)

    assert second_result["status"] == "completed"

    # ---------------------------------------------------------
    # 4. Historical Learning muss wieder auftauchen
    # ---------------------------------------------------------

    historical = second_result["reasoning"][
        "historical_outcome_analysis"
    ]

    assert historical["known_outcome_count"] >= 1
    assert historical["improved_count"] >= 1
    assert historical["dominant_outcome"] == "improved"

    # ---------------------------------------------------------
    # 5. Prediction muss Historical Support übernehmen
    # ---------------------------------------------------------

    prediction_support = second_result["prediction"][
        "historical_support"
    ]

    assert prediction_support["status"] == "available"
    assert prediction_support["known_outcome_count"] >= 1
    assert prediction_support["dominant_outcome"] == "improved"

    # ---------------------------------------------------------
    # 6. Decision muss den historischen Kontext erhalten
    # ---------------------------------------------------------

    decision_evidence = second_result["decision"]["evidence"]

    assert "historical_support" in decision_evidence

    historical_decision_support = decision_evidence[
        "historical_support"
    ]

    assert historical_decision_support["status"] in {
        "available",
        "positive_history",
        "limited",
    }

    engine.stop()
