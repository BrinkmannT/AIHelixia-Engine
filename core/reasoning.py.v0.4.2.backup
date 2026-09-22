"""
AIHelixia Intelligence Engine
Reasoning Layer
Version: 0.4.2
"""

from __future__ import annotations

from typing import Any


class Reasoning:
    """
    Deterministische Reasoning-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - World State analysieren
    - Memory berücksichtigen
    - historisches Feedback auswerten
    - Lernsignale ableiten
    - strukturierte Schlussfolgerungen erzeugen

    V0.4.2:
    - deterministisch
    - reproduzierbar
    - Memory Retrieval
    - Feedback Analysis
    - Learning Signal
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
        und berücksichtigt vorhandenes Memory.
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

        feedback_analysis = self._analyze_feedback(
            memory
        )

        learning_signal = self._build_learning_signal(
            feedback_analysis
        )

        conclusions = self._build_conclusions(
            observation_count=observation_count,
            entity_count=entity_count,
            condition_count=condition_count,
            memory_count=memory_count,
            memory_assessment=memory_assessment,
            feedback_analysis=feedback_analysis,
        )

        return {
            "status": "analyzed",
            "state_assessment": state_assessment,
            "observation_count": observation_count,
            "entity_count": entity_count,
            "condition_count": condition_count,
            "memory_count": memory_count,
            "memory_assessment": memory_assessment,
            "feedback_analysis": feedback_analysis,
            "learning_signal": learning_signal,
            "conclusions": conclusions,
        }

    def _assess_memory(
        self,
        memory: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Bewertet die Struktur des vorhandenen Memorys.
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

    def _analyze_feedback(
        self,
        memory: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Analysiert historische Feedback-Einträge.

        Die Analyse bleibt deterministisch und wertet
        ausschließlich bereits gespeicherte Signale aus.
        """

        feedback_entries = [
            entry
            for entry in memory
            if isinstance(entry, dict)
            and entry.get("type") == "feedback"
        ]

        positive_count = 0
        negative_count = 0
        error_count = 0

        reinforce_count = 0
        adjust_count = 0
        review_count = 0

        scores: list[float] = []

        for entry in feedback_entries:

            data = entry.get(
                "data",
                {},
            )

            if not isinstance(data, dict):
                continue

            feedback_type = data.get(
                "feedback_type"
            )

            signal = data.get(
                "signal"
            )

            score = data.get(
                "score"
            )

            if feedback_type == "positive":
                positive_count += 1

            elif feedback_type == "negative":
                negative_count += 1

            elif feedback_type == "error":
                error_count += 1

            if signal == "reinforce":
                reinforce_count += 1

            elif signal == "adjust":
                adjust_count += 1

            elif signal == "review":
                review_count += 1

            if isinstance(score, (int, float)):
                scores.append(float(score))

        feedback_count = len(feedback_entries)

        if feedback_count == 0:
            assessment = "no_feedback"

        elif negative_count > 0 or error_count > 0:
            assessment = "adjustment_required"

        elif positive_count > 0:
            assessment = "positive_history"

        else:
            assessment = "feedback_available"

        if scores:
            average_score = (
                sum(scores) / len(scores)
            )
        else:
            average_score = None

        return {
            "status": assessment,
            "feedback_count": feedback_count,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "error_count": error_count,
            "reinforce_count": reinforce_count,
            "adjust_count": adjust_count,
            "review_count": review_count,
            "average_score": average_score,
        }

    def _build_learning_signal(
        self,
        feedback_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Erzeugt ein strukturiertes Lernsignal
        aus dem historischen Feedback.
        """

        status = feedback_analysis.get(
            "status",
            "no_feedback",
        )

        if status == "adjustment_required":
            return {
                "type": "adjust",
                "priority": "high",
                "reason": (
                    "Historisches Feedback enthält "
                    "negative oder fehlerhafte Ergebnisse."
                ),
            }

        if status == "positive_history":
            return {
                "type": "reinforce",
                "priority": "normal",
                "reason": (
                    "Historisches Feedback zeigt "
                    "erfolgreiche Verarbeitung."
                ),
            }

        return {
            "type": "review",
            "priority": "normal",
            "reason": (
                "Es liegt noch kein ausreichendes "
                "historisches Feedback vor."
            ),
        }

    def _build_conclusions(
        self,
        observation_count: int,
        entity_count: int,
        condition_count: int,
        memory_count: int,
        memory_assessment: dict[str, Any],
        feedback_analysis: dict[str, Any],
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

        if feedback_analysis.get(
            "feedback_count",
            0,
        ) > 0:
            conclusions.append(
                {
                    "type": "historical_feedback_available",
                    "value": True,
                    "description": (
                        "Historisches Feedback wurde "
                        "für das aktuelle Reasoning ausgewertet."
                    ),
                }
            )

        if feedback_analysis.get(
            "status"
        ) == "positive_history":
            conclusions.append(
                {
                    "type": "successful_history",
                    "value": True,
                    "description": (
                        "Die bisherige Verarbeitungshistorie "
                        "enthält erfolgreiche Ergebnisse."
                    ),
                }
            )

        if feedback_analysis.get(
            "status"
        ) == "adjustment_required":
            conclusions.append(
                {
                    "type": "adjustment_required",
                    "value": True,
                    "description": (
                        "Die bisherige Verarbeitungshistorie "
                        "enthält Ergebnisse, die eine Anpassung "
                        "erfordern."
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