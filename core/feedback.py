"""
AIHelixia Intelligence Engine
Feedback Layer
Version: 0.4.0
"""

from __future__ import annotations

from typing import Any


class Feedback:
    """
    Verarbeitet Evaluation-Ergebnisse und erzeugt
    strukturierte Learning Signals.

    V0.4.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    - Outcome-aware
    - unterscheidet improved / degraded /
      unchanged / unknown
    """

    VERSION = "0.4.0"

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
        Verarbeitet ein Evaluation-Ergebnis.

        Learning Signals:

        improved
            → reinforce

        degraded
            → adjust

        unchanged
            → review

        unknown
            → review
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

        outcome_status = evaluation.get(
            "outcome_status",
            "unknown",
        )

        outcome_confidence = evaluation.get(
            "outcome_confidence",
            0.0,
        )

        score = evaluation.get(
            "score",
            0.0,
        )

        # ---------------------------------------------------------
        # 1. Bestätigte Verbesserung
        # ---------------------------------------------------------

        if (
            evaluation_result == "successful"
            and outcome_status == "improved"
        ):
            feedback_type = "positive"
            signal = "reinforce"

            recommendation = (
                "Der beobachtete Zustand hat sich verbessert. "
                "Die zugrunde liegende Strategie kann unter "
                "vergleichbaren Bedingungen verstärkt werden."
            )

        # ---------------------------------------------------------
        # 2. Bestätigte Verschlechterung
        # ---------------------------------------------------------

        elif (
            evaluation_result == "unsuccessful"
            and outcome_status == "degraded"
        ):
            feedback_type = "negative"
            signal = "adjust"

            recommendation = (
                "Der beobachtete Zustand hat sich verschlechtert. "
                "Die zugrunde liegende Strategie sollte überprüft "
                "und angepasst werden."
            )

        # ---------------------------------------------------------
        # 3. Zustand unverändert
        # ---------------------------------------------------------

        elif (
            evaluation_result == "unchanged"
            and outcome_status == "unchanged"
        ):
            feedback_type = "neutral"
            signal = "review"

            recommendation = (
                "Der beobachtete Zustand hat sich nicht verändert. "
                "Die Strategie sollte überprüft werden, bevor "
                "sie erneut eingesetzt wird."
            )

        # ---------------------------------------------------------
        # 4. Outcome unbekannt
        # ---------------------------------------------------------

        elif (
            evaluation_result
            == "execution_success_outcome_unknown"
            or outcome_status == "unknown"
        ):
            feedback_type = "pending"
            signal = "review"

            recommendation = (
                "Die Action wurde technisch erfolgreich ausgeführt, "
                "aber der tatsächliche Outcome ist noch nicht bekannt. "
                "Es sollte zunächst eine Outcome-Beobachtung erfolgen."
            )

        # ---------------------------------------------------------
        # 5. Technischer Fehler
        # ---------------------------------------------------------

        elif evaluation_result == "failed":
            feedback_type = "error"
            signal = "adjust"

            recommendation = (
                "Die Action konnte technisch nicht erfolgreich "
                "ausgeführt werden. Die Ausführung sollte "
                "überprüft und angepasst werden."
            )

        # ---------------------------------------------------------
        # 6. Fallback
        # ---------------------------------------------------------

        else:
            feedback_type = "error"
            signal = "review"

            recommendation = (
                "Das Evaluation-Ergebnis ist nicht eindeutig. "
                "Es sollte überprüft werden, bevor die Strategie "
                "erneut verwendet wird."
            )

        return {
            "status": "processed",
            "version": self.VERSION,
            "feedback_id": self.feedback_count,

            "feedback_type": feedback_type,
            "signal": signal,

            "score": score,
            "outcome_status": outcome_status,
            "outcome_confidence": outcome_confidence,

            "recommendation": recommendation,
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "feedback",
            "version": self.VERSION,
            "status": self.status,
            "feedback_count": self.feedback_count,
        }
