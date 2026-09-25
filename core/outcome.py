"""
AIHelixia Intelligence Engine
Outcome Layer
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


class Outcome:
    """
    Bewertet den beobachtbaren Zustand nach einer Action.

    Die Outcome-Schicht vergleicht einen vorherigen Zustand
    mit einem beobachteten Zustand.

    V0.1.0:
    - deterministisch
    - reproduzierbar
    - keine LLM-Abhängigkeit
    - keine automatische Maschinensteuerung
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self.status = "created"
        self.outcome_count = 0

    def start(self) -> None:
        """Startet die Outcome-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Outcome-Schicht."""

        self.status = "stopped"

    def evaluate(
        self,
        previous_state: dict[str, Any],
        observed_state: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Vergleicht einen vorherigen Zustand mit einem
        beobachteten Zustand.

        Unterstützte industrielle Signale:

        - Temperatur
        - Vibration
        - Produktion
        - Energie

        Niedrigere Temperatur/Vibration werden als Verbesserung
        betrachtet.

        Höhere Produktion und niedrigere Energie werden als
        Verbesserung betrachtet.

        Wenn keine verwertbaren Messwerte vorhanden sind,
        bleibt der Outcome unknown.
        """

        if self.status != "running":
            raise RuntimeError(
                "Outcome ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(previous_state, dict):
            raise TypeError(
                "previous_state muss ein Dictionary sein."
            )

        if not isinstance(observed_state, dict):
            raise TypeError(
                "observed_state muss ein Dictionary sein."
            )

        self.outcome_count += 1

        comparisons: list[dict[str, Any]] = []

        # ---------------------------------------------------------
        # Temperatur
        # ---------------------------------------------------------

        self._compare_lower_is_better(
            "temperature",
            previous_state,
            observed_state,
            comparisons,
        )

        # ---------------------------------------------------------
        # Vibration
        # ---------------------------------------------------------

        self._compare_lower_is_better(
            "vibration",
            previous_state,
            observed_state,
            comparisons,
        )

        # ---------------------------------------------------------
        # Produktion
        # ---------------------------------------------------------

        self._compare_higher_is_better(
            "production",
            previous_state,
            observed_state,
            comparisons,
        )

        # ---------------------------------------------------------
        # Energie
        # ---------------------------------------------------------

        self._compare_lower_is_better(
            "energy",
            previous_state,
            observed_state,
            comparisons,
        )

        if not comparisons:
            return {
                "status": "evaluated",
                "version": self.VERSION,
                "outcome_id": self.outcome_count,
                "outcome": "unknown",
                "success": None,
                "confidence": 0.0,
                "comparisons": [],
                "message": (
                    "Es konnten keine vergleichbaren "
                    "Messwerte gefunden werden."
                ),
            }

        improved = sum(
            1
            for item in comparisons
            if item["direction"] == "improved"
        )

        degraded = sum(
            1
            for item in comparisons
            if item["direction"] == "degraded"
        )

        unchanged = sum(
            1
            for item in comparisons
            if item["direction"] == "unchanged"
        )

        total = len(comparisons)

        # ---------------------------------------------------------
        # Outcome bestimmen
        # ---------------------------------------------------------

        if improved > degraded:
            outcome = "improved"
            success = True

        elif degraded > improved:
            outcome = "degraded"
            success = False

        else:
            outcome = "unchanged"
            success = False

        confidence = round(
            max(improved, degraded, unchanged) / total,
            2,
        )

        return {
            "status": "evaluated",
            "version": self.VERSION,
            "outcome_id": self.outcome_count,
            "outcome": outcome,
            "success": success,
            "confidence": confidence,
            "comparisons": comparisons,
            "summary": {
                "improved": improved,
                "degraded": degraded,
                "unchanged": unchanged,
                "total": total,
            },
            "message": (
                "Der beobachtete Zustand zeigt eine "
                f"{outcome}-Entwicklung."
            ),
        }

    @staticmethod
    def _compare_lower_is_better(
        metric: str,
        previous_state: dict[str, Any],
        observed_state: dict[str, Any],
        comparisons: list[dict[str, Any]],
    ) -> None:
        previous = previous_state.get(metric)
        observed = observed_state.get(metric)

        if not isinstance(previous, (int, float)):
            return

        if not isinstance(observed, (int, float)):
            return

        if observed < previous:
            direction = "improved"
        elif observed > previous:
            direction = "degraded"
        else:
            direction = "unchanged"

        comparisons.append(
            {
                "metric": metric,
                "previous": previous,
                "observed": observed,
                "delta": observed - previous,
                "direction": direction,
            }
        )

    @staticmethod
    def _compare_higher_is_better(
        metric: str,
        previous_state: dict[str, Any],
        observed_state: dict[str, Any],
        comparisons: list[dict[str, Any]],
    ) -> None:
        previous = previous_state.get(metric)
        observed = observed_state.get(metric)

        if not isinstance(previous, (int, float)):
            return

        if not isinstance(observed, (int, float)):
            return

        if observed > previous:
            direction = "improved"
        elif observed < previous:
            direction = "degraded"
        else:
            direction = "unchanged"

        comparisons.append(
            {
                "metric": metric,
                "previous": previous,
                "observed": observed,
                "delta": observed - previous,
                "direction": direction,
            }
        )

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "outcome",
            "version": self.VERSION,
            "status": self.status,
            "outcome_count": self.outcome_count,
        }
