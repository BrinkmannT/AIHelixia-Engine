"""
AIHelixia Intelligence Engine
Prediction Layer
Version: 0.5.0

Responsibilities:
- Analyze current world state
- Use reasoning results
- Generate deterministic future scenarios
- Support generic and industrial FactoryIQ state
- Never confuse observed state with prediction
"""

from __future__ import annotations

from typing import Any


class Prediction:
    VERSION = "0.5.0"

    def __init__(self) -> None:
        self.status = "created"
        self.prediction_count = 0
        self.last_prediction: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> dict[str, Any]:
        self.status = "running"
        return self.get_status()

    def stop(self) -> dict[str, Any]:
        self.status = "stopped"
        return self.get_status()

    # ------------------------------------------------------------------
    # Main prediction
    # ------------------------------------------------------------------

    def predict(
        self,
        world_state: dict[str, Any],
        reasoning: dict[str, Any],
    ) -> dict[str, Any]:

        if self.status != "running":
            raise RuntimeError(
                "Prediction ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(world_state, dict):
            raise TypeError("world_state muss ein Dictionary sein.")

        if not isinstance(reasoning, dict):
            raise TypeError("reasoning muss ein Dictionary sein.")

        self.prediction_count += 1

        scenarios: list[dict[str, Any]] = []

        # --------------------------------------------------------------
        # Generic state
        # --------------------------------------------------------------

        observations = world_state.get("observations", [])
        entities = world_state.get("entities", [])
        conditions = world_state.get("conditions", [])

        observation_count = self._count(observations)
        entity_count = self._count(entities)
        condition_count = self._count(conditions)

        if observation_count > 0:
            scenarios.append({
                "type": "state_persistence",
                "source": "observations",
                "confidence": "medium",
                "description": (
                    "Der beobachtete Zustand kann kurzfristig bestehen bleiben."
                ),
            })

        if entity_count > 0:
            scenarios.append({
                "type": "entity_activity",
                "source": "entities",
                "confidence": "low",
                "description": (
                    "Vorhandene Entitäten können weiterhin aktiv sein."
                ),
            })

        if condition_count > 0:
            scenarios.append({
                "type": "condition_change",
                "source": "conditions",
                "confidence": "low",
                "description": (
                    "Bestehende Bedingungen können sich verändern."
                ),
            })

        # --------------------------------------------------------------
        # Industrial state
        # --------------------------------------------------------------

        industrial_scenarios = self._predict_industrial_state(
            world_state,
            reasoning,
        )

        scenarios.extend(industrial_scenarios)

        # --------------------------------------------------------------
        # Empty state
        # --------------------------------------------------------------

        if not scenarios:
            scenarios.append({
                "type": "no_change",
                "source": "world_state",
                "confidence": "high",
                "description": (
                    "Es liegen noch keine ausreichenden Zustandsdaten "
                    "für ein spezifisches Szenario vor."
                ),
            })

        result = {
            "component": "prediction",
            "version": self.VERSION,
            "status": "predicted",
            "prediction_id": self.prediction_count,
            "scenario_count": len(scenarios),
            "scenarios": scenarios,
        }

        self.last_prediction = result

        return result

    # ------------------------------------------------------------------
    # Industrial prediction
    # ------------------------------------------------------------------

    def _predict_industrial_state(
        self,
        world_state: dict[str, Any],
        reasoning: dict[str, Any],
    ) -> list[dict[str, Any]]:

        scenarios: list[dict[str, Any]] = []

        machines = world_state.get("machines", [])
        alarms = world_state.get("alarms", [])
        production = world_state.get("production", {})
        energy = world_state.get("energy", {})

        industrial_analysis = reasoning.get(
            "industrial_analysis",
            {},
        )

        if not isinstance(industrial_analysis, dict):
            industrial_analysis = {}

        operational_signal = industrial_analysis.get(
            "operational_signal"
        )

        # --------------------------------------------------------------
        # Alarm persistence
        # --------------------------------------------------------------

        if len(alarms) > 0:
            scenarios.append({
                "type": "alarm_persistence",
                "source": "alarms",
                "confidence": "medium",
                "description": (
                    "Der bestehende industrielle Alarmzustand "
                    "kann kurzfristig bestehen bleiben."
                ),
                "alarm_count": len(alarms),
            })

        # --------------------------------------------------------------
        # Machine state
        # --------------------------------------------------------------

        if len(machines) > 0:

            running_count = 0
            stopped_count = 0
            warning_count = 0

            for machine in machines:

                if not isinstance(machine, dict):
                    continue

                status = str(
                    machine.get("status", "")
                ).lower()

                if status == "running":
                    running_count += 1

                elif status in {
                    "stopped",
                    "offline",
                    "down",
                }:
                    stopped_count += 1

                elif status in {
                    "warning",
                    "degraded",
                }:
                    warning_count += 1

            if running_count > 0:
                scenarios.append({
                    "type": "machine_state_persistence",
                    "source": "machines",
                    "confidence": "medium",
                    "description": (
                        "Laufende Maschinen können ihren aktuellen "
                        "Betriebszustand kurzfristig beibehalten."
                    ),
                    "running_machine_count": running_count,
                })

            if stopped_count > 0:
                scenarios.append({
                    "type": "machine_downtime_persistence",
                    "source": "machines",
                    "confidence": "medium",
                    "description": (
                        "Ein erkannter Maschinenstillstand kann "
                        "kurzfristig bestehen bleiben."
                    ),
                    "stopped_machine_count": stopped_count,
                })

            if warning_count > 0:
                scenarios.append({
                    "type": "machine_warning_persistence",
                    "source": "machines",
                    "confidence": "medium",
                    "description": (
                        "Ein erkannter Maschinen-Warnzustand kann "
                        "kurzfristig bestehen bleiben."
                    ),
                    "warning_machine_count": warning_count,
                })

        # --------------------------------------------------------------
        # Operational signal
        # --------------------------------------------------------------

        if operational_signal == "critical_alarm":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "confidence": "medium",
                "priority": "high",
                "description": (
                    "Der erkannte kritische Alarmzustand weist auf "
                    "ein erhöhtes operatives Risiko hin."
                ),
            })

        elif operational_signal == "machine_stop_detected":

            scenarios.append({
                "type": "potential_production_impact",
                "source": "industrial_analysis",
                "confidence": "medium",
                "priority": "high",
                "description": (
                    "Ein erkannter Maschinenstillstand kann "
                    "Auswirkungen auf die Produktion haben."
                ),
            })

        elif operational_signal == "machine_warning":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "confidence": "low",
                "priority": "medium",
                "description": (
                    "Ein Maschinen-Warnzustand kann auf ein "
                    "zunehmendes operatives Risiko hinweisen."
                ),
            })

        elif operational_signal == "warning_alarm":

            scenarios.append({
                "type": "potential_machine_risk",
                "source": "industrial_analysis",
                "confidence": "low",
                "priority": "medium",
                "description": (
                    "Ein Warnalarm kann auf eine mögliche "
                    "Verschlechterung des Maschinenzustands hinweisen."
                ),
            })

        # --------------------------------------------------------------
        # Production
        # --------------------------------------------------------------

        if production:

            scenarios.append({
                "type": "production_state_persistence",
                "source": "production",
                "confidence": "low",
                "description": (
                    "Der aktuelle Produktionszustand kann "
                    "kurzfristig bestehen bleiben."
                ),
            })

        # --------------------------------------------------------------
        # Energy
        # --------------------------------------------------------------

        if energy:

            scenarios.append({
                "type": "energy_state_persistence",
                "source": "energy",
                "confidence": "low",
                "description": (
                    "Der aktuelle Energiezustand kann "
                    "kurzfristig bestehen bleiben."
                ),
            })

        return scenarios

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _count(value: Any) -> int:

        if value is None:
            return 0

        if isinstance(value, (list, tuple, set, dict)):
            return len(value)

        return 1

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict[str, Any]:

        return {
            "component": "prediction",
            "version": self.VERSION,
            "status": self.status,
            "prediction_count": self.prediction_count,
            "last_prediction_id": (
                self.last_prediction.get("prediction_id")
                if self.last_prediction
                else None
            ),
        }
