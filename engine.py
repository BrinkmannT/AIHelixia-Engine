"""
AIHelixia Intelligence Engine
Core Engine
Version: 0.5.2
"""

from __future__ import annotations

from typing import Any

from core.action import Action
from core.decision import Decision
from core.evaluation import Evaluation
from core.factory_input import FactoryInput
from core.feedback import Feedback
from core.memory import Memory
from core.perception import Perception
from core.persistence import Persistence
from core.prediction import Prediction
from core.reasoning import Reasoning
from core.root_cause import RootCause
from core.world_state import WorldState
from core.outcome import Outcome
from providers.model_provider import ModelProvider


class AIHelixiaEngine:
    """
    Zentrale Orchestrierung der AIHelixia Intelligence Engine.

    Pipeline:

    Input
        ↓
    Perception
        ↓
    World State
        ↓
    Persistence
        ↓
    Memory Retrieval
        ↓
    Reasoning
        ↓
    Prediction
        ↓
    Decision
        ↓
    Action
        ↓
    Evaluation
        ↓
    Feedback
        ↓
    Persistence
        ↺
    """

    VERSION = "0.5.2"

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        model_device: str = "auto",
        database_path: str = "data/factoryiq.db",
    ) -> None:
        self.name = "AIHelixia Intelligence Engine"
        self.status = "created"

        self.model_provider = ModelProvider(
            model_name=model_name,
            device=model_device,
        )

        self.perception = Perception()
        self.factory_input = FactoryInput()
        self.world_state = WorldState()
        self.persistence = Persistence(
            database_path=database_path,
        )
        self.memory = Memory()
        self.reasoning = Reasoning()
        self.prediction = Prediction()
        self.root_cause = RootCause()
        self.decision = Decision()
        self.action = Action()
        self.evaluation = Evaluation()
        self.feedback = Feedback()
        self.outcome = Outcome()

        self.components = [
            "model_provider",
            "perception",
            "factory_input",
            "world_state",
            "persistence",
            "memory",
            "reasoning",
            "prediction",
            "root_cause",
            "decision",
            "action",
            "evaluation",
            "feedback",
        ]

    def start(self) -> None:
        if self.status == "running":
            return

        self.persistence.start()

        self.perception.start()
        self.factory_input.start()
        self.world_state.start()

        restore_result = self._restore_latest_factory_state()

        self.memory.start()
        self.reasoning.start()
        self.prediction.start()
        self.root_cause.start()
        self.decision.start()
        self.action.start()
        self.evaluation.start()
        self.feedback.start()
        self.outcome.start()

        if self.model_provider.status != "loaded":
            self.model_provider.load()

        self.status = "running"

        self.persistence.save_engine_event(
            "engine_started",
            {
                "engine_version": self.VERSION,
                "components": self.components,
                "factory_restore": restore_result,
            },
        )

    def _restore_latest_factory_state(self) -> dict[str, object]:
        """
        Restore the latest persisted FactoryIQ state into WorldState.
        """

        history = self.persistence.get_history(
            "factory_states",
            limit=1,
        )

        if not history:
            return {
                "status": "no_persisted_factory_state",
                "restored": False,
            }

        latest = history[0]

        if not isinstance(latest, dict):
            return {
                "status": "invalid_persisted_factory_state",
                "restored": False,
            }

        persisted_data = latest.get("data", {})

        if not isinstance(persisted_data, dict):
            return {
                "status": "invalid_persisted_factory_data",
                "restored": False,
            }

        factory_data = {
            field: persisted_data[field]
            for field in (
                "factory",
                "production_lines",
                "machines",
                "sensors",
                "production",
                "energy",
                "maintenance",
                "alarms",
            )
            if field in persisted_data
        }

        if not factory_data:
            return {
                "status": "empty_persisted_factory_data",
                "restored": False,
            }

        restore_result = self.factory_input.ingest(
            factory_data=factory_data,
            world_state=self.world_state,
        )

        return {
            "status": "restored",
            "restored": True,
            "source_id": latest.get("id"),
            "factory_id": (
                persisted_data.get("factory", {}).get("id")
                if isinstance(
                    persisted_data.get("factory"),
                    dict,
                )
                else None
            ),
            "processed": restore_result.get(
                "processed",
                {},
            ),
        }

    def stop(self) -> None:
        if self.status == "stopped":
            return

        if self.persistence.status == "running":
            self.persistence.save_engine_event(
                "engine_stopped",
                {
                    "engine_version": self.VERSION,
                },
            )

        self.feedback.stop()
        self.outcome.stop()
        self.evaluation.stop()
        self.action.stop()
        self.decision.stop()
        self.root_cause.stop()
        self.prediction.stop()
        self.reasoning.stop()
        self.memory.stop()
        self.world_state.stop()
        self.factory_input.stop()
        self.perception.stop()
        self.persistence.stop()

        self.status = "stopped"

    def ingest_factory_data(
        self,
        factory_data: dict[str, object],
    ) -> dict[str, object]:
        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        result = self.factory_input.ingest(
            factory_data=factory_data,
            world_state=self.world_state,
        )

        factory_state = self.world_state.get_state()

        self.persistence.save_factory_state(
            factory_state,
        )

        for alarm in factory_state.get(
            "alarms",
            [],
        ):
            if isinstance(alarm, dict):
                self.persistence.save_alarm(
                    alarm,
                )

        self.persistence.save_engine_event(
            "factory_data_ingested",
            {
                "factory_input": result,
                "world_state": self.world_state.get_status(),
            },
        )

        return result

    def process(
        self,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        # 1. Factory Input Detection
        is_factory_input = (
            isinstance(input_data, dict)
            and "factory" in input_data
            and "machines" in input_data
            and "sensors" in input_data
            and "alarms" in input_data
        )

        factory_ingest_result = None

        if is_factory_input:
            factory_ingest_result = self.ingest_factory_data(
                input_data
            )

        # 2. Perception
        perception_result = self.perception.perceive(
            input_data,
        )

        # 3. World State
        if is_factory_input:
            world_state = self.world_state.get_state()
        else:
            observation = perception_result.get(
                "observation",
                input_data,
            )

            if isinstance(observation, dict):
                self.world_state.add_observation(
                    observation,
                )

            world_state = self.world_state.get_state()

        # 4. Persistence
        self.persistence.save_factory_state(
            world_state,
        )

        self.persistence.save_engine_event(
            "observation_received",
            {
                "input": input_data,
                "perception": perception_result,
                "factory_ingest": factory_ingest_result,
            },
        )

        # 5. Memory
        if is_factory_input:
            memory_type = "factory_state"
            memory_data = world_state
        else:
            memory_type = "observation"
            memory_data = perception_result.get(
                "observation",
                input_data,
            )

        self.memory.store(
            memory_type,
            memory_data,
        )

        memory_result = self.memory.retrieve()

        # 6. Reasoning
        reasoning_result = self.reasoning.analyze(
            world_state,
            memory_result,
        )

        # 7. Prediction
        prediction_result = self.prediction.predict(
            world_state,
            reasoning_result,
        )

        # 8. Root Cause Analysis
        root_cause_result = self.root_cause.analyze(
            reasoning=reasoning_result,
            prediction=prediction_result,
        )

        # 9. Decision
        decision_result = self.decision.decide(
            reasoning_result,
            prediction_result,
            root_cause_result,
        )

        # 10. Memory
        self.memory.store(
            "decision",
            decision_result,
        )

        # 11. Action
        action_result = self.action.execute(
            decision_result,
        )

        # 12. Evaluation
        evaluation_result = self.evaluation.evaluate(
            action_result=action_result,
        )

        # 13. Feedback
        feedback_result = self.feedback.process(
            evaluation_result,
        )

        # 14. Memory
        self.memory.store(
            "evaluation",
            evaluation_result,
        )

        self.memory.store(
            "feedback",
            feedback_result,
        )

        # 15. Persistence
        self.persistence.save_ai_result(
            "reasoning",
            reasoning_result,
        )

        self.persistence.save_ai_result(
            "prediction",
            prediction_result,
        )

        self.persistence.save_ai_result(
            "root_cause",
            root_cause_result,
        )

        self.persistence.save_ai_result(
            "decision",
            decision_result,
        )

        self.persistence.save_ai_result(
            "action",
            action_result,
        )

        self.persistence.save_ai_result(
            "evaluation",
            evaluation_result,
        )

        self.persistence.save_ai_result(
            "feedback",
            feedback_result,
        )

        self.persistence.save_engine_event(
            "closed_loop_completed",
            {
                "reasoning": reasoning_result,
                "prediction": prediction_result,
                "root_cause": root_cause_result,
                "decision": decision_result,
                "action": action_result,
                "evaluation": evaluation_result,
                "feedback": feedback_result,
            },
        )

        return {
            "status": "completed",
            "factory_ingest": factory_ingest_result,
            "perception": perception_result,
            "world_state": world_state,
            "memory": memory_result,
            "reasoning": reasoning_result,
            "prediction": prediction_result,
            "root_cause": root_cause_result,
            "decision": decision_result,
            "action": action_result,
            "evaluation": evaluation_result,
            "feedback": feedback_result,
        }

    def evaluate_outcome(
        self,
        previous_state: dict,
        observed_state: dict,
        action_result: dict,
    ) -> dict:
        """
        Verarbeitet einen beobachteten Outcome nach einer Action.

        Pipeline:

        previous_state
            ↓
        observed_state
            ↓
        Outcome
            ↓
        Evaluation
            ↓
        Feedback
        """

        outcome_result = self.outcome.evaluate(
            previous_state=previous_state,
            observed_state=observed_state,
        )

        evaluation_result = self.evaluation.evaluate(
            action_result=action_result,
            outcome_result=outcome_result,
        )

        feedback_result = self.feedback.process(
            evaluation_result,
        )

        # ---------------------------------------------------------
        # Outcome Learning Memory
        # ---------------------------------------------------------
        learning_memory = {
            "type": "outcome_learning",
            "outcome": outcome_result.get("outcome"),
            "outcome_success": outcome_result.get("success"),
            "outcome_confidence": outcome_result.get("confidence"),
            "evaluation": evaluation_result.get("evaluation"),
            "evaluation_score": evaluation_result.get("score"),
            "feedback_type": feedback_result.get("feedback_type"),
            "learning_signal": feedback_result.get("signal"),
            "recommendation": feedback_result.get("recommendation"),
        }

        self.memory.store(
            "outcome_learning",
            learning_memory,
        )

        return {
            "outcome": outcome_result,
            "evaluation": evaluation_result,
            "feedback": feedback_result,
            "learning_memory": learning_memory,
        }

    def get_status(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.VERSION,
            "status": self.status,
            "components": self.components,
        }
