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
from core.world_state import WorldState
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
        self.decision = Decision()
        self.action = Action()
        self.evaluation = Evaluation()
        self.feedback = Feedback()

        self.components = [
            "model_provider",
            "perception",
            "factory_input",
            "world_state",
            "persistence",
            "memory",
            "reasoning",
            "prediction",
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
        self.memory.start()
        self.reasoning.start()
        self.prediction.start()
        self.decision.start()
        self.action.start()
        self.evaluation.start()
        self.feedback.start()

        if self.model_provider.status != "loaded":
            self.model_provider.load()

        self.status = "running"

        self.persistence.save_engine_event(
            "engine_started",
            {
                "engine_version": self.VERSION,
                "components": self.components,
            },
        )

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
        self.evaluation.stop()
        self.action.stop()
        self.decision.stop()
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

        # 1. Perception
        perception_result = self.perception.perceive(
            input_data,
        )

        # 2. World State
        observation = perception_result.get(
            "observation",
            input_data,
        )

        if isinstance(observation, dict):
            self.world_state.add_observation(
                observation,
            )

        world_state = self.world_state.get_state()

        # 3. Persistence
        self.persistence.save_factory_state(
            world_state,
        )

        self.persistence.save_engine_event(
            "observation_received",
            {
                "input": input_data,
                "perception": perception_result,
            },
        )

        # 4. Memory
        if isinstance(observation, dict):
            self.memory.store(
                "observation",
                observation,
            )

        memory_result = self.memory.retrieve()

        # 5. Reasoning
        reasoning_result = self.reasoning.analyze(
            self.world_state.get_state(),
            memory_result,
        )

        # 6. Prediction
        prediction_result = self.prediction.predict(
            self.world_state.get_state(),
            reasoning_result,
        )

        # 7. Decision
        decision_result = self.decision.decide(
            reasoning_result,
            prediction_result,
        )

        # 8. Memory
        self.memory.store(
            "decision",
            decision_result,
        )

        # 9. Action
        action_result = self.action.execute(
            decision_result,
        )

        # 10. Evaluation
        evaluation_result = self.evaluation.evaluate(
            action_result=action_result,
        )

        # 11. Feedback
        feedback_result = self.feedback.process(
            evaluation_result,
        )

        # 12. Memory
        self.memory.store(
            "evaluation",
            evaluation_result,
        )

        self.memory.store(
            "feedback",
            feedback_result,
        )

        # 13. Persistence
        self.persistence.save_ai_result(
            "reasoning",
            reasoning_result,
        )

        self.persistence.save_ai_result(
            "prediction",
            prediction_result,
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
                "decision": decision_result,
                "action": action_result,
                "evaluation": evaluation_result,
                "feedback": feedback_result,
            },
        )

        return {
            "status": "completed",
            "perception": perception_result,
            "world_state": self.world_state.get_state(),
            "memory": memory_result,
            "reasoning": reasoning_result,
            "prediction": prediction_result,
            "decision": decision_result,
            "action": action_result,
            "evaluation": evaluation_result,
            "feedback": feedback_result,
        }

    def get_status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.VERSION,
            "status": self.status,
            "core": {
                "status": self.status,
                "components": self.components,
                "component_count": len(self.components),
            },
            "model": self.model_provider.model_name,
            "device": self.model_provider.device,
            "model_status": self.model_provider.status,
            "factory_input": self.factory_input.get_status(),
            "world_state": self.world_state.get_status(),
            "persistence": self.persistence.get_status(),
            "memory": self.memory.get_status(),
            "reasoning": self.reasoning.get_status(),
            "prediction": self.prediction.get_status(),
            "decision": self.decision.get_status(),
            "action": self.action.get_status(),
            "evaluation": self.evaluation.get_status(),
            "feedback": self.feedback.get_status(),
        }
