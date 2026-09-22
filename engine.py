"""
AIHelixia Intelligence Engine
Core Engine
Version: 0.5.1
"""

from __future__ import annotations

from core.action import Action
from core.decision import Decision
from core.engine_core import EngineCore
from core.evaluation import Evaluation
from core.factory_input import FactoryInput
from core.feedback import Feedback
from core.memory import Memory
from core.perception import Perception
from core.prediction import Prediction
from core.reasoning import Reasoning
from core.world_state import WorldState
from providers.model_provider import ModelProvider


ENGINE_NAME = "AIHelixia Intelligence Engine"
ENGINE_VERSION = "0.5.1"


class AIHelixiaEngine:
    """
    Zentrale AIHelixia Engine.

    V0.5.0:
    - Engine Core
    - Model Provider
    - Perception
    - Industrial World State
    - Memory
    - Memory Retrieval
    - Industrial Reasoning
    - Industrial Prediction
    - Decision
    - Action
    - Evaluation
    - Feedback
    - vollständiger Closed Loop

    FactoryIQ Input V0.1.0:
    - strukturierte industrielle Eingaben
    - deterministische Überführung in den World State
    """

    def __init__(self) -> None:

        self.name = ENGINE_NAME
        self.version = ENGINE_VERSION

        self.core = EngineCore()

        self.model_provider = ModelProvider()
        self.perception = Perception()
        self.factory_input = FactoryInput()
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
            "factory_input",
            self.factory_input,
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

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> dict[str, object]:
        """Startet die AIHelixia Engine."""

        self.core.start()

        self.model_provider.load()

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
        self.factory_input.stop()
        self.perception.stop()
        self.core.stop()

        self.status = "stopped"

        return self.get_status()

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict[str, object]:

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "core": self.core.get_status(),
            "model": self.model_provider.model_name,
            "device": self.model_provider.device,
            "model_status": self.model_provider.status,
            "perception": self.perception.get_status(),
            "factory_input": self.factory_input.get_status(),
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

        return {
            "engine": self.name,
            "version": self.version,
            "status": "healthy",
            "core_status": self.core.status,
            "components": self.core.get_status(),
        }

    # ------------------------------------------------------------------
    # FactoryIQ / Industrial Input
    # ------------------------------------------------------------------

    def configure_factory(
        self,
        factory: dict[str, object],
    ) -> dict[str, object]:
        """Konfiguriert die Factory im World State."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.set_factory(factory)

    def add_production_line(
        self,
        production_line: dict[str, object],
    ) -> dict[str, object]:
        """Fügt eine Produktionslinie hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.add_production_line(
            production_line
        )

    def add_machine(
        self,
        machine: dict[str, object],
    ) -> dict[str, object]:
        """Fügt eine Maschine hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.add_machine(machine)

    def add_sensor(
        self,
        sensor: dict[str, object],
    ) -> dict[str, object]:
        """Fügt einen Sensor hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.add_sensor(sensor)

    def set_production(
        self,
        production: dict[str, object],
    ) -> dict[str, object]:
        """Setzt den Produktionszustand."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.set_production(production)

    def set_energy(
        self,
        energy: dict[str, object],
    ) -> dict[str, object]:
        """Setzt den Energiezustand."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.set_energy(energy)

    def set_maintenance(
        self,
        maintenance: dict[str, object],
    ) -> dict[str, object]:
        """Setzt den Wartungszustand."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.set_maintenance(
            maintenance
        )

    def add_alarm(
        self,
        alarm: dict[str, object],
    ) -> dict[str, object]:
        """Fügt einen Alarm hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.world_state.add_alarm(alarm)

    def ingest_factory_data(
        self,
        factory_data: dict[str, object],
    ) -> dict[str, object]:
        """
        Überführt strukturierte FactoryIQ-Daten
        in den World State.
        """

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        return self.factory_input.ingest(
            factory_data=factory_data,
            world_state=self.world_state,
        )

    # ------------------------------------------------------------------
    # Closed Loop
    # ------------------------------------------------------------------

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
        Memory
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

        # 2. Generic observation

        observation = self.world_state.add_observation(
            perception
        )

        world_state = self.world_state.get_state()

        # 3. Memory: aktuelle Observation

        observation_memory = self.memory.store(
            memory_type="observation",
            data=observation,
        )

        # 4. Memory Retrieval

        memory_entries = self.memory.retrieve()

        # 5. Reasoning

        reasoning = self.reasoning.analyze(
            world_state=world_state,
            memory=memory_entries,
        )

        # 6. Prediction

        prediction = self.prediction.predict(
            world_state=world_state,
            reasoning=reasoning,
        )

        # 7. Decision

        decision = self.decision.decide(
            reasoning=reasoning,
            prediction=prediction,
        )

        # 8. Memory: Decision

        decision_memory = self.memory.store(
            memory_type="decision",
            data=decision,
        )

        # 9. Action

        action = self.action.execute(
            decision
        )

        # 10. Evaluation

        evaluation = self.evaluation.evaluate(
            action_result=action,
        )

        # 11. Memory: Evaluation

        evaluation_memory = self.memory.store(
            memory_type="evaluation",
            data=evaluation,
        )

        # 12. Feedback

        feedback = self.feedback.process(
            evaluation
        )

        # 13. Memory: Feedback

        feedback_memory = self.memory.store(
            memory_type="feedback",
            data=feedback,
        )

        return {
            "engine": self.name,
            "version": self.version,
            "status": "processed",
            "perception": perception,
            "world_state": world_state,
            "memory": {
                "observation": observation_memory,
                "retrieved": memory_entries,
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


if __name__ == "__main__":

    engine = AIHelixiaEngine()

    print("=" * 70)
    print("AIHELIXIA INTELLIGENCE ENGINE")
    print("=" * 70)

    engine.start()

    engine.configure_factory(
        {
            "id": "F-001",
            "name": "FactoryIQ Demo Factory",
            "location": "Schwedt",
        }
    )

    engine.add_production_line(
        {
            "id": "L-01",
            "name": "Production Line 01",
            "status": "running",
        }
    )

    engine.add_machine(
        {
            "id": "M-204",
            "name": "Production Machine 204",
            "status": "running",
            "temperature": 87.4,
            "vibration": 6.8,
        }
    )

    engine.add_sensor(
        {
            "id": "S-01",
            "machine_id": "M-204",
            "type": "temperature_vibration",
            "status": "active",
        }
    )

    engine.set_production(
        {
            "output": 1250,
            "unit": "units",
            "status": "running",
        }
    )

    engine.set_energy(
        {
            "power_kw": 114,
            "status": "normal",
        }
    )

    engine.set_maintenance(
        {
            "next_maintenance": "2026-10-15",
            "status": "scheduled",
        }
    )

    engine.add_alarm(
        {
            "type": "warning",
            "source": "temperature",
            "machine_id": "M-204",
            "value": 87.4,
        }
    )

    print("\nINITIAL STATUS")
    print(engine.get_status())

    print("\nPROCESSING CYCLE 1")
    result_1 = engine.process(
        {
            "source": "FactoryIQ",
            "event": "industrial_state_update",
        }
    )

    print(result_1)

    print("\nPROCESSING CYCLE 2")
    result_2 = engine.process(
        {
            "source": "FactoryIQ",
            "event": "industrial_state_update",
        }
    )

    print(result_2)

    print("\nHEALTH")
    print(engine.health())

    print("\n" + "=" * 70)
    print("AIHELIXIA V0.5.1 INDUSTRIAL CLOSED LOOP")
    print("=" * 70)
