"""
AIHelixia Intelligence Engine
Root Cause Analysis Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class RootCause:
    """
    Deterministische Root-Cause-Analyse.

    Die Komponente erzeugt aus Anomalie- und
    Produktionssignalen strukturierte Ursachen-Hypothesen.

    Die Primary Hypothesis wird deterministisch
    anhand der höchsten Priorität ausgewählt.

    Keine Behauptung einer physikalisch validierten Ursache.
    Keine LLM-Abhängigkeit.
    """

    VERSION = "0.2.0"

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

    def _select_primary_hypothesis(
        self,
        hypotheses: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """
        Wählt deterministisch die Hypothese mit
        der höchsten Priorität aus.

        Bei gleicher Priorität bleibt die bestehende
        Reihenfolge der Hypothesen erhalten.
        """

        if not hypotheses:
            return None

        return max(
            hypotheses,
            key=lambda hypothesis: self.PRIORITY_ORDER.get(
                hypothesis.get("priority", "low"),
                0,
            ),
        )

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

        if not isinstance(anomaly_analysis, dict):
            anomaly_analysis = {}

        signals = anomaly_analysis.get(
            "signals",
            [],
        )

        if not isinstance(signals, list):
            signals = []

        signal_types = {
            signal.get("type")
            for signal in signals
            if isinstance(signal, dict)
            and signal.get("type")
        }

        correlated_machines = anomaly_analysis.get(
            "correlated_machines",
            [],
        )

        if not isinstance(
            correlated_machines,
            list,
        ):
            correlated_machines = []

        hypotheses: list[dict[str, Any]] = []

        # ----------------------------------------------------------
        # Thermal / mechanical pattern
        # ----------------------------------------------------------

        thermal_signal = (
            "temperature_elevated"
            in signal_types
        )

        vibration_signal = (
            "vibration_elevated"
            in signal_types
        )

        energy_signal = (
            "energy_increased"
            in signal_types
        )

        production_signal = (
            "production_decreased"
            in signal_types
        )

        if thermal_signal and vibration_signal:

            hypotheses.append({
                "type": "thermal_mechanical_stress",
                "priority": "high",
                "confidence": "medium",
                "machine_ids": correlated_machines,
                "supporting_signals": [
                    "temperature_elevated",
                    "vibration_elevated",
                ],
                "description": (
                    "Die Kombination aus erhöhter "
                    "Temperatur und erhöhter Vibration "
                    "deutet auf ein mögliches thermisch-"
                    "mechanisches Belastungsmuster hin."
                ),
            })

        # ----------------------------------------------------------
        # Energy / efficiency pattern
        # ----------------------------------------------------------

        if energy_signal and production_signal:

            hypotheses.append({
                "type": "energy_efficiency_degradation",
                "priority": "high",
                "confidence": "medium",
                "machine_ids": correlated_machines,
                "supporting_signals": [
                    "energy_increased",
                    "production_decreased",
                ],
                "description": (
                    "Ein erhöhter Energieverbrauch bei "
                    "gleichzeitig reduziertem Produktionsoutput "
                    "deutet auf eine mögliche Verschlechterung "
                    "der betrieblichen Effizienz hin."
                ),
            })

        # ----------------------------------------------------------
        # Multi-signal machine pattern
        # ----------------------------------------------------------

        if (
            thermal_signal
            and vibration_signal
            and energy_signal
            and production_signal
        ):

            hypotheses.append({
                "type": "multi_signal_machine_degradation",
                "priority": "critical",
                "confidence": "medium",
                "machine_ids": correlated_machines,
                "supporting_signals": [
                    "temperature_elevated",
                    "vibration_elevated",
                    "energy_increased",
                    "production_decreased",
                ],
                "description": (
                    "Mehrere gleichzeitig auftretende "
                    "Maschinensignale bilden ein konsistentes "
                    "Muster einer möglichen Maschinen-"
                    "verschlechterung."
                ),
            })

        # ----------------------------------------------------------
        # Critical alarm pattern
        # ----------------------------------------------------------

        if "critical_alarm" in signal_types:

            hypotheses.append({
                "type": "critical_alarm_condition",
                "priority": "critical",
                "confidence": "medium",
                "machine_ids": correlated_machines,
                "supporting_signals": [
                    "critical_alarm",
                ],
                "description": (
                    "Ein kritischer Alarm stellt einen "
                    "direkten Hinweis auf einen relevanten "
                    "industriellen Zustand dar."
                ),
            })

        # ----------------------------------------------------------
        # Result
        # ----------------------------------------------------------

        if not hypotheses:

            result_status = "insufficient_signal"
            primary_hypothesis = None

        else:

            result_status = "hypotheses_generated"

            primary_hypothesis = (
                self._select_primary_hypothesis(
                    hypotheses
                )
            )

        self.analysis_count += 1

        result = {
            "version": self.VERSION,
            "status": result_status,
            "analysis_id": self.analysis_count,
            "hypothesis_count": len(hypotheses),
            "primary_hypothesis": primary_hypothesis,
            "hypotheses": hypotheses,
            "input_signal_types": sorted(
                signal_types
            ),
            "correlated_machines": sorted(
                correlated_machines
            ),
        }

        self.last_analysis = result

        return result

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
