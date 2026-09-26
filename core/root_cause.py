"""
AIHelixia Intelligence Engine
Root Cause Analysis Layer
Version: 0.3.0
"""

from __future__ import annotations

from typing import Any


class RootCause:
    """
    Deterministische Root-Cause-Analyse.

    Verantwortlichkeiten:
    - Reasoning-Anomalien auswerten
    - Prediction-Ergebnisse auswerten
    - mögliche Ursachenhypothesen erzeugen
    - Evidence strukturiert an Hypothesen binden
    - qualitative Confidence ableiten
    - primäre Hypothese bestimmen

    Die Komponente behauptet keine physikalisch validierte Ursache.
    Hypothesen müssen anhand der verfügbaren Evidenz interpretiert
    und später mit realen Daten validiert werden.
    """

    VERSION = "0.3.0"

    PRIORITY_ORDER = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }

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
        reasoning: dict[str, Any],
        prediction: dict[str, Any],
    ) -> dict[str, Any]:

        if self.status != "running":
            raise RuntimeError(
                "RootCause ist nicht gestartet."
            )

        if not isinstance(reasoning, dict):
            raise TypeError(
                "reasoning must be a dictionary"
            )

        if not isinstance(prediction, dict):
            raise TypeError(
                "prediction must be a dictionary"
            )

        anomaly_analysis = reasoning.get(
            "anomaly_analysis",
            {},
        )

        if not isinstance(
            anomaly_analysis,
            dict,
        ):
            anomaly_analysis = {}

        anomaly_status = anomaly_analysis.get(
            "status"
        )

        anomaly_severity = anomaly_analysis.get(
            "severity"
        )

        signals = anomaly_analysis.get(
            "signals",
            [],
        )

        if not isinstance(
            signals,
            list,
        ):
            signals = []

        correlated_machines = anomaly_analysis.get(
            "correlated_machines",
            [],
        )

        if not isinstance(
            correlated_machines,
            list,
        ):
            correlated_machines = [
                correlated_machines
            ] if correlated_machines else []

        signal_types = [
            signal.get("type")
            for signal in signals
            if isinstance(signal, dict)
            and signal.get("type")
        ]

        prediction_scenarios = prediction.get(
            "scenarios",
            [],
        )

        if not isinstance(
            prediction_scenarios,
            list,
        ):
            prediction_scenarios = []

        historical_support = reasoning.get(
            "historical_outcome_analysis",
            {},
        )

        if not isinstance(
            historical_support,
            dict,
        ):
            historical_support = {}

        hypotheses: list[dict[str, Any]] = []

        # ----------------------------------------------------------
        # Thermal + mechanical signal combination
        # ----------------------------------------------------------

        has_temperature = (
            "temperature_elevated"
            in signal_types
        )

        has_vibration = (
            "vibration_elevated"
            in signal_types
        )

        has_energy = (
            "energy_increased"
            in signal_types
        )

        has_production = (
            "production_decreased"
            in signal_types
        )

        if (
            has_temperature
            and has_vibration
        ):

            hypotheses.append(
                self._build_hypothesis(
                    hypothesis_type=(
                        "thermal_mechanical_stress"
                    ),
                    priority="high",
                    confidence="medium",
                    description=(
                        "Die Kombination aus erhöhter "
                        "Temperatur und erhöhter Vibration "
                        "kann auf eine thermisch-mechanische "
                        "Belastung hindeuten."
                    ),
                    signal_types=signal_types,
                    correlated_machines=(
                        correlated_machines
                    ),
                    prediction_scenarios=(
                        prediction_scenarios
                    ),
                    historical_support=(
                        historical_support
                    ),
                )
            )

        # ----------------------------------------------------------
        # Energy + production signal combination
        # ----------------------------------------------------------

        if (
            has_energy
            and has_production
        ):

            hypotheses.append(
                self._build_hypothesis(
                    hypothesis_type=(
                        "energy_efficiency_degradation"
                    ),
                    priority="high",
                    confidence="medium",
                    description=(
                        "Die Kombination aus erhöhtem "
                        "Energieverbrauch und reduzierter "
                        "Produktion kann auf eine mögliche "
                        "Verschlechterung der Energieeffizienz "
                        "hindeuten."
                    ),
                    signal_types=signal_types,
                    correlated_machines=(
                        correlated_machines
                    ),
                    prediction_scenarios=(
                        prediction_scenarios
                    ),
                    historical_support=(
                        historical_support
                    ),
                )
            )

        # ----------------------------------------------------------
        # Multi-signal degradation
        # ----------------------------------------------------------

        if (
            has_temperature
            and has_vibration
            and has_energy
            and has_production
        ):

            hypotheses.append(
                self._build_hypothesis(
                    hypothesis_type=(
                        "multi_signal_machine_degradation"
                    ),
                    priority="critical",
                    confidence="medium",
                    description=(
                        "Die Kombination mehrerer "
                        "korrelierter Betriebsabweichungen "
                        "kann auf eine mögliche "
                        "Maschinendegradation hindeuten."
                    ),
                    signal_types=signal_types,
                    correlated_machines=(
                        correlated_machines
                    ),
                    prediction_scenarios=(
                        prediction_scenarios
                    ),
                    historical_support=(
                        historical_support
                    ),
                )
            )

        # ----------------------------------------------------------
        # Critical alarm
        # ----------------------------------------------------------

        if anomaly_status == "critical_alarm":

            hypotheses.append(
                self._build_hypothesis(
                    hypothesis_type=(
                        "critical_alarm_condition"
                    ),
                    priority="critical",
                    confidence="medium",
                    description=(
                        "Der kritische Alarmzustand "
                        "erfordert eine weitere Untersuchung "
                        "der zugrunde liegenden Ursache."
                    ),
                    signal_types=signal_types,
                    correlated_machines=(
                        correlated_machines
                    ),
                    prediction_scenarios=(
                        prediction_scenarios
                    ),
                    historical_support=(
                        historical_support
                    ),
                )
            )

        # ----------------------------------------------------------
        # Fallback
        # ----------------------------------------------------------

        if not hypotheses:

            hypotheses.append(
                self._build_hypothesis(
                    hypothesis_type="insufficient_signal",
                    priority="low",
                    confidence="low",
                    description=(
                        "Es liegen nicht genügend "
                        "korrelierte Signale für eine "
                        "spezifische Root-Cause-Hypothese vor."
                    ),
                    signal_types=signal_types,
                    correlated_machines=(
                        correlated_machines
                    ),
                    prediction_scenarios=(
                        prediction_scenarios
                    ),
                    historical_support=(
                        historical_support
                    ),
                )
            )

        primary_hypothesis = (
            self._select_primary_hypothesis(
                hypotheses
            )
        )

        self.analysis_count += 1

        result = {
            "version": self.VERSION,
            "status": "analysis_completed",
            "analysis_id": self.analysis_count,
            "hypothesis_count": len(hypotheses),
            "primary_hypothesis": primary_hypothesis,
            "hypotheses": hypotheses,
            "input_signal_types": signal_types,
            "correlated_machines": correlated_machines,
        }

        self.last_analysis = result

        return result

    def _build_hypothesis(
        self,
        hypothesis_type: str,
        priority: str,
        confidence: str,
        description: str,
        signal_types: list[str],
        correlated_machines: list[Any],
        prediction_scenarios: list[dict[str, Any]],
        historical_support: dict[str, Any],
    ) -> dict[str, Any]:

        supporting_predictions = []

        for scenario in prediction_scenarios:

            if not isinstance(
                scenario,
                dict,
            ):
                continue

            scenario_type = scenario.get(
                "type"
            )

            if scenario_type in {
                "potential_machine_degradation",
                "potential_energy_persistence",
                "potential_production_impact",
                "potential_anomaly_persistence",
                "machine_state_persistence",
            }:
                supporting_predictions.append(
                    scenario_type
                )

        supporting_predictions = list(
            dict.fromkeys(
                supporting_predictions
            )
        )

        evidence = self._build_evidence(
            signal_types=signal_types,
            correlated_machines=(
                correlated_machines
            ),
            supporting_predictions=(
                supporting_predictions
            ),
            historical_support=(
                historical_support
            ),
        )

        confidence_factors = []

        if signal_types:
            confidence_factors.append(
                "supporting_signals_available"
            )

        if correlated_machines:
            confidence_factors.append(
                "correlated_machine_available"
            )

        if supporting_predictions:
            confidence_factors.append(
                "prediction_support_available"
            )

        historical_outcome_count = (
            historical_support.get(
                "known_outcome_count",
                0,
            )
        )

        historical_confidence = (
            historical_support.get(
                "average_confidence"
            )
        )

        if (
            historical_outcome_count > 0
            and historical_confidence is not None
        ):
            confidence_factors.append(
                "historical_support_available"
            )

        return {
            "type": hypothesis_type,
            "priority": priority,
            "confidence": confidence,
            "description": description,
            "evidence": evidence,
            "confidence_factors": (
                confidence_factors
            ),
        }

    @staticmethod
    def _build_evidence(
        signal_types: list[str],
        correlated_machines: list[Any],
        supporting_predictions: list[str],
        historical_support: dict[str, Any],
    ) -> dict[str, Any]:

        known_outcome_count = (
            historical_support.get(
                "known_outcome_count",
                0,
            )
        )

        average_confidence = (
            historical_support.get(
                "average_confidence"
            )
        )

        dominant_outcome = (
            historical_support.get(
                "dominant_outcome"
            )
        )

        historical_available = (
            known_outcome_count > 0
            and average_confidence is not None
        )

        evidence_count = (
            len(signal_types)
            + len(correlated_machines)
            + len(supporting_predictions)
        )

        if historical_available:
            evidence_count += 1

        if evidence_count >= 5:
            evidence_strength = "strong"

        elif evidence_count >= 3:
            evidence_strength = "moderate"

        elif evidence_count >= 1:
            evidence_strength = "limited"

        else:
            evidence_strength = "none"

        return {
            "evidence_count": evidence_count,
            "supporting_signals": signal_types,
            "correlated_machines": (
                correlated_machines
            ),
            "supporting_predictions": (
                supporting_predictions
            ),
            "historical_support": (
                historical_support
                if historical_available
                else "not_available"
            ),
            "historical_evidence_available": (
                historical_available
            ),
            "historical_outcome_count": (
                known_outcome_count
            ),
            "historical_average_confidence": (
                average_confidence
            ),
            "historical_dominant_outcome": (
                dominant_outcome
            ),
            "evidence_strength": evidence_strength,
        }

    def _select_primary_hypothesis(
        self,
        hypotheses: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not hypotheses:
            return {}

        return max(
            hypotheses,
            key=lambda hypothesis: self.PRIORITY_ORDER.get(
                hypothesis.get(
                    "priority",
                    "low",
                ),
                0,
            ),
        )

    def get_status(
        self,
    ) -> dict[str, Any]:

        return {
            "component": "root_cause",
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
            "last_analysis_id": (
                self.last_analysis.get(
                    "analysis_id"
                )
                if self.last_analysis
                else None
            ),
        }
