"""
AIHelixia Intelligence Engine
Decision Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class Decision:
    """
    Deterministische Decision-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - Reasoning-Ergebnisse auswerten
    - Predictions berücksichtigen
    - einen strukturierten nächsten Schritt bestimmen
    - noch keine Aktion ausführen

    V0.2.0:
    - deterministisch
    - reproduzierbar
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
        von Reasoning und Prediction.
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

        if state_assessment == "no_observations":
            decision_type = "wait"
            action = "observe"
            rationale = (
                "Es liegen keine Beobachtungen vor. "
                "Die Engine wartet auf weitere Informationen."
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
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "decision",
            "status": self.status,
        }