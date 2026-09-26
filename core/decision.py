"""
AIHelixia Intelligence Engine
Decision Layer
Version: 0.5.1
"""

from __future__ import annotations

from typing import Any


class Decision:
    """
    Deterministische Decision-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - Reasoning-Ergebnisse auswerten
    - Predictions berücksichtigen
    - Root-Cause-Ergebnisse berücksichtigen
    - Evidence berücksichtigen
    - Historical Support berücksichtigen
    - Learning Signals berücksichtigen
    - strukturierten nächsten Schritt bestimmen
    - noch keine externe Aktion ausführen

    V0.5.1:
    - deterministisch
    - reproduzierbar
    - Memory-aware
    - Feedback-aware
    - Learning Signal-aware
    - Root-Cause-aware
    - Evidence-aware
    - Historical-Support-aware
    - keine LLM-Abhängigkeit
    - keine externe Aktion
    """

    VERSION = "0.5.1"

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
        root_cause: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Erzeugt eine strukturierte Entscheidung auf Basis
        von Reasoning, Prediction, Root Cause, Evidence,
        Historical Support und Learning Signal.
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

        if root_cause is not None and not isinstance(
            root_cause,
            dict,
        ):
            raise TypeError(
                "Root Cause muss ein Dictionary oder None sein."
            )

        state_assessment = reasoning.get(
            "state_assessment",
            "unknown",
        )

        scenarios = prediction.get(
            "scenarios",
            [],
        )

        if not isinstance(
            scenarios,
            list,
        ):
            scenarios = []

        learning_signal = reasoning.get(
            "learning_signal",
            {},
        )

        if not isinstance(
            learning_signal,
            dict,
        ):
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

        # ---------------------------------------------------------
        # Root Cause Analysis
        # ---------------------------------------------------------

        root_cause_status = "not_available"
        root_cause_priority = "none"
        root_cause_type = None
        root_cause_confidence = None
        root_cause_hypothesis_count = 0

        root_cause_evidence: dict[str, Any] = {}
        root_cause_historical_support: dict[str, Any] = {}

        if isinstance(
            root_cause,
            dict,
        ):

            root_cause_status = root_cause.get(
                "status",
                "unknown",
            )

            root_cause_hypothesis_count = root_cause.get(
                "hypothesis_count",
                0,
            )

            primary_hypothesis = root_cause.get(
                "primary_hypothesis",
                {},
            )

            if isinstance(
                primary_hypothesis,
                dict,
            ):

                root_cause_priority = (
                    primary_hypothesis.get(
                        "priority",
                        "none",
                    )
                )

                root_cause_type = (
                    primary_hypothesis.get(
                        "type"
                    )
                )

                root_cause_confidence = (
                    primary_hypothesis.get(
                        "confidence"
                    )
                )

                primary_evidence = (
                    primary_hypothesis.get(
                        "evidence",
                        {},
                    )
                )

                if isinstance(
                    primary_evidence,
                    dict,
                ):
                    root_cause_evidence = (
                        primary_evidence
                    )

                historical_support = (
                    primary_hypothesis.get(
                        "historical_support",
                        {},
                    )
                )

                if isinstance(
                    historical_support,
                    dict,
                ):
                    root_cause_historical_support = (
                        historical_support
                    )

        # ---------------------------------------------------------
        # Evidence Summary
        # ---------------------------------------------------------

        evidence_count = root_cause_evidence.get(
            "evidence_count",
            0,
        )

        evidence_strength = root_cause_evidence.get(
            "evidence_strength",
            "none",
        )

        supporting_signals = root_cause_evidence.get(
            "supporting_signals",
            [],
        )

        correlated_machines = root_cause_evidence.get(
            "correlated_machines",
            [],
        )

        supporting_predictions = root_cause_evidence.get(
            "supporting_predictions",
            [],
        )

        historical_status = (
            root_cause_historical_support.get(
                "status",
                "not_available",
            )
        )

        historical_strength = (
            root_cause_historical_support.get(
                "strength",
                "none",
            )
        )

        historical_outcome_count = (
            root_cause_historical_support.get(
                "known_outcome_count",
                0,
            )
        )

        historical_average_confidence = (
            root_cause_historical_support.get(
                "average_confidence"
            )
        )

        historical_dominant_outcome = (
            root_cause_historical_support.get(
                "dominant_outcome"
            )
        )

        # ---------------------------------------------------------
        # Decision Logic
        # ---------------------------------------------------------

        if state_assessment == "no_observations":

            decision_type = "wait"
            action = "observe"

            rationale = (
                "Es liegen keine Beobachtungen vor. "
                "Die Engine wartet auf weitere Informationen."
            )

        elif (
            root_cause_status
            in {
                "analysis_completed",
                "hypotheses_generated",
            }
            and root_cause_priority == "critical"
        ):

            decision_type = "root_cause_review"
            action = "review_strategy"

            rationale = (
                "Die Root-Cause-Analyse enthält eine "
                "kritische Hypothese. Der erkannte Zustand "
                "soll gezielt überprüft werden, bevor "
                "eine weitere Strategie beibehalten wird."
            )

        elif (
            root_cause_status
            in {
                "analysis_completed",
                "hypotheses_generated",
            }
            and root_cause_priority == "high"
            and learning_type == "adjust"
        ):

            decision_type = "root_cause_adjust"
            action = "review_strategy"

            rationale = (
                "Die Root-Cause-Analyse enthält eine "
                "hoch priorisierte Hypothese und historisches "
                "Feedback signalisiert eine notwendige "
                "Anpassung der bisherigen Strategie."
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

        # ---------------------------------------------------------
        # Structured Evidence
        # ---------------------------------------------------------

        evidence = {
            "evidence_count": evidence_count,
            "evidence_strength": evidence_strength,
            "supporting_signals": supporting_signals,
            "correlated_machines": correlated_machines,
            "supporting_predictions": supporting_predictions,
            "historical_support": {
                "status": historical_status,
                "strength": historical_strength,
                "known_outcome_count": (
                    historical_outcome_count
                ),
                "average_confidence": (
                    historical_average_confidence
                ),
                "dominant_outcome": (
                    historical_dominant_outcome
                ),
            },
        }

        return {
            "status": "decided",
            "version": self.VERSION,
            "decision_type": decision_type,
            "action": action,
            "rationale": rationale,
            "scenario_count": len(scenarios),
            "root_cause": {
                "status": root_cause_status,
                "hypothesis_count": root_cause_hypothesis_count,
                "primary_type": root_cause_type,
                "priority": root_cause_priority,
                "confidence": root_cause_confidence,
            },
            "evidence": evidence,
            "learning_signal": {
                "type": learning_type,
                "priority": learning_priority,
            },
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "decision",
            "version": self.VERSION,
            "status": self.status,
        }
