from core.action import Action
from core.evaluation import Evaluation
from core.feedback import Feedback


def test_successful_action_with_improved_outcome_creates_reinforce_signal():
    action = Action()
    evaluation = Evaluation()
    feedback = Feedback()

    action.start()
    evaluation.start()
    feedback.start()

    decision = {
        "decision_type": "monitor",
        "action": "continue_monitoring",
    }

    action_result = action.execute(decision)

    assert action_result["status"] == "executed"
    assert action_result["action"] == "continue_monitoring"
    assert action_result["result"]["success"] is True

    outcome_result = {
        "outcome": "improved",
        "success": True,
        "confidence": 0.9,
    }

    evaluation_result = evaluation.evaluate(
        action_result=action_result,
        outcome_result=outcome_result,
    )

    assert evaluation_result["status"] == "evaluated"
    assert evaluation_result["evaluation"] == "successful"
    assert evaluation_result["execution_evaluation"] == "successful"
    assert evaluation_result["outcome_evaluation"] == "successful"
    assert evaluation_result["outcome_known"] is True
    assert evaluation_result["outcome_confidence"] == 0.9

    feedback_result = feedback.process(evaluation_result)

    assert feedback_result["status"] == "processed"
    assert feedback_result["feedback_type"] == "positive"
    assert feedback_result["signal"] == "reinforce"
    assert feedback_result["outcome_status"] == "improved"
    assert feedback_result["outcome_confidence"] == 0.9

    feedback.stop()
    evaluation.stop()
    action.stop()


def test_unsuccessful_outcome_creates_adjust_signal():
    action = Action()
    evaluation = Evaluation()
    feedback = Feedback()

    action.start()
    evaluation.start()
    feedback.start()

    decision = {
        "decision_type": "monitor",
        "action": "continue_monitoring",
    }

    action_result = action.execute(decision)

    outcome_result = {
        "outcome": "degraded",
        "success": False,
        "confidence": 0.85,
    }

    evaluation_result = evaluation.evaluate(
        action_result=action_result,
        outcome_result=outcome_result,
    )

    assert evaluation_result["evaluation"] == "unsuccessful"
    assert evaluation_result["outcome_evaluation"] == "unsuccessful"

    feedback_result = feedback.process(evaluation_result)

    assert feedback_result["feedback_type"] == "negative"
    assert feedback_result["signal"] == "adjust"
    assert feedback_result["outcome_status"] == "degraded"

    feedback.stop()
    evaluation.stop()
    action.stop()


def test_unchanged_outcome_creates_review_signal():
    action = Action()
    evaluation = Evaluation()
    feedback = Feedback()

    action.start()
    evaluation.start()
    feedback.start()

    decision = {
        "decision_type": "review",
        "action": "observe",
    }

    action_result = action.execute(decision)

    outcome_result = {
        "outcome": "unchanged",
        "success": False,
        "confidence": 0.8,
    }

    evaluation_result = evaluation.evaluate(
        action_result=action_result,
        outcome_result=outcome_result,
    )

    assert evaluation_result["evaluation"] == "unchanged"
    assert evaluation_result["outcome_evaluation"] == "unchanged"

    feedback_result = feedback.process(evaluation_result)

    assert feedback_result["feedback_type"] == "neutral"
    assert feedback_result["signal"] == "review"
    assert feedback_result["outcome_status"] == "unchanged"

    feedback.stop()
    evaluation.stop()
    action.stop()


def test_unknown_outcome_creates_pending_review_signal():
    action = Action()
    evaluation = Evaluation()
    feedback = Feedback()

    action.start()
    evaluation.start()
    feedback.start()

    decision = {
        "decision_type": "monitor",
        "action": "continue_monitoring",
    }

    action_result = action.execute(decision)

    evaluation_result = evaluation.evaluate(
        action_result=action_result,
    )

    assert evaluation_result["evaluation"] == "execution_success_outcome_unknown"
    assert evaluation_result["outcome_known"] is False

    feedback_result = feedback.process(evaluation_result)

    assert feedback_result["feedback_type"] == "pending"
    assert feedback_result["signal"] == "review"
    assert feedback_result["outcome_status"] == "unknown"

    feedback.stop()
    evaluation.stop()
    action.stop()
