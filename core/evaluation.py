"""
AIHelixia Intelligence Engine
Evaluation Layer
Version: 0.3.0
"""

from __future__ import annotations

from typing import Any


class Evaluation:
    """
    Bewertet Action-Ausführung und beobachtbaren Outcome.

    Verantwortlichkeiten:
    - technische Action-Ausführung prüfen
    - beobachtbaren Outcome unterscheiden
    - Execution Success nicht mit Outcome Success verwechseln
    - strukturierte Bewertung erzeugen
    - Grundlage für Feedback und Learning Signal schaffen

    V0.3.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    - trennt Execution Status und Outcome Status
    """

    VERSION = "0.3.0"

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

        Wichtig:
        Eine erfolgreich ausgeführte Action bedeutet nicht automatisch,
        dass das industrielle Problem gelöst wurde.

        Deshalb werden zwei Ebenen getrennt:

        1. execution
           Wurde die Action technisch ausgeführt?

        2. outcome
           Ist ein tatsächlicher Outcome bekannt und erfolgreich?
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

        action_payload = action_result.get(
            "result",
            {},
        )

        if not isinstance(action_payload, dict):
            action_payload = {}

        execution_success = action_payload.get(
            "success",
            False,
        )

        outcome = action_result.get(
            "outcome",
        )

        outcome_status = "unknown"
        outcome_success: bool | None = None

        if isinstance(outcome, dict):
            outcome_status = outcome.get(
                "status",
                "unknown",
            )

            if "success" in outcome:
                outcome_success = outcome.get(
                    "success",
                )

        elif outcome is not None:
            outcome_status = str(outcome)

        # ---------------------------------------------------------
        # 1. Technische Ausführung bewerten
        # ---------------------------------------------------------

        if execution_status != "executed":
            execution_evaluation = "failed"
            execution_score = 0.0

        elif execution_success is True:
            execution_evaluation = "successful"
            execution_score = 1.0

        else:
            execution_evaluation = "unsuccessful"
            execution_score = 0.0

        # ---------------------------------------------------------
        # 2. Tatsächlichen Outcome bewerten
        # ---------------------------------------------------------

        if outcome_success is True:
            outcome_evaluation = "successful"
            outcome_score = 1.0

        elif outcome_success is False:
            outcome_evaluation = "unsuccessful"
            outcome_score = 0.0

        else:
            outcome_evaluation = "unknown"
            outcome_score = None

        # ---------------------------------------------------------
        # 3. Gesamtevaluation
        # ---------------------------------------------------------

        if execution_evaluation == "failed":
            evaluation = "failed"
            score = 0.0
            message = (
                "Die Action wurde technisch nicht erfolgreich "
                "ausgeführt."
            )

        elif outcome_evaluation == "successful":
            evaluation = "successful"
            score = outcome_score
            message = (
                "Die Action wurde erfolgreich ausgeführt "
                "und der beobachtete Outcome war erfolgreich."
            )

        elif outcome_evaluation == "unsuccessful":
            evaluation = "unsuccessful"
            score = outcome_score
            message = (
                "Die Action wurde technisch ausgeführt, "
                "aber der beobachtete Outcome war nicht erfolgreich."
            )

        else:
            evaluation = "execution_success_outcome_unknown"
            score = execution_score
            message = (
                "Die Action wurde technisch erfolgreich ausgeführt, "
                "aber ein tatsächlicher Outcome ist noch nicht bekannt."
            )

        return {
            "status": "evaluated",
            "version": self.VERSION,
            "evaluation_id": self.evaluation_count,

            # Gesamtbewertung
            "evaluation": evaluation,
            "score": score,
            "message": message,

            # Technische Ausführung
            "action_status": execution_status,
            "execution_evaluation": execution_evaluation,
            "execution_score": execution_score,

            # Tatsächlicher Outcome
            "outcome_status": outcome_status,
            "outcome_evaluation": outcome_evaluation,
            "outcome_score": outcome_score,
            "outcome_known": outcome_success is not None,
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "evaluation",
            "version": self.VERSION,
            "status": self.status,
            "evaluation_count": self.evaluation_count,
        }
