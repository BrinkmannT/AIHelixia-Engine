"""
AIHelixia Intelligence Engine
Feedback Layer
Version: 0.3.0
"""

from __future__ import annotations

from typing import Any


class Feedback:
    """
    Verarbeitet Evaluation-Ergebnisse und erzeugt
    strukturiertes Feedback für die nächste Verarbeitung.

    Verantwortlichkeiten:
    - Evaluation aufnehmen
    - technische Ausführung von tatsächlichem Outcome unterscheiden
    - Erfolg oder Misserfolg klassifizieren
    - Verbesserungssignale erzeugen
    - Feedback strukturiert bereitstellen

    V0.3.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    - berücksichtigt unbekannte Outcomes
    """

    VERSION = "0.3.0"

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

        Wichtig:
        Ein technisch erfolgreicher Action-Run mit unbekanntem
        Outcome darf nicht als positives Learning Signal
        interpretiert werden.
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

        outcome_known = evaluation.get(
            "outcome_known",
            False,
        )

        outcome_evaluation = evaluation.get(
            "outcome_evaluation",
            "unknown",
        )

        execution_evaluation = evaluation.get(
            "execution_evaluation",
            "unknown",
        )

        # ---------------------------------------------------------
        # 1. Bestätigter positiver Outcome
        # ---------------------------------------------------------

        if (
            evaluation_result == "successful"
            and outcome_known is True
            and outcome_evaluation == "successful"
        ):
            feedback_type = "positive"
            signal = "reinforce"
            recommendation = (
                "Der beobachtete Outcome war erfolgreich. "
                "Die zugrunde liegende Strategie kann "
                "unter vergleichbaren Bedingungen "
                "beibehalten werden."
            )

        # ---------------------------------------------------------
        # 2. Bestätigter negativer Outcome
        # ---------------------------------------------------------

        elif (
            evaluation_result == "unsuccessful"
            and outcome_known is True
            and outcome_evaluation == "unsuccessful"
        ):
            feedback_type = "negative"
            signal = "adjust"
            recommendation = (
                "Der beobachtete Outcome war nicht erfolgreich. "
                "Die Strategie sollte überprüft und "
                "gegebenenfalls angepasst werden."
            )

        # ---------------------------------------------------------
        # 3. Action technisch erfolgreich, Outcome unbekannt
        # ---------------------------------------------------------

        elif (
            evaluation_result
            == "execution_success_outcome_unknown"
            or outcome_known is False
        ):
            feedback_type = "pending"
            signal = "review"
            recommendation = (
                "Die Action wurde technisch erfolgreich "
                "ausgeführt, aber der tatsächliche Outcome "
                "ist noch nicht bekannt. Es sollte zunächst "
                "eine Outcome-Beobachtung erfolgen."
            )

        # ---------------------------------------------------------
        # 4. Technische Ausführung fehlgeschlagen
        # ---------------------------------------------------------

        elif execution_evaluation == "failed":
            feedback_type = "error"
            signal = "adjust"
            recommendation = (
                "Die Action konnte technisch nicht "
                "erfolgreich ausgeführt werden. "
                "Die Ausführung sollte überprüft werden."
            )

        # ---------------------------------------------------------
        # 5. Fallback
        # ---------------------------------------------------------

        else:
            feedback_type = "error"
            signal = "review"
            recommendation = (
                "Das Evaluation-Ergebnis ist nicht eindeutig. "
                "Es sollte überprüft werden, bevor die "
                "Strategie erneut verwendet wird."
            )

        return {
            "status": "processed",
            "version": self.VERSION,
            "feedback_id": self.feedback_count,
            "feedback_type": feedback_type,
            "signal": signal,
            "score": score,
            "outcome_known": outcome_known,
            "outcome_evaluation": outcome_evaluation,
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
