"""
AIHelixia Intelligence Engine
Feedback Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class Feedback:
    """
    Verarbeitet Evaluation-Ergebnisse und erzeugt
    strukturiertes Feedback für die nächste Verarbeitung.

    Verantwortlichkeiten:
    - Evaluation aufnehmen
    - Erfolg oder Misserfolg klassifizieren
    - Verbesserungssignale erzeugen
    - Feedback strukturiert bereitstellen

    V0.2.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    """

    def __init__(self) -> None:
        self.status = "created"
        self.feedback_count = 0

    def start(self) -> None:
        """Startet die Feedback-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Feedback-Schicht."""

        self.status = "stopped"

    def process(
        self,
        evaluation: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Verarbeitet ein Evaluation-Ergebnis und erzeugt
        ein strukturiertes Feedback-Signal.
        """

        if self.status != "running":
            raise RuntimeError(
                "Feedback ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(evaluation, dict):
            raise TypeError(
                "Evaluation muss ein Dictionary sein."
            )

        self.feedback_count += 1

        evaluation_result = evaluation.get(
            "evaluation",
            "unknown",
        )

        score = evaluation.get(
            "score",
            0.0,
        )

        if evaluation_result == "successful":
            feedback_type = "positive"
            signal = "reinforce"
            recommendation = (
                "Die ausgeführte Strategie kann "
                "beibehalten werden."
            )

        elif evaluation_result == "unsuccessful":
            feedback_type = "negative"
            signal = "adjust"
            recommendation = (
                "Die Strategie sollte überprüft "
                "und angepasst werden."
            )

        else:
            feedback_type = "error"
            signal = "review"
            recommendation = (
                "Das Ergebnis sollte überprüft werden, "
                "bevor die Strategie erneut verwendet wird."
            )

        return {
            "status": "processed",
            "feedback_id": self.feedback_count,
            "feedback_type": feedback_type,
            "signal": signal,
            "score": score,
            "recommendation": recommendation,
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "feedback",
            "status": self.status,
            "feedback_count": self.feedback_count,
        }