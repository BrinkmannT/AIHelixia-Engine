"""
AIHelixia Intelligence Engine
Economic Discovery Layer
Version: 0.3.0
"""

from __future__ import annotations

from typing import Any


class EconomicDiscovery:
    """
    Deterministische Economic-Discovery-Schicht.

    Verantwortlichkeiten:
    - wirtschaftliche Auffälligkeiten erkennen
    - Economic Impact berechnen
    - Savings Potential nur bei belastbarer Grundlage ableiten
    - Berechnungen transparent machen
    - Findings strukturiert für die Decision-Schicht bereitstellen

    Unterstützte Analysen:
    - procurement
    - energy
    - maintenance
    - inventory

    Keine LLM-Abhängigkeit.
    Keine externen Aktionen.
    Keine erfundenen wirtschaftlichen Werte.

    Economic Impact, Savings Potential und Realized Savings
    werden strikt voneinander getrennt.
    """

    VERSION = "0.3.0"

    def __init__(self) -> None:
        self.status = "created"
        self.analysis_count = 0
        self.last_analysis: dict[str, Any] | None = None

    def start(self) -> None:
        self.status = "running"

    def stop(self) -> None:
        self.status = "stopped"

    def analyze(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Analysiert wirtschaftliche Auffälligkeiten.

        Unterstützte Bereiche:
        - procurement
        - energy
        - maintenance
        - inventory
        """

        if self.status != "running":
            raise RuntimeError(
                "Economic Discovery ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(data, dict):
            raise TypeError(
                "Economic-Discovery-Daten müssen ein Dictionary sein."
            )

        self.analysis_count += 1

        findings: list[dict[str, Any]] = []

        analyzers = (
            ("procurement", self._analyze_procurement),
            ("energy", self._analyze_energy),
            ("maintenance", self._analyze_maintenance),
            ("inventory", self._analyze_inventory),
        )

        for key, analyzer in analyzers:
            section = data.get(key)

            if isinstance(section, dict):
                finding = analyzer(section)

                if finding is not None:
                    findings.append(finding)

        economic_impacts = [
            self._safe_float(
                finding.get("economic_impact")
            )
            for finding in findings
        ]

        valid_impacts = [
            value
            for value in economic_impacts
            if value is not None
        ]

        total_economic_impact = sum(
            valid_impacts
        )

        savings_values = [
            self._safe_float(
                finding.get("savings_potential")
            )
            for finding in findings
        ]

        valid_savings = [
            value
            for value in savings_values
            if value is not None
        ]

        total_savings_potential = (
            sum(valid_savings)
            if valid_savings
            else None
        )

        critical_count = sum(
            1
            for finding in findings
            if finding.get("priority") == "critical"
        )

        result = {
            "status": "analysis_completed",
            "version": self.VERSION,
            "finding_count": len(findings),
            "critical_count": critical_count,
            "total_economic_impact": total_economic_impact,
            "total_savings_potential": total_savings_potential,
            "findings": findings,
        }

        self.last_analysis = result

        return result

    # =============================================================
    # Procurement
    # =============================================================

    def _analyze_procurement(
        self,
        procurement: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Economic Impact:

            annual_volume
            ×
            (actual_cost - benchmark_cost)

        Savings Potential wird nur berechnet,
        wenn ein explizit validierter realization_factor
        vorhanden ist.
        """

        required_fields = (
            "annual_volume",
            "actual_cost",
            "benchmark_cost",
        )

        if not all(
            field in procurement
            for field in required_fields
        ):
            return {
                "status": "finding_detected",
                "type": "procurement_cost",
                "category": "cost_optimization",
                "problem": (
                    "Für die Beschaffungsanalyse "
                    "liegen nicht alle erforderlichen "
                    "Daten vor."
                ),
                "priority": "unknown",
                "calculation_status": "insufficient_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
                "missing_fields": [
                    field
                    for field in required_fields
                    if field not in procurement
                ],
            }

        try:
            annual_volume = float(
                procurement["annual_volume"]
            )
            actual_cost = float(
                procurement["actual_cost"]
            )
            benchmark_cost = float(
                procurement["benchmark_cost"]
            )
        except (
            TypeError,
            ValueError,
        ):
            return {
                "status": "finding_detected",
                "type": "procurement_cost",
                "category": "cost_optimization",
                "problem": (
                    "Beschaffungsdaten enthalten "
                    "ungültige numerische Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        if (
            annual_volume < 0
            or actual_cost < 0
            or benchmark_cost < 0
        ):
            return {
                "status": "finding_detected",
                "type": "procurement_cost",
                "category": "cost_optimization",
                "problem": (
                    "Beschaffungsdaten enthalten "
                    "negative Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        price_difference = (
            actual_cost - benchmark_cost
        )

        if price_difference <= 0:
            return None

        economic_impact = (
            annual_volume
            * price_difference
        )

        deviation_ratio = (
            price_difference / actual_cost
            if actual_cost > 0
            else 0.0
        )

        priority = self._priority_from_ratio(
            deviation_ratio
        )

        confidence = self._calculate_confidence(
            procurement
        )

        realization_factor = procurement.get(
            "realization_factor"
        )

        savings_potential: float | None = None
        savings_status = "not_estimated"

        if realization_factor is not None:
            try:
                realization_factor = float(
                    realization_factor
                )
            except (
                TypeError,
                ValueError,
            ):
                realization_factor = None

        if (
            realization_factor is not None
            and 0.0 <= realization_factor <= 1.0
        ):
            savings_potential = (
                economic_impact
                * realization_factor
            )
            savings_status = (
                "estimated_from_validated_factor"
            )

        return {
            "status": "finding_detected",
            "type": "procurement_cost",
            "category": "cost_optimization",
            "problem": (
                "Beschaffungskosten liegen oberhalb "
                "des ermittelten Benchmark-Niveaus."
            ),
            "priority": priority,
            "annual_volume": annual_volume,
            "actual_cost": actual_cost,
            "benchmark_cost": benchmark_cost,
            "price_difference": price_difference,
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "savings_status": savings_status,
            "realized_savings": 0.0,
            "confidence": confidence,
            "calculation_status": "calculated",
            "calculation": {
                "economic_impact": (
                    "annual_volume * "
                    "(actual_cost - benchmark_cost)"
                ),
                "deviation_ratio": deviation_ratio,
                "realization_factor": realization_factor,
                "savings_potential": (
                    "economic_impact * "
                    "realization_factor"
                    if realization_factor is not None
                    else None
                ),
            },
            "evidence": {
                "benchmark_source": procurement.get(
                    "benchmark_source"
                ),
                "period": procurement.get(
                    "period"
                ),
                "supplier_count": procurement.get(
                    "supplier_count"
                ),
                "comparable_volume": procurement.get(
                    "comparable_volume"
                ),
                "verified": procurement.get(
                    "verified"
                ),
            },
            "recommendation": (
                "Beschaffungsbedingungen, "
                "Preisstruktur und Volumenstaffeln "
                "überprüfen."
            ),
        }

    # =============================================================
    # Energy
    # =============================================================

    def _analyze_energy(
        self,
        energy: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Economic Impact:

            annual_kwh
            ×
            (actual_cost_per_kwh - benchmark_cost_per_kwh)

        Ein Finding entsteht nur, wenn die tatsächlichen
        Energiekosten oberhalb des Benchmarks liegen.
        """

        required_fields = (
            "annual_kwh",
            "actual_cost_per_kwh",
            "benchmark_cost_per_kwh",
        )

        if not all(
            field in energy
            for field in required_fields
        ):
            return {
                "status": "finding_detected",
                "type": "energy_cost",
                "category": "energy_optimization",
                "problem": (
                    "Für die Energieanalyse "
                    "liegen nicht alle erforderlichen "
                    "Daten vor."
                ),
                "priority": "unknown",
                "calculation_status": "insufficient_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
                "missing_fields": [
                    field
                    for field in required_fields
                    if field not in energy
                ],
            }

        try:
            annual_kwh = float(
                energy["annual_kwh"]
            )
            actual_cost_per_kwh = float(
                energy["actual_cost_per_kwh"]
            )
            benchmark_cost_per_kwh = float(
                energy["benchmark_cost_per_kwh"]
            )
        except (
            TypeError,
            ValueError,
        ):
            return {
                "status": "finding_detected",
                "type": "energy_cost",
                "category": "energy_optimization",
                "problem": (
                    "Energiedaten enthalten "
                    "ungültige numerische Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        if (
            annual_kwh < 0
            or actual_cost_per_kwh < 0
            or benchmark_cost_per_kwh < 0
        ):
            return {
                "status": "finding_detected",
                "type": "energy_cost",
                "category": "energy_optimization",
                "problem": (
                    "Energiedaten enthalten "
                    "negative Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        cost_difference = (
            actual_cost_per_kwh
            - benchmark_cost_per_kwh
        )

        if cost_difference <= 0:
            return None

        economic_impact = (
            annual_kwh
            * cost_difference
        )

        deviation_ratio = (
            cost_difference / actual_cost_per_kwh
            if actual_cost_per_kwh > 0
            else 0.0
        )

        priority = self._priority_from_ratio(
            deviation_ratio
        )

        confidence = self._calculate_confidence(
            energy
        )

        savings_potential, savings_status = (
            self._calculate_validated_savings(
                economic_impact,
                energy,
            )
        )

        return {
            "status": "finding_detected",
            "type": "energy_cost",
            "category": "energy_optimization",
            "problem": (
                "Energiekosten liegen oberhalb "
                "des ermittelten Benchmark-Niveaus."
            ),
            "priority": priority,
            "annual_kwh": annual_kwh,
            "actual_cost_per_kwh": actual_cost_per_kwh,
            "benchmark_cost_per_kwh": (
                benchmark_cost_per_kwh
            ),
            "cost_difference": cost_difference,
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "savings_status": savings_status,
            "realized_savings": 0.0,
            "confidence": confidence,
            "calculation_status": "calculated",
            "calculation": {
                "economic_impact": (
                    "annual_kwh * "
                    "(actual_cost_per_kwh - "
                    "benchmark_cost_per_kwh)"
                ),
                "deviation_ratio": deviation_ratio,
            },
            "evidence": {
                "benchmark_source": energy.get(
                    "benchmark_source"
                ),
                "period": energy.get(
                    "period"
                ),
                "verified": energy.get(
                    "verified"
                ),
            },
            "recommendation": (
                "Energieverbrauch, Tarifstruktur "
                "und operative Energieeffizienz "
                "überprüfen."
            ),
        }

    # =============================================================
    # Maintenance
    # =============================================================

    def _analyze_maintenance(
        self,
        maintenance: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Economic Impact:

            annual_maintenance_cost
            -
            benchmark_maintenance_cost

        Ein positives Ergebnis zeigt höhere
        Instandhaltungskosten als der Vergleichswert.
        """

        required_fields = (
            "annual_maintenance_cost",
            "benchmark_maintenance_cost",
        )

        if not all(
            field in maintenance
            for field in required_fields
        ):
            return {
                "status": "finding_detected",
                "type": "maintenance_cost",
                "category": "maintenance_optimization",
                "problem": (
                    "Für die Instandhaltungsanalyse "
                    "liegen nicht alle erforderlichen "
                    "Daten vor."
                ),
                "priority": "unknown",
                "calculation_status": "insufficient_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
                "missing_fields": [
                    field
                    for field in required_fields
                    if field not in maintenance
                ],
            }

        try:
            annual_cost = float(
                maintenance[
                    "annual_maintenance_cost"
                ]
            )
            benchmark_cost = float(
                maintenance[
                    "benchmark_maintenance_cost"
                ]
            )
        except (
            TypeError,
            ValueError,
        ):
            return {
                "status": "finding_detected",
                "type": "maintenance_cost",
                "category": "maintenance_optimization",
                "problem": (
                    "Instandhaltungsdaten enthalten "
                    "ungültige numerische Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        if (
            annual_cost < 0
            or benchmark_cost < 0
        ):
            return {
                "status": "finding_detected",
                "type": "maintenance_cost",
                "category": "maintenance_optimization",
                "problem": (
                    "Instandhaltungsdaten enthalten "
                    "negative Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        economic_impact = (
            annual_cost
            - benchmark_cost
        )

        if economic_impact <= 0:
            return None

        deviation_ratio = (
            economic_impact / annual_cost
            if annual_cost > 0
            else 0.0
        )

        priority = self._priority_from_ratio(
            deviation_ratio
        )

        confidence = self._calculate_confidence(
            maintenance
        )

        savings_potential, savings_status = (
            self._calculate_validated_savings(
                economic_impact,
                maintenance,
            )
        )

        return {
            "status": "finding_detected",
            "type": "maintenance_cost",
            "category": "maintenance_optimization",
            "problem": (
                "Instandhaltungskosten liegen oberhalb "
                "des ermittelten Benchmark-Niveaus."
            ),
            "priority": priority,
            "annual_maintenance_cost": annual_cost,
            "benchmark_maintenance_cost": benchmark_cost,
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "savings_status": savings_status,
            "realized_savings": 0.0,
            "confidence": confidence,
            "calculation_status": "calculated",
            "calculation": {
                "economic_impact": (
                    "annual_maintenance_cost - "
                    "benchmark_maintenance_cost"
                ),
                "deviation_ratio": deviation_ratio,
            },
            "evidence": {
                "benchmark_source": maintenance.get(
                    "benchmark_source"
                ),
                "period": maintenance.get(
                    "period"
                ),
                "verified": maintenance.get(
                    "verified"
                ),
            },
            "recommendation": (
                "Wartungsintervalle, Reparaturkosten, "
                "Ersatzteilkosten und Instandhaltungsstrategie "
                "überprüfen."
            ),
        }

    # =============================================================
    # Inventory
    # =============================================================

    def _analyze_inventory(
        self,
        inventory: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Economic Impact:

            (average_inventory_value - target_inventory_value)
            ×
            carrying_cost_rate

        Dadurch wird nur dann ein jährlicher wirtschaftlicher
        Impact berechnet, wenn sowohl der überschüssige Bestand
        als auch die jährliche Kapital-/Lagerkostenrate bekannt
        sind.
        """

        required_fields = (
            "average_inventory_value",
            "target_inventory_value",
            "carrying_cost_rate",
        )

        if not all(
            field in inventory
            for field in required_fields
        ):
            return {
                "status": "finding_detected",
                "type": "inventory_carrying_cost",
                "category": "working_capital_optimization",
                "problem": (
                    "Für die Bestandsanalyse "
                    "liegen nicht alle erforderlichen "
                    "Daten vor."
                ),
                "priority": "unknown",
                "calculation_status": "insufficient_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
                "missing_fields": [
                    field
                    for field in required_fields
                    if field not in inventory
                ],
            }

        try:
            average_inventory_value = float(
                inventory["average_inventory_value"]
            )
            target_inventory_value = float(
                inventory["target_inventory_value"]
            )
            carrying_cost_rate = float(
                inventory["carrying_cost_rate"]
            )
        except (
            TypeError,
            ValueError,
        ):
            return {
                "status": "finding_detected",
                "type": "inventory_carrying_cost",
                "category": "working_capital_optimization",
                "problem": (
                    "Bestandsdaten enthalten "
                    "ungültige numerische Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        if (
            average_inventory_value < 0
            or target_inventory_value < 0
            or carrying_cost_rate < 0
            or carrying_cost_rate > 1
        ):
            return {
                "status": "finding_detected",
                "type": "inventory_carrying_cost",
                "category": "working_capital_optimization",
                "problem": (
                    "Bestandsdaten enthalten "
                    "ungültige Werte."
                ),
                "priority": "unknown",
                "calculation_status": "invalid_data",
                "economic_impact": None,
                "savings_potential": None,
                "confidence": 0.0,
            }

        excess_inventory = (
            average_inventory_value
            - target_inventory_value
        )

        if excess_inventory <= 0:
            return None

        economic_impact = (
            excess_inventory
            * carrying_cost_rate
        )

        deviation_ratio = (
            excess_inventory
            / average_inventory_value
            if average_inventory_value > 0
            else 0.0
        )

        priority = self._priority_from_ratio(
            deviation_ratio
        )

        confidence = self._calculate_confidence(
            inventory
        )

        savings_potential, savings_status = (
            self._calculate_validated_savings(
                economic_impact,
                inventory,
            )
        )

        return {
            "status": "finding_detected",
            "type": "inventory_carrying_cost",
            "category": "working_capital_optimization",
            "problem": (
                "Der durchschnittliche Bestand liegt "
                "oberhalb des ermittelten Zielbestands."
            ),
            "priority": priority,
            "average_inventory_value": (
                average_inventory_value
            ),
            "target_inventory_value": (
                target_inventory_value
            ),
            "excess_inventory": excess_inventory,
            "carrying_cost_rate": carrying_cost_rate,
            "economic_impact": economic_impact,
            "savings_potential": savings_potential,
            "savings_status": savings_status,
            "realized_savings": 0.0,
            "confidence": confidence,
            "calculation_status": "calculated",
            "calculation": {
                "economic_impact": (
                    "(average_inventory_value - "
                    "target_inventory_value) * "
                    "carrying_cost_rate"
                ),
                "excess_inventory": excess_inventory,
            },
            "evidence": {
                "benchmark_source": inventory.get(
                    "benchmark_source"
                ),
                "period": inventory.get(
                    "period"
                ),
                "verified": inventory.get(
                    "verified"
                ),
            },
            "recommendation": (
                "Bestandsstruktur, Sicherheitsbestände, "
                "Nachschubparameter und gebundenes Kapital "
                "überprüfen."
            ),
        }

    # =============================================================
    # Shared Helpers
    # =============================================================

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float | None:
        if isinstance(
            value,
            bool,
        ):
            return None

        if isinstance(
            value,
            (int, float),
        ):
            return float(value)

        return None

    @staticmethod
    def _priority_from_ratio(
        deviation_ratio: float,
    ) -> str:
        if deviation_ratio >= 0.10:
            return "critical"

        if deviation_ratio >= 0.05:
            return "high"

        if deviation_ratio >= 0.02:
            return "medium"

        return "low"

    @staticmethod
    def _calculate_confidence(
        data: dict[str, Any],
    ) -> float:
        """
        Deterministische Confidence anhand der vorhandenen Evidenz.

        Die Confidence bewertet die Qualität der Analysegrundlage,
        nicht die tatsächliche Realisierbarkeit einer Einsparung.
        """

        confidence = 70.0

        if data.get(
            "benchmark_source"
        ):
            confidence += 5.0

        if data.get(
            "period"
        ):
            confidence += 5.0

        if data.get(
            "supplier_count"
        ):
            confidence += 5.0

        if data.get(
            "comparable_volume"
        ) is True:
            confidence += 5.0

        if data.get(
            "verified"
        ) is True:
            confidence += 9.0

        return min(
            confidence,
            99.0,
        )

    @classmethod
    def _calculate_validated_savings(
        cls,
        economic_impact: float,
        data: dict[str, Any],
    ) -> tuple[float | None, str]:
        realization_factor = data.get(
            "realization_factor"
        )

        if realization_factor is None:
            return None, "not_estimated"

        try:
            realization_factor = float(
                realization_factor
            )
        except (
            TypeError,
            ValueError,
        ):
            return None, "not_estimated"

        if not (
            0.0
            <= realization_factor
            <= 1.0
        ):
            return None, "not_estimated"

        return (
            economic_impact
            * realization_factor,
            "estimated_from_validated_factor",
        )

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "economic_discovery",
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
            "last_analysis": self.last_analysis,
        }
