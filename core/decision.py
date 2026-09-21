"""
AIHelixia Intelligence Engine
Decision Layer
Version: 0.4.3
"""

from __future__ import annotations

from typing import Any


class Decision:
    """
    Deterministische Decision-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - Reasoning-Ergebnisse auswerten
    - Predictions berücksichtigen
    - Learning Signals berücksichtigen
    - strukturierten nächsten Schritt bestimmen
    - noch keine externe Aktion ausführen

    V0.4.3:
    - deterministisch
    - reproduzierbar
    - Memory-aware
    - Feedback-aware
    - Learning Signal-aware
    - keine LLM-Abhängigkeit
    - keine externe Aktion
    """

    def __init__(self) -> None:
        self.status = "created"

    def start(self) -> None:
        """Startet die Decision-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Decision-Schicht."""

        self.status = "stopped"

    def decide(
        self,
        reasoning: dict[str, Any],
        prediction: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Erzeugt eine strukturierte Entscheidung auf Basis
        von Reasoning, Prediction und Learning Signal.
        """

        if self.status != "running":
            raise RuntimeError(
                "Decision ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(reasoning, dict):
            raise TypeError(
                "Reasoning muss ein Dictionary sein."
            )

        if not isinstance(prediction, dict):
            raise TypeError(
                "Prediction muss ein Dictionary sein."
            )

        state_assessment = reasoning.get(
            "state_assessment",
            "unknown",
        )

        scenarios = prediction.get(
            "scenarios",
            [],
        )

        learning_signal = reasoning.get(
            "learning_signal",
            {},
        )

        if not isinstance(learning_signal, dict):
            raise TypeError(
                "Learning Signal muss ein Dictionary sein."
            )

        learning_type = learning_signal.get(
            "type",
            "review",
        )

        learning_priority = learning_signal.get(
            "priority",
            "normal",
        )

        if state_assessment == "no_observations":

            decision_type = "wait"
            action = "observe"

            rationale = (
                "Es liegen keine Beobachtungen vor. "
                "Die Engine wartet auf weitere Informationen."
            )

        elif learning_type == "adjust":

            decision_type = "adjust"
            action = "review_strategy"

            rationale = (
                "Historisches Feedback enthält negative "
                "oder fehlerhafte Ergebnisse. "
                "Die bisherige Strategie soll überprüft "
                "und angepasst werden."
            )

        elif learning_type == "reinforce" and scenarios:

            decision_type = "reinforce"
            action = "continue_monitoring"

            rationale = (
                "Historisches Feedback zeigt erfolgreiche "
                "Verarbeitung. Die bisherige Strategie "
                "wird für den aktuellen Zustand beibehalten."
            )

        elif learning_type == "review":

            decision_type = "review"
            action = "observe"

            rationale = (
                "Es liegt noch kein ausreichendes historisches "
                "Feedback vor. Der aktuelle Zustand soll "
                "weiter beobachtet werden."
            )

        elif scenarios:

            decision_type = "monitor"
            action = "continue_monitoring"

            rationale = (
                "Es liegen Beobachtungen und mindestens "
                "ein mögliches Szenario vor. "
                "Der Zustand soll weiter beobachtet werden."
            )

        else:

            decision_type = "wait"
            action = "observe"

            rationale = (
                "Es konnte kein verwertbares Szenario "
                "für eine weitere Entscheidung bestimmt werden."
            )

        return {
            "status": "decided",
            "decision_type": decision_type,
            "action": action,
            "rationale": rationale,
            "scenario_count": len(scenarios),
            "learning_signal": {
                "type": learning_type,
                "priority": learning_priority,
            },
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "decision",
            "status": self.status,
        }