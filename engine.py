"""
AIHelixia Intelligence Engine
Core Engine
Version: 0.4.0
"""

from __future__ import annotations

from core.action import Action
from core.decision import Decision
from core.engine_core import EngineCore
from core.evaluation import Evaluation
from core.feedback import Feedback
from core.memory import Memory
from core.perception import Perception
from core.prediction import Prediction
from core.reasoning import Reasoning
from core.world_state import WorldState
from providers.model_provider import ModelProvider


ENGINE_NAME = "AIHelixia Intelligence Engine"
ENGINE_VERSION = "0.4.0"


class AIHelixiaEngine:
    """
    Zentrale AIHelixia Engine.

    V0.4.0:
    - Engine Core
    - Model Provider
    - Perception
    - World State
    - Memory
    - Reasoning
    - Prediction
    - Decision
    - Action
    - Evaluation
    - Feedback
    - vollständiger Closed Loop
    """

    def __init__(self) -> None:

        self.name = ENGINE_NAME
        self.version = ENGINE_VERSION

        self.core = EngineCore()

        self.model_provider = ModelProvider()
        self.perception = Perception()
        self.world_state = WorldState()
        self.memory = Memory()
        self.reasoning = Reasoning()
        self.prediction = Prediction()
        self.decision = Decision()
        self.action = Action()
        self.evaluation = Evaluation()
        self.feedback = Feedback()

        self.core.register_component(
            "model_provider",
            self.model_provider,
        )

        self.core.register_component(
            "perception",
            self.perception,
        )

        self.core.register_component(
            "world_state",
            self.world_state,
        )

        self.core.register_component(
            "memory",
            self.memory,
        )

        self.core.register_component(
            "reasoning",
            self.reasoning,
        )

        self.core.register_component(
            "prediction",
            self.prediction,
        )

        self.core.register_component(
            "decision",
            self.decision,
        )

        self.core.register_component(
            "action",
            self.action,
        )

        self.core.register_component(
            "evaluation",
            self.evaluation,
        )

        self.core.register_component(
            "feedback",
            self.feedback,
        )

        self.status = "created"

    def start(self) -> dict[str, object]:
        """Startet die AIHelixia Engine."""

        self.core.start()
        self.perception.start()
        self.world_state.start()
        self.memory.start()
        self.reasoning.start()
        self.prediction.start()
        self.decision.start()
        self.action.start()
        self.evaluation.start()
        self.feedback.start()

        self.status = "running"

        return self.get_status()

    def stop(self) -> dict[str, object]:
        """Stoppt die AIHelixia Engine."""

        self.feedback.stop()
        self.evaluation.stop()
        self.action.stop()
        self.decision.stop()
        self.prediction.stop()
        self.reasoning.stop()
        self.memory.stop()
        self.world_state.stop()
        self.perception.stop()
        self.core.stop()

        self.status = "stopped"

        return self.get_status()

    def get_status(self) -> dict[str, object]:
        """Gibt den aktuellen Engine-Status zurück."""

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "core": self.core.get_status(),
            "model": self.model_provider.model_name,
            "device": self.model_provider.device,
            "model_status": self.model_provider.status,
            "perception": self.perception.get_status(),
            "world_state": self.world_state.get_status(),
            "memory": self.memory.get_status(),
            "reasoning": self.reasoning.get_status(),
            "prediction": self.prediction.get_status(),
            "decision": self.decision.get_status(),
            "action": self.action.get_status(),
            "evaluation": self.evaluation.get_status(),
            "feedback": self.feedback.get_status(),
        }

    def health(self) -> dict[str, object]:
        """Führt einen Health Check durch."""

        return {
            "engine": self.name,
            "version": self.version,
            "status": "healthy",
            "core_status": self.core.status,
            "model_provider": self.model_provider.status,
            "perception": self.perception.status,
            "world_state": self.world_state.status,
            "memory": self.memory.status,
            "reasoning": self.reasoning.status,
            "prediction": self.prediction.status,
            "decision": self.decision.status,
            "action": self.action.status,
            "evaluation": self.evaluation.status,
            "feedback": self.feedback.status,
        }

    def process(
        self,
        input_data: object,
    ) -> dict[str, object]:
        """
        Führt den vollständigen AIHelixia Closed Loop aus.

        Input
          ↓
        Perception
          ↓
        World State
          ↓
        Memory
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
        """

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        # 1. Perception
        perception = self.perception.perceive(
            input_data
        )

        # 2. World State
        observation = self.world_state.add_observation(
            perception
        )

        world_state = self.world_state.get_state()

        # 3. Memory: Observation speichern
        observation_memory = self.memory.store(
            memory_type="observation",
            data=observation,
        )

        # 4. Reasoning
        reasoning = self.reasoning.analyze(
            world_state
        )

        # 5. Prediction
        prediction = self.prediction.predict(
            world_state=world_state,
            reasoning=reasoning,
        )

        # 6. Decision
        decision = self.decision.decide(
            reasoning=reasoning,
            prediction=prediction,
        )

        # 7. Memory: Decision speichern
        decision_memory = self.memory.store(
            memory_type="decision",
            data=decision,
        )

        # 8. Action
        action = self.action.execute(
            decision
        )

        # 9. Evaluation
        evaluation = self.evaluation.evaluate(
            action
        )

        # 10. Memory: Evaluation speichern
        evaluation_memory = self.memory.store(
            memory_type="evaluation",
            data=evaluation,
        )

        # 11. Feedback
        feedback = self.feedback.process(
            evaluation
        )

        # 12. Memory: Feedback speichern
        feedback_memory = self.memory.store(
            memory_type="feedback",
            data=feedback,
        )

        return {
            "input": input_data,
            "perception": perception,
            "observation": observation,
            "world_state": world_state,
            "memory": {
                "observation": observation_memory,
                "decision": decision_memory,
                "evaluation": evaluation_memory,
                "feedback": feedback_memory,
            },
            "reasoning": reasoning,
            "prediction": prediction,
            "decision": decision,
            "action": action,
            "evaluation": evaluation,
            "feedback": feedback,
        }

    def ask(
        self,
        prompt: str,
        max_new_tokens: int = 64,
    ) -> str:
        """
        Verarbeitet eine Anfrage über den Model Provider.

        Das Modell wird nur verwendet,
        wenn es geladen wurde.
        """

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        return self.model_provider.generate(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
        )


if __name__ == "__main__":

    engine = AIHelixiaEngine()

    print("=" * 60)
    print("AIHELIXIA INTELLIGENCE ENGINE")
    print("=" * 60)

    print()
    print("Initial status:")
    print(engine.get_status())

    print()
    print("Starting engine...")

    engine.start()

    print(engine.get_status())

    print()
    print("Running complete AIHelixia pipeline...")

    result = engine.process(
        "FactoryIQ erkennt eine Anomalie."
    )

    print()
    print("PIPELINE RESULT")
    print("-" * 60)

    print("Input:")
    print(result["input"])

    print()
    print("Perception:")
    print(result["perception"])

    print()
    print("Reasoning:")
    print(result["reasoning"])

    print()
    print("Prediction:")
    print(result["prediction"])

    print()
    print("Decision:")
    print(result["decision"])

    print()
    print("Action:")
    print(result["action"])

    print()
    print("Evaluation:")
    print(result["evaluation"])

    print()
    print("Feedback:")
    print(result["feedback"])

    print()
    print("Memory:")
    print(result["memory"])

    print()
    print("Memory status:")
    print(engine.memory.get_status())

    print()
    print("Health check:")
    print(engine.health())

    print()
    print("AIHELIXIA V0.4.0 MEMORY INTEGRATED")

    print("=" * 60)