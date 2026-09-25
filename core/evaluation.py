"""
AIHelixia Intelligence Engine
Evaluation Layer
Version: 0.4.0
"""

from __future__ import annotations

from typing import Any


class Evaluation:
    """
    Bewertet Action-Ausführung und beobachtbaren Outcome.

    Verantwortlichkeiten:
    - technische Action-Ausführung prüfen
    - beobachtbaren Outcome auswerten
    - Execution Success von Outcome Success trennen
    - strukturiertes Evaluation-Ergebnis erzeugen
    - Grundlage für Feedback und Learning Signal schaffen

    V0.4.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    - Outcome Engine Integration
    - Execution und Outcome getrennt
    """

    VERSION = "0.4.0"

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
        outcome_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Bewertet Action-Ausführung und optionalen Outcome.

        action_result:
            Ergebnis der technischen Action-Ausführung.

        outcome_result:
            Ergebnis der Outcome Engine.

        Wichtig:
        Eine erfolgreich ausgeführte Action bedeutet nicht automatisch,
        dass das industrielle Problem gelöst wurde.
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

        if outcome_result is not None and not isinstance(
            outcome_result,
            dict,
        ):
            raise TypeError(
                "Outcome-Ergebnis muss ein Dictionary sein."
            )

        self.evaluation_count += 1

        # ---------------------------------------------------------
        # 1. Technische Action-Ausführung
        # ---------------------------------------------------------

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
        # 2. Outcome auswerten
        # ---------------------------------------------------------

        outcome_status = "unknown"
        outcome_success: bool | None = None
        outcome_score: float | None = None
        outcome_confidence = 0.0

        if outcome_result is not None:

            outcome_status = outcome_result.get(
                "outcome",
                "unknown",
            )

            raw_success = outcome_result.get(
                "success",
            )

            if isinstance(raw_success, bool):
                outcome_success = raw_success

            raw_confidence = outcome_result.get(
                "confidence",
                0.0,
            )

            if isinstance(raw_confidence, (int, float)):
                outcome_confidence = float(
                    raw_confidence
                )

            if outcome_success is True:
                outcome_score = 1.0

            elif outcome_success is False:
                outcome_score = 0.0

        # ---------------------------------------------------------
        # 3. Outcome Evaluation
        # ---------------------------------------------------------

        if outcome_success is True:
            outcome_evaluation = "successful"

        elif outcome_success is False:
            if outcome_status == "unchanged":
                outcome_evaluation = "unchanged"
            else:
                outcome_evaluation = "unsuccessful"

        else:
            outcome_evaluation = "unknown"

        # ---------------------------------------------------------
        # 4. Gesamtevaluation
        # ---------------------------------------------------------

        if execution_evaluation == "failed":

            evaluation = "failed"
            score = 0.0

            message = (
                "Die Action wurde technisch nicht "
                "erfolgreich ausgeführt."
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

        elif outcome_evaluation == "unchanged":

            evaluation = "unchanged"
            score = 0.0

            message = (
                "Die Action wurde ausgeführt, "
                "aber der beobachtete Zustand hat sich "
                "nicht verbessert."
            )

        else:

            evaluation = "execution_success_outcome_unknown"
            score = execution_score

            message = (
                "Die Action wurde technisch erfolgreich "
                "ausgeführt, aber ein tatsächlicher "
                "Outcome ist noch nicht bekannt."
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

            # Outcome
            "outcome_status": outcome_status,
            "outcome_evaluation": outcome_evaluation,
            "outcome_score": outcome_score,
            "outcome_confidence": outcome_confidence,
            "outcome_known": outcome_success is not None,

            # Metadaten
            "outcome_result_available": outcome_result is not None,
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "evaluation",
            "version": self.VERSION,
            "status": self.status,
            "evaluation_count": self.evaluation_count,
        }
