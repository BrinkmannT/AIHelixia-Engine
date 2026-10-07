"""
AIHelixia Intelligence Engine
Value Prioritization Layer
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


class ValuePrioritization:
    """
    Deterministische wirtschaftliche Priorisierung.

    Verantwortlichkeiten:
    - Economic Findings wirtschaftlich bewerten
    - Findings vergleichbar machen
    - wirtschaftliche Priorität bestimmen
    - Prioritäten transparent begründen

    Keine LLM-Abhängigkeit.
    Keine externen Aktionen.
    Keine Änderung der Economic-Discovery-Berechnung.
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self.status = "created"
        self.analysis_count = 0
        self.last_analysis: dict[str, Any] | None = None

    def start(self) -> None:
        self.status = "running"

    def stop(self) -> None:
        self.status = "stopped"

    def prioritize(
        self,
        economic_discovery: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Priorisiert wirtschaftliche Findings.

        Die Priorisierung basiert auf:

        - Savings Potential
        - Economic Impact
        - Confidence
        - bestehender Priorität

        Der Score ist deterministisch und zwischen 0 und 100.
        """

        if self.status != "running":
            raise RuntimeError(
                "Value Prioritization ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(economic_discovery, dict):
            raise TypeError(
                "Economic Discovery muss ein Dictionary sein."
            )

        self.analysis_count += 1

        findings = economic_discovery.get("findings", [])

        if not isinstance(findings, list):
            findings = []

        prioritized: list[dict[str, Any]] = []

        for index, finding in enumerate(findings, start=1):
            if not isinstance(finding, dict):
                continue

            prioritized.append(
                self._prioritize_finding(
                    finding=finding,
                    rank=index,
                )
            )

        prioritized.sort(
            key=lambda item: (
                item["priority_score"],
                item["savings_potential"] or 0.0,
                item["economic_impact"] or 0.0,
            ),
            reverse=True,
        )

        for rank, finding in enumerate(prioritized, start=1):
            finding["rank"] = rank

        critical_count = sum(
            1
            for finding in prioritized
            if finding["value_priority"] == "critical"
        )

        high_count = sum(
            1
            for finding in prioritized
            if finding["value_priority"] == "high"
        )

        result = {
            "status": "prioritization_completed",
            "version": self.VERSION,
            "finding_count": len(prioritized),
            "critical_count": critical_count,
            "high_count": high_count,
            "top_finding": (
                prioritized[0]
                if prioritized
                else None
            ),
            "findings": prioritized,
        }

        self.last_analysis = result

        return result

    def _prioritize_finding(
        self,
        finding: dict[str, Any],
        rank: int,
    ) -> dict[str, Any]:
        economic_impact = self._safe_float(
            finding.get("economic_impact")
        )

        savings_potential = self._safe_float(
            finding.get("savings_potential")
        )

        confidence = self._safe_float(
            finding.get("confidence")
        )

        if confidence is None:
            confidence = 0.0

        confidence = max(0.0, min(1.0, confidence))

        existing_priority = finding.get(
            "priority",
            "unknown",
        )

        # ---------------------------------------------------------
        # Economic value component
        # ---------------------------------------------------------

        if savings_potential is not None and savings_potential > 0:
            value_score = 60.0
        elif economic_impact is not None and economic_impact > 0:
            value_score = 40.0
        else:
            value_score = 0.0

        # ---------------------------------------------------------
        # Confidence component
        # ---------------------------------------------------------

        confidence_score = confidence * 25.0

        # ---------------------------------------------------------
        # Existing economic severity
        # ---------------------------------------------------------

        priority_bonus = {
            "critical": 15.0,
            "high": 10.0,
            "medium": 5.0,
            "low": 0.0,
            "unknown": 0.0,
        }.get(existing_priority, 0.0)

        priority_score = min(
            100.0,
            value_score
            + confidence_score
            + priority_bonus,
        )

        priority_score = round(
            priority_score,
            2,
        )

        value_priority = self._priority_level(
            priority_score
        )

        return {
            "rank": rank,
            "type": finding.get("type"),
            "category": finding.get("category"),
            "problem": finding.get("problem"),
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "confidence": confidence,
            "existing_priority": existing_priority,
            "priority_score": priority_score,
            "value_priority": value_priority,
            "reason": self._build_reason(
                savings_potential=savings_potential,
                economic_impact=economic_impact,
                confidence=confidence,
                value_priority=value_priority,
            ),
        }

    @staticmethod
    def _priority_level(score: float) -> str:
        if score >= 85.0:
            return "critical"

        if score >= 65.0:
            return "high"

        if score >= 40.0:
            return "medium"

        return "low"

    @staticmethod
    def _build_reason(
        savings_potential: float | None,
        economic_impact: float | None,
        confidence: float,
        value_priority: str,
    ) -> str:
        if savings_potential is not None:
            return (
                f"{value_priority} wirtschaftliche Priorität "
                f"auf Basis von Savings Potential "
                f"€{savings_potential:,.2f} und "
                f"{confidence:.0%} Confidence."
            )

        if economic_impact is not None:
            return (
                f"{value_priority} wirtschaftliche Priorität "
                f"auf Basis eines Economic Impact von "
                f"€{economic_impact:,.2f} und "
                f"{confidence:.0%} Confidence."
            )

        return (
            f"{value_priority} wirtschaftliche Priorität "
            f"aufgrund unzureichender wirtschaftlicher Daten."
        )

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None
