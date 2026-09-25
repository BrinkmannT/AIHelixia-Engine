"""
AIHelixia Intelligence Engine
Prediction Layer
Version: 0.6.0
"""

from __future__ import annotations

from typing import Any


class Prediction:
    """
    Deterministische Prediction-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - aktuellen World State analysieren
    - Reasoning-Ergebnis berücksichtigen
    - industrielle Anomalien berücksichtigen
    - zukünftige Szenarien deterministisch erzeugen
    - beobachteten Zustand klar von einer Prediction trennen

    Keine Behauptung realer Ausfallwahrscheinlichkeiten.
    Keine LLM-Abhängigkeit.
    """

    VERSION = "0.6.0"

    def __init__(self) -> None:
        self.status = "created"
        self.prediction_count = 0
        self.last_prediction: dict[str, Any] | None = None

    def start(self) -> None:
        self.status = "running"

    def stop(self) -> None:
        self.status = "stopped"

    def predict(
        self,
        world_state: dict[str, Any],
        reasoning: dict[str, Any],
    ) -> dict[str, Any]:

        if self.status != "running":
            raise RuntimeError(
                "Prediction ist nicht gestartet."
            )

        if not isinstance(world_state, dict):
            raise TypeError(
                "world_state must be a dictionary"
            )

        if not isinstance(reasoning, dict):
            raise TypeError(
                "reasoning must be a dictionary"
            )

        scenarios: list[dict[str, Any]] = []

        observations = world_state.get(
            "observations",
            [],
        )

        entities = world_state.get(
            "entities",
            [],
        )

        conditions = world_state.get(
            "conditions",
            [],
        )

        scenarios.extend(
            self._predict_generic_state(
                observations=observations,
                entities=entities,
                conditions=conditions,
            )
        )

        scenarios.extend(
            self._predict_industrial_state(
                world_state=world_state,
                reasoning=reasoning,
            )
        )

        self.prediction_count += 1

        result = {
            "version": self.VERSION,
            "status": "prediction_completed",
            "prediction_id": self.prediction_count,
            "scenario_count": len(scenarios),
            "scenarios": scenarios,
        }

        self.last_prediction = result

        return result

    def _predict_generic_state(
        self,
        observations: Any,
        entities: Any,
        conditions: Any,
    ) -> list[dict[str, Any]]:

        scenarios: list[dict[str, Any]] = []

        observation_count = self._count(
            observations
        )

        entity_count = self._count(
            entities
        )

        condition_count = self._count(
            conditions
        )

        if observation_count > 0:

            scenarios.append({
                "type": "observation_persistence",
                "source": "observations",
                "priority": "low",
                "confidence": "low",
                "description": (
                    "Der aktuelle Beobachtungszustand "
                    "kann kurzfristig bestehen bleiben."
                ),
            })

        if entity_count > 0:

            scenarios.append({
                "type": "entity_state_persistence",
                "source": "entities",
                "priority": "low",
                "confidence": "low",
                "description": (
                    "Der aktuelle Zustand der erkannten "
                    "Entitäten kann kurzfristig bestehen bleiben."
                ),
            })

        if condition_count > 0:

            scenarios.append({
                "type": "condition_persistence",
                "source": "conditions",
                "priority": "low",
                "confidence": "low",
                "description": (
                    "Die aktuelle Bedingung kann "
                    "kurzfristig bestehen bleiben."
                ),
            })

        return scenarios

    def _predict_industrial_state(
        self,
        world_state: dict[str, Any],
        reasoning: dict[str, Any],
    ) -> list[dict[str, Any]]:

        scenarios: list[dict[str, Any]] = []

        machines = world_state.get(
            "machines",
            [],
        )

        alarms = world_state.get(
            "alarms",
            [],
        )

        production = world_state.get(
            "production",
        )

        energy = world_state.get(
            "energy",
        )

        industrial_analysis = reasoning.get(
            "industrial_analysis",
            {},
        )

        anomaly_analysis = reasoning.get(
            "anomaly_analysis",
            {},
        )

        operational_signal = industrial_analysis.get(
            "operational_signal"
        )

        anomaly_status = anomaly_analysis.get(
            "status"
        )

        anomaly_severity = anomaly_analysis.get(
            "severity"
        )

        anomaly_signals = anomaly_analysis.get(
            "signals",
            [],
        )

        correlated_machines = anomaly_analysis.get(
            "correlated_machines",
            [],
        )

        # ----------------------------------------------------------
        # Existing alarm persistence
        # ----------------------------------------------------------

        if alarms:

            scenarios.append({
                "type": "alarm_persistence",
                "source": "alarms",
                "priority": "medium",
                "confidence": "medium",
                "description": (
                    "Der aktuelle Alarmzustand kann "
                    "kurzfristig bestehen bleiben."
                ),
            })

        # ----------------------------------------------------------
        # Existing machine state persistence
        # ----------------------------------------------------------

        for machine in machines:

            if not isinstance(machine, dict):
                continue

            machine_id = machine.get(
                "id"
            )

            status = str(
                machine.get(
                    "status",
                    ""
                )
            ).lower()

            if not machine_id:
                continue

            if status == "running":

                scenarios.append({
                    "type": "machine_state_persistence",
                    "source": "machine",
                    "machine_id": machine_id,
                    "priority": "low",
                    "confidence": "high",
                    "description": (
                        "Der aktuelle laufende "
                        "Maschinenzustand kann "
                        "kurzfristig bestehen bleiben."
                    ),
                })

            elif status in {
                "stopped",
                "offline",
                "down",
            }:

                scenarios.append({
                    "type": "machine_downtime_persistence",
                    "source": "machine",
                    "machine_id": machine_id,
                    "priority": "high",
                    "confidence": "medium",
                    "description": (
                        "Der aktuelle Stillstands- oder "
                        "Offline-Zustand kann "
                        "kurzfristig bestehen bleiben."
                    ),
                })

            elif status in {
                "warning",
                "degraded",
            }:

                scenarios.append({
                    "type": "machine_warning_persistence",
                    "source": "machine",
                    "machine_id": machine_id,
                    "priority": "medium",
                    "confidence": "medium",
                    "description": (
                        "Der aktuelle Warn- oder "
                        "Degradationszustand kann "
                        "kurzfristig bestehen bleiben."
                    ),
                })

        # ----------------------------------------------------------
        # Operational signal
        # ----------------------------------------------------------

        if operational_signal == "critical_alarm":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "priority": "high",
                "confidence": "medium",
                "description": (
                    "Der aktuelle kritische Alarmzustand "
                    "kann auf ein erhöhtes Maschinenrisiko "
                    "hindeuten."
                ),
            })

        elif operational_signal == "machine_stop_detected":

            scenarios.append({
                "type": "potential_production_impact",
                "source": "industrial_analysis",
                "priority": "high",
                "confidence": "medium",
                "description": (
                    "Der erkannte Maschinenstillstand "
                    "kann kurzfristig die Produktion "
                    "beeinträchtigen."
                ),
            })

        elif operational_signal == "machine_warning":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "priority": "medium",
                "confidence": "low",
                "description": (
                    "Der aktuelle Maschinenwarnzustand "
                    "kann auf ein erhöhtes Maschinenrisiko "
                    "hindeuten."
                ),
            })

        elif operational_signal == "warning_alarm":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "priority": "medium",
                "confidence": "low",
                "description": (
                    "Der aktuelle Warnalarm kann "
                    "kurzfristig bestehen bleiben."
                ),
            })

        # ----------------------------------------------------------
        # NEW: anomaly-driven prediction
        # ----------------------------------------------------------

        if anomaly_status in {
            "anomaly_signal",
            "anomaly_detected",
        }:

            signal_types = [
                signal.get("type")
                for signal in anomaly_signals
                if isinstance(signal, dict)
                and signal.get("type")
            ]

            # Single anomaly signal
            if anomaly_status == "anomaly_signal":

                scenarios.append({
                    "type": "potential_anomaly_persistence",
                    "source": "anomaly_analysis",
                    "priority": "medium",
                    "confidence": "low",
                    "severity": anomaly_severity,
                    "trigger_signals": signal_types,
                    "description": (
                        "Das erkannte Anomaliesignal "
                        "kann kurzfristig bestehen bleiben "
                        "und sollte weiter beobachtet werden."
                    ),
                })

            # Correlated anomaly
            if correlated_machines:

                for machine_id in correlated_machines:

                    scenarios.append({
                        "type": "potential_machine_degradation",
                        "source": "anomaly_analysis",
                        "machine_id": machine_id,
                        "priority": "high",
                        "confidence": "medium",
                        "severity": anomaly_severity,
                        "trigger_signals": signal_types,
                        "description": (
                            "Die Kombination mehrerer "
                            "korrelierter Anomaliesignale "
                            "kann auf eine mögliche weitere "
                            "Maschinenverschlechterung "
                            "hindeuten."
                        ),
                    })

            # Production impact
            if (
                "production_decreased"
                in signal_types
            ):

                scenarios.append({
                    "type": "potential_production_impact",
                    "source": "anomaly_analysis",
                    "priority": "high",
                    "confidence": "medium",
                    "trigger_signals": signal_types,
                    "description": (
                        "Die erkannte Produktionsabweichung "
                        "kann kurzfristig zu einer weiteren "
                        "Beeinträchtigung des Produktionsoutputs "
                        "führen."
                    ),
                })

            # Energy impact
            if (
                "energy_increased"
                in signal_types
            ):

                scenarios.append({
                    "type": "potential_energy_persistence",
                    "source": "anomaly_analysis",
                    "priority": "medium",
                    "confidence": "medium",
                    "trigger_signals": signal_types,
                    "description": (
                        "Der erhöhte Energieverbrauch "
                        "kann kurzfristig bestehen bleiben."
                    ),
                })

        # ----------------------------------------------------------
        # Production state
        # ----------------------------------------------------------

        if production:

            scenarios.append({
                "type": "production_state_persistence",
                "source": "production",
                "priority": "low",
                "confidence": "low",
                "description": (
                    "Der aktuelle Produktionszustand "
                    "kann kurzfristig bestehen bleiben."
                ),
            })

        # ----------------------------------------------------------
        # Energy state
        # ----------------------------------------------------------

        if energy:

            scenarios.append({
                "type": "energy_state_persistence",
                "source": "energy",
                "priority": "low",
                "confidence": "low",
                "description": (
                    "Der aktuelle Energiezustand "
                    "kann kurzfristig bestehen bleiben."
                ),
            })

        return scenarios

    @staticmethod
    def _count(
        value: Any,
    ) -> int:

        if value is None:
            return 0

        if isinstance(
            value,
            (
                list,
                tuple,
                set,
                dict,
            ),
        ):
            return len(value)

        return 1

    def get_status(
        self,
    ) -> dict[str, Any]:

        return {
            "component": "prediction",
            "version": self.VERSION,
            "status": self.status,
            "prediction_count": self.prediction_count,
            "last_prediction_id": (
                self.last_prediction.get(
                    "prediction_id"
                )
                if self.last_prediction
                else None
            ),
        }
