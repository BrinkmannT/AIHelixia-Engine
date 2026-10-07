"""
AIHelixia Intelligence Engine
Economic Opportunity Layer
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


class EconomicOpportunity:
    """
    Deterministische Economic-Opportunity-Schicht.

    Verantwortlichkeiten:
    - Economic Findings in konkrete Opportunities überführen
    - wirtschaftlichen Wert strukturiert zusammenfassen
    - vorhandene Priorisierung übernehmen
    - empfohlene nächste Handlung ableiten
    - Opportunities für Decision, Dashboard und Outcome bereitstellen

    Keine LLM-Abhängigkeit.
    Keine externen Aktionen.
    Keine neue wirtschaftliche Berechnung.
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

    def get_status(self) -> dict[str, Any]:
        """
        Liefert den aktuellen Status des Economic Opportunity Layers.
        """
        return {
            "name": "Economic Opportunity",
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
            "last_analysis": self.last_analysis,
        }

    def build(
        self,
        economic_discovery: dict[str, Any],
        value_prioritization: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Erstellt Economic Opportunities aus Economic Discovery
        und Value Prioritization.

        Die wirtschaftlichen Werte werden nicht neu berechnet.
        Sie werden ausschließlich aus den vorhandenen Findings
        und der bestehenden Value-Prioritization übernommen.
        """

        if self.status != "running":
            raise RuntimeError(
                "Economic Opportunity ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(economic_discovery, dict):
            raise TypeError(
                "Economic Discovery muss ein Dictionary sein."
            )

        if not isinstance(value_prioritization, dict):
            raise TypeError(
                "Value Prioritization muss ein Dictionary sein."
            )

        self.analysis_count += 1

        economic_findings = economic_discovery.get(
            "findings",
            [],
        )

        prioritized_findings = value_prioritization.get(
            "findings",
            [],
        )

        if not isinstance(economic_findings, list):
            economic_findings = []

        if not isinstance(prioritized_findings, list):
            prioritized_findings = []

        prioritized_by_type: dict[str, dict[str, Any]] = {}

        for finding in prioritized_findings:
            if not isinstance(finding, dict):
                continue

            finding_type = finding.get("type")

            if isinstance(finding_type, str):
                prioritized_by_type[finding_type] = finding

        opportunities: list[dict[str, Any]] = []

        for finding in economic_findings:
            if not isinstance(finding, dict):
                continue

            opportunity = self._build_opportunity(
                finding=finding,
                prioritized_finding=prioritized_by_type.get(
                    finding.get("type")
                ),
            )

            opportunities.append(opportunity)

        opportunities.sort(
            key=lambda item: (
                item["priority_score"] or 0.0,
                item["savings_potential"] or 0.0,
                item["economic_impact"] or 0.0,
            ),
            reverse=True,
        )

        for rank, opportunity in enumerate(
            opportunities,
            start=1,
        ):
            opportunity["rank"] = rank

        critical_count = sum(
            1
            for opportunity in opportunities
            if opportunity["priority"] == "critical"
        )

        high_count = sum(
            1
            for opportunity in opportunities
            if opportunity["priority"] == "high"
        )

        total_economic_impact = self._sum_values(
            opportunities,
            "economic_impact",
        )

        total_savings_potential = self._sum_values(
            opportunities,
            "savings_potential",
        )

        result = {
            "status": "opportunity_analysis_completed",
            "version": self.VERSION,
            "opportunity_count": len(opportunities),
            "critical_count": critical_count,
            "high_count": high_count,
            "total_economic_impact": total_economic_impact,
            "total_savings_potential": total_savings_potential,
            "top_opportunity": (
                opportunities[0]
                if opportunities
                else None
            ),
            "opportunities": opportunities,
        }

        self.last_analysis = result

        return result

    def _build_opportunity(
        self,
        finding: dict[str, Any],
        prioritized_finding: dict[str, Any] | None,
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

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        if prioritized_finding is not None:
            priority_score = self._safe_float(
                prioritized_finding.get(
                    "priority_score"
                )
            )

            value_priority = prioritized_finding.get(
                "value_priority",
                finding.get("priority", "unknown"),
            )

            reason = prioritized_finding.get(
                "reason"
            )

        else:
            priority_score = None
            value_priority = finding.get(
                "priority",
                "unknown",
            )
            reason = None

        if not isinstance(value_priority, str):
            value_priority = "unknown"

        if not isinstance(reason, str):
            reason = self._build_reason(
                savings_potential=savings_potential,
                economic_impact=economic_impact,
                confidence=confidence,
            )

        recommended_action = self._recommended_action(
            finding
        )

        expected_savings = savings_potential

        title = self._build_title(
            finding
        )

        return {
            "opportunity_id": self._build_id(
                finding
            ),
            "type": finding.get("type"),
            "category": finding.get("category"),
            "title": title,
            "problem": finding.get("problem"),
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "expected_savings": expected_savings,
            "confidence": confidence,
            "priority": value_priority,
            "priority_score": priority_score,
            "reason": reason,
            "evidence": finding.get("evidence"),
            "recommended_action": recommended_action,
            "status": "identified",
        }

    @staticmethod
    def _build_id(
        finding: dict[str, Any],
    ) -> str:
        finding_type = finding.get(
            "type",
            "economic",
        )

        return f"economic_opportunity:{finding_type}"

    @staticmethod
    def _build_title(
        finding: dict[str, Any],
    ) -> str:
        finding_type = finding.get(
            "type"
        )

        titles = {
            "procurement_cost": (
                "Procurement Optimization Opportunity"
            ),
            "energy_cost": (
                "Energy Cost Optimization Opportunity"
            ),
            "maintenance_cost": (
                "Maintenance Cost Optimization Opportunity"
            ),
            "inventory_value": (
                "Inventory Optimization Opportunity"
            ),
        }

        return titles.get(
            finding_type,
            "Economic Optimization Opportunity",
        )

    @staticmethod
    def _recommended_action(
        finding: dict[str, Any],
    ) -> str:
        finding_type = finding.get(
            "type"
        )

        actions = {
            "procurement_cost": "review_strategy",
            "energy_cost": "review_strategy",
            "maintenance_cost": "review_strategy",
            "inventory_value": "review_strategy",
        }

        return actions.get(
            finding_type,
            "review_strategy",
        )

    @staticmethod
    def _build_reason(
        savings_potential: float | None,
        economic_impact: float | None,
        confidence: float,
    ) -> str:
        parts: list[str] = []

        if savings_potential is not None:
            parts.append(
                f"Savings Potential: "
                f"{savings_potential:,.2f} EUR"
            )

        if economic_impact is not None:
            parts.append(
                f"Economic Impact: "
                f"{economic_impact:,.2f} EUR"
            )

        parts.append(
            f"Confidence: {confidence:.2f}"
        )

        return " | ".join(parts)

    @staticmethod
    def _sum_values(
        opportunities: list[dict[str, Any]],
        key: str,
    ) -> float | None:
        values = [
            EconomicOpportunity._safe_float(
                opportunity.get(key)
            )
            for opportunity in opportunities
        ]

        valid_values = [
            value
            for value in values
            if value is not None
        ]

        if not valid_values:
            return None

        return round(
            sum(valid_values),
            2,
        )

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        return None
