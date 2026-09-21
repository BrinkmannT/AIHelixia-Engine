"""
AIHelixia Intelligence Engine
Reasoning Layer
Version: 0.4.1
"""

from __future__ import annotations

from typing import Any


class Reasoning:
    """
    Deterministische Reasoning-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - World State analysieren
    - Memory berücksichtigen
    - Beobachtungen auswerten
    - Zustandsmerkmale ableiten
    - strukturierte Schlussfolgerungen erzeugen

    V0.4.1:
    - deterministisch
    - reproduzierbar
    - Memory Retrieval
    - keine LLM-Abhängigkeit
    """

    def __init__(self) -> None:
        self.status = "created"

    def start(self) -> None:
        """Startet die Reasoning-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Reasoning-Schicht."""

        self.status = "stopped"

    def analyze(
        self,
        world_state: dict[str, Any],
        memory: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Analysiert den aktuellen World State
        und berücksichtigt vorhandene Memory-Einträge.
        """

        if self.status != "running":
            raise RuntimeError(
                "Reasoning ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(world_state, dict):
            raise TypeError(
                "World State muss ein Dictionary sein."
            )

        if memory is not None and not isinstance(memory, list):
            raise TypeError(
                "Memory muss eine Liste sein."
            )

        if memory is None:
            memory = []

        observations = world_state.get(
            "observations",
            [],
        )

        entities = world_state.get(
            "entities",
            [],
        )

        conditions = world_state.get(
            "conditions",
            [],
        )

        observation_count = len(observations)
        entity_count = len(entities)
        condition_count = len(conditions)
        memory_count = len(memory)

        if observation_count == 0:
            state_assessment = "no_observations"
        else:
            state_assessment = "observations_available"

        memory_assessment = self._assess_memory(
            memory
        )

        conclusions = self._build_conclusions(
            observation_count=observation_count,
            entity_count=entity_count,
            condition_count=condition_count,
            memory_count=memory_count,
            memory_assessment=memory_assessment,
        )

        return {
            "status": "analyzed",
            "state_assessment": state_assessment,
            "observation_count": observation_count,
            "entity_count": entity_count,
            "condition_count": condition_count,
            "memory_count": memory_count,
            "memory_assessment": memory_assessment,
            "conclusions": conclusions,
        }

    def _assess_memory(
        self,
        memory: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Bewertet vorhandene Memory-Einträge.

        Die Methode interpretiert die Inhalte noch nicht
        fachlich. Sie bestimmt zunächst nur deren Struktur.
        """

        memory_types: dict[str, int] = {}

        for entry in memory:
            if not isinstance(entry, dict):
                continue

            memory_type = entry.get(
                "type",
                "unknown",
            )

            memory_types[memory_type] = (
                memory_types.get(memory_type, 0) + 1
            )

        if not memory:
            status = "no_memory"
        else:
            status = "memory_available"

        return {
            "status": status,
            "entry_count": len(memory),
            "types": memory_types,
        }

    def _build_conclusions(
        self,
        observation_count: int,
        entity_count: int,
        condition_count: int,
        memory_count: int,
        memory_assessment: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Erzeugt deterministische Schlussfolgerungen."""

        conclusions: list[dict[str, Any]] = []

        if observation_count > 0:
            conclusions.append(
                {
                    "type": "observation_present",
                    "value": True,
                    "description": (
                        "Mindestens eine Beobachtung "
                        "liegt im World State vor."
                    ),
                }
            )

        if entity_count > 0:
            conclusions.append(
                {
                    "type": "entities_present",
                    "value": True,
                    "description": (
                        "Mindestens eine Entität "
                        "liegt im World State vor."
                    ),
                }
            )

        if condition_count > 0:
            conclusions.append(
                {
                    "type": "conditions_present",
                    "value": True,
                    "description": (
                        "Mindestens eine Bedingung "
                        "liegt im World State vor."
                    ),
                }
            )

        if memory_count > 0:
            conclusions.append(
                {
                    "type": "memory_available",
                    "value": True,
                    "description": (
                        "Frühere Verarbeitungsergebnisse "
                        "stehen für das Reasoning zur Verfügung."
                    ),
                }
            )

        if (
            memory_assessment.get("types", {}).get(
                "feedback",
                0,
            )
            > 0
        ):
            conclusions.append(
                {
                    "type": "historical_feedback_available",
                    "value": True,
                    "description": (
                        "Früheres Feedback steht "
                        "für die aktuelle Verarbeitung zur Verfügung."
                    ),
                }
            )

        if not conclusions:
            conclusions.append(
                {
                    "type": "empty_state",
                    "value": True,
                    "description": (
                        "Der World State enthält "
                        "noch keine relevanten Daten."
                    ),
                }
            )

        return conclusions

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "reasoning",
            "status": self.status,
        }