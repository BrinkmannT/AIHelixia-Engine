from core.memory import Memory
from core.reasoning import Reasoning


def _outcome_memory(
    outcome: str,
    confidence: float = 1.0,
    learning_signal: str = "review",
    evaluation_score: float = 0.0,
) -> dict:
    return {
        "type": "outcome_learning",
        "data": {
            "outcome": outcome,
            "outcome_success": (
                True if outcome == "improved"
                else False if outcome == "degraded"
                else None
            ),
            "outcome_confidence": confidence,
            "evaluation": (
                "successful"
                if outcome == "improved"
                else "unsuccessful"
                if outcome == "degraded"
                else "unchanged"
            ),
            "evaluation_score": evaluation_score,
            "feedback_type": (
                "positive"
                if outcome == "improved"
                else "negative"
                if outcome == "degraded"
                else "neutral"
            ),
            "learning_signal": learning_signal,
            "recommendation": learning_signal,
        },
    }


def _reasoning() -> Reasoning:
    reasoning = Reasoning()
    reasoning.start()
    return reasoning


def test_three_high_confidence_positive_outcomes_reinforce():
    reasoning = _reasoning()

    memory = [
        _outcome_memory(
            "improved",
            confidence=1.0,
            learning_signal="reinforce",
            evaluation_score=1.0,
        )
        for _ in range(3)
    ]

    result = reasoning.analyze(
        world_state={},
        memory=memory,
    )

    learning_signal = result["learning_signal"]
    historical = result["historical_outcome_analysis"]

    assert historical["known_outcome_count"] == 3
    assert historical["improved_count"] == 3
    assert historical["average_confidence"] == 1.0

    assert learning_signal["action"] == "reinforce"
    assert learning_signal["priority"] == "normal"


def test_three_high_confidence_negative_outcomes_adjust():
    reasoning = _reasoning()

    memory = [
        _outcome_memory(
            "degraded",
            confidence=1.0,
            learning_signal="adjust",
            evaluation_score=0.0,
        )
        for _ in range(3)
    ]

    result = reasoning.analyze(
        world_state={},
        memory=memory,
    )

    learning_signal = result["learning_signal"]
    historical = result["historical_outcome_analysis"]

    assert historical["known_outcome_count"] == 3
    assert historical["degraded_count"] == 3
    assert historical["average_confidence"] == 1.0

    assert learning_signal["action"] == "adjust"
    assert learning_signal["priority"] == "high"


def test_too_few_outcomes_do_not_activate_historical_learning():
    reasoning = _reasoning()

    memory = [
        _outcome_memory(
            "improved",
            confidence=1.0,
            learning_signal="reinforce",
            evaluation_score=1.0,
        )
        for _ in range(2)
    ]

    result = reasoning.analyze(
        world_state={},
        memory=memory,
    )

    learning_signal = result["learning_signal"]
    historical = result["historical_outcome_analysis"]

    assert historical["known_outcome_count"] == 2
    assert learning_signal["action"] == "reinforce"


def test_low_confidence_outcomes_do_not_activate_historical_learning():
    reasoning = _reasoning()

    memory = [
        _outcome_memory(
            "improved",
            confidence=0.5,
            learning_signal="reinforce",
            evaluation_score=1.0,
        )
        for _ in range(3)
    ]

    result = reasoning.analyze(
        world_state={},
        memory=memory,
    )

    learning_signal = result["learning_signal"]
    historical = result["historical_outcome_analysis"]

    assert historical["known_outcome_count"] == 3
    assert historical["average_confidence"] == 0.5

    assert learning_signal["action"] == "reinforce"
    assert learning_signal["priority"] == "normal"
