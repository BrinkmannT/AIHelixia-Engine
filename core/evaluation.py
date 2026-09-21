"""
AIHelixia Intelligence Engine
Evaluation Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class Evaluation:
    """
    Bewertet die Ausführung einer Action.

    Verantwortlichkeiten:
    - Action-Ergebnis prüfen
    - Erfolg oder Fehler feststellen
    - strukturierte Bewertung erzeugen
    - Grundlage für späteres Feedback schaffen

    V0.2.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    """

    def __init__(self) -> None:
        self.status = "created"
        self.evaluation_count = 0

    def start(self) -> None:
        """Startet die Evaluation-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Evaluation-Schicht."""

        self.status = "stopped"

    def evaluate(
        self,
        action_result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Bewertet das Ergebnis einer ausgeführten Action.
        """

        if self.status != "running":
            raise RuntimeError(
                "Evaluation ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(action_result, dict):
            raise TypeError(
                "Action-Ergebnis muss ein Dictionary sein."
            )

        self.evaluation_count += 1

        execution_status = action_result.get(
            "status",
            "unknown",
        )

        result = action_result.get(
            "result",
            {},
        )

        success = result.get(
            "success",
            False,
        )

        if execution_status != "executed":
            evaluation = "failed"
            score = 0.0
            message = (
                "Die Action wurde nicht erfolgreich "
                "ausgeführt."
            )

        elif success is True:
            evaluation = "successful"
            score = 1.0
            message = (
                "Die Action wurde erfolgreich "
                "ausgeführt."
            )

        else:
            evaluation = "unsuccessful"
            score = 0.0
            message = (
                "Die Action wurde ausgeführt, "
                "aber das Ergebnis war nicht erfolgreich."
            )

        return {
            "status": "evaluated",
            "evaluation_id": self.evaluation_count,
            "evaluation": evaluation,
            "score": score,
            "message": message,
            "action_status": execution_status,
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "evaluation",
            "status": self.status,
            "evaluation_count": self.evaluation_count,
        }