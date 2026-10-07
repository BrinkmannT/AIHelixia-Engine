"""
AIHelixia Intelligence Engine
Decision Layer
Version: 0.5.2
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

    VERSION = "0.5.2"

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
        economic_discovery: dict[str, Any] | None = None,
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

        if economic_discovery is not None and not isinstance(
            economic_discovery,
            dict,
        ):
            raise TypeError(
                "Economic Discovery muss ein Dictionary oder None sein."
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
            "action",
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
        # Economic Discovery
        # ---------------------------------------------------------

        economic_status = "not_available"
        economic_finding_count = 0
        economic_critical_count = 0
        total_economic_impact = None
        total_savings_potential = None
        economic_priority = "none"
        economic_confidence = None
        economic_findings = []

        if isinstance(
            economic_discovery,
            dict,
        ):
            economic_status = economic_discovery.get(
                "status",
                "unknown",
            )

            economic_finding_count = self._safe_int(
                economic_discovery.get(
                    "finding_count",
                    0,
                )
            )

            economic_critical_count = self._safe_int(
                economic_discovery.get(
                    "critical_count",
                    0,
                )
            )

            total_economic_impact = self._safe_float(
                economic_discovery.get(
                    "total_economic_impact"
                )
            )

            total_savings_potential = self._safe_float(
                economic_discovery.get(
                    "total_savings_potential"
                )
            )

            findings = economic_discovery.get(
                "findings",
                [],
            )

            if isinstance(
                findings,
                list,
            ):
                economic_findings = [
                    finding
                    for finding in findings
                    if isinstance(
                        finding,
                        dict,
                    )
                ]

            economic_priority = self._determine_economic_priority(
                economic_discovery
            )

            economic_confidence = self._determine_economic_confidence(
                economic_discovery
            )

        economic_actionable = (
            economic_finding_count > 0
            and economic_status == "analysis_completed"
        )

        economic_verified = self._has_verified_economic_evidence(
            economic_findings
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
            economic_actionable
            and economic_priority == "critical"
            and economic_verified
        ):

            decision_type = "economic_priority"
            action = "review_strategy"

            rationale = (
                "Die Economic-Discovery-Analyse enthält "
                "ein verifiziertes kritisches wirtschaftliches "
                "Finding. Der erkannte wirtschaftliche Impact "
                "soll priorisiert untersucht werden."
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
            "economic": {
                "status": economic_status,
                "actionable": economic_actionable,
                "verified": economic_verified,
                "finding_count": economic_finding_count,
                "critical_count": economic_critical_count,
                "priority": economic_priority,
                "confidence": economic_confidence,
                "total_economic_impact": total_economic_impact,
                "total_savings_potential": total_savings_potential,
            },
            "evidence": evidence,
            "learning_signal": {
                "type": learning_type,
                "priority": learning_priority,
            },
        }


    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        return None

    @staticmethod
    def _safe_int(
        value: Any,
    ) -> int:
        if isinstance(value, bool):
            return 0

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        return 0

    @staticmethod
    def _determine_economic_priority(
        economic_discovery: dict[str, Any],
    ) -> str:
        findings = economic_discovery.get(
            "findings",
            [],
        )

        if not isinstance(findings, list):
            return "none"

        ranking = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
        }

        priorities = [
            finding.get("priority")
            for finding in findings
            if isinstance(finding, dict)
            and finding.get("priority") in ranking
        ]

        if not priorities:
            return "none"

        return max(
            priorities,
            key=lambda priority: ranking[priority],
        )

    @classmethod
    def _determine_economic_confidence(
        cls,
        economic_discovery: dict[str, Any],
    ) -> float | None:
        findings = economic_discovery.get(
            "findings",
            [],
        )

        if not isinstance(findings, list):
            return None

        confidences = []

        for finding in findings:
            if not isinstance(finding, dict):
                continue

            confidence = cls._safe_float(
                finding.get("confidence")
            )

            if confidence is not None:
                confidences.append(confidence)

        if not confidences:
            return None

        return max(confidences)

    @staticmethod
    def _has_verified_economic_evidence(
        findings: list[dict[str, Any]],
    ) -> bool:
        for finding in findings:
            evidence = finding.get(
                "evidence",
                {},
            )

            if not isinstance(evidence, dict):
                continue

            if evidence.get("verified") is True:
                return True

        return False

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "decision",
            "version": self.VERSION,
            "status": self.status,
        }
