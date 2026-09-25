"""
AIHelixia Intelligence Engine
Reasoning Layer
Version: 0.7.0
"""

from __future__ import annotations

from typing import Any


class Reasoning:
    VERSION = "0.7.0"

    def __init__(self):
        self.status = "created"
        self.analysis_count = 0
        self.last_analysis: dict[str, Any] | None = None

    def start(self):
        self.status = "running"
        return self.get_status()

    def stop(self):
        self.status = "stopped"
        return self.get_status()

    def analyze(
        self,
        world_state: dict[str, Any],
        memory: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        if not isinstance(world_state, dict):
            raise TypeError("world_state must be a dictionary")

        memory_entries = memory if isinstance(memory, list) else []

        observations = world_state.get("observations", [])
        entities = world_state.get("entities", [])
        conditions = world_state.get("conditions", [])

        industrial_fields = {
            "factory": world_state.get("factory"),
            "production_lines": world_state.get("production_lines", []),
            "machines": world_state.get("machines", []),
            "sensors": world_state.get("sensors", []),
            "production": world_state.get("production"),
            "energy": world_state.get("energy"),
            "maintenance": world_state.get("maintenance"),
            "alarms": world_state.get("alarms", []),
        }

        state_assessment = self._assess_state(
            observations,
            entities,
            conditions,
            industrial_fields,
        )

        memory_analysis = self._analyze_memory(memory_entries)

        historical_memory_analysis = self._analyze_historical_memory(
            memory_entries
        )

        feedback_analysis = self._analyze_feedback(
            memory_entries
        )

        learning_signal = self._build_learning_signal(
            feedback_analysis,
            historical_memory_analysis,
        )

        industrial_analysis = self._analyze_industrial_state(
            industrial_fields
        )

        anomaly_analysis = self._analyze_anomalies(
            industrial_fields
        )

        conclusions = self._build_conclusions(
            state_assessment,
            memory_analysis,
            historical_memory_analysis,
            feedback_analysis,
            learning_signal,
            industrial_analysis,
            anomaly_analysis,
        )

        self.analysis_count += 1

        result = {
            "version": self.VERSION,
            "status": "analysis_completed",
            "analysis_id": self.analysis_count,
            "state_assessment": state_assessment,
            "memory_analysis": memory_analysis,
            "historical_memory_analysis": historical_memory_analysis,
            "feedback_analysis": feedback_analysis,
            "learning_signal": learning_signal,
            "industrial_analysis": industrial_analysis,
            "anomaly_analysis": anomaly_analysis,
            "conclusions": conclusions,
        }

        self.last_analysis = result

        return result

    def _assess_state(
        self,
        observations: Any,
        entities: Any,
        conditions: Any,
        industrial_fields: dict[str, Any],
    ) -> dict[str, Any]:

        assessment: dict[str, Any] = {}

        assessment["observations"] = {
            "status": (
                "observations_available"
                if observations
                else "no_observations"
            ),
            "count": len(observations),
        }

        assessment["entities"] = {
            "status": (
                "entities_available"
                if entities
                else "no_entities"
            ),
            "count": len(entities),
        }

        assessment["conditions"] = {
            "status": (
                "conditions_available"
                if conditions
                else "no_conditions"
            ),
            "count": len(conditions),
        }

        if industrial_fields["alarms"]:
            assessment["industrial_alarms"] = {
                "status": "industrial_alarm_state",
                "count": len(industrial_fields["alarms"]),
            }

        if industrial_fields["machines"]:
            assessment["industrial_machines"] = {
                "status": "industrial_machine_state",
                "count": len(industrial_fields["machines"]),
            }

        if industrial_fields["production"] is not None:
            assessment["industrial_production"] = {
                "status": "industrial_production_state"
            }

        if any(
            value not in (None, [], {})
            for value in industrial_fields.values()
        ):
            assessment["industrial_state"] = {
                "status": "industrial_state_available"
            }

        return assessment

    def _analyze_memory(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not memory_entries:
            return {
                "status": "no_memory",
                "entry_count": 0,
                "types": {},
            }

        type_counts: dict[str, int] = {}

        for entry in memory_entries:

            if not isinstance(entry, dict):
                continue

            memory_type = entry.get("type", "unknown")

            type_counts[memory_type] = (
                type_counts.get(memory_type, 0) + 1
            )

        return {
            "status": "memory_available",
            "entry_count": len(memory_entries),
            "types": type_counts,
        }

    def _analyze_historical_memory(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not memory_entries:
            return {
                "status": "no_historical_memory",
                "entry_count": 0,
                "type_counts": {},
                "machine_counts": {},
                "status_counts": {},
                "action_counts": {},
                "recurring_machine_ids": [],
            }

        type_counts: dict[str, int] = {}
        machine_counts: dict[str, int] = {}
        status_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}

        for entry in memory_entries:

            if not isinstance(entry, dict):
                continue

            memory_type = entry.get("type", "unknown")

            type_counts[memory_type] = (
                type_counts.get(memory_type, 0) + 1
            )

            data = entry.get("data", {})

            if not isinstance(data, dict):
                data = {}

            machine_id = data.get("machine_id")

            if machine_id:
                machine_counts[machine_id] = (
                    machine_counts.get(machine_id, 0) + 1
                )

            machines = data.get("machines", [])

            if isinstance(machines, list):

                for machine in machines:

                    if not isinstance(machine, dict):
                        continue

                    nested_machine_id = machine.get("id")

                    if nested_machine_id:
                        machine_counts[nested_machine_id] = (
                            machine_counts.get(
                                nested_machine_id,
                                0,
                            ) + 1
                        )

                    nested_status = machine.get("status")

                    if nested_status:
                        status_counts[nested_status] = (
                            status_counts.get(
                                nested_status,
                                0,
                            ) + 1
                        )

            status = data.get("status")

            if status:
                status_counts[status] = (
                    status_counts.get(status, 0) + 1
                )

            action = data.get("action")

            if action:
                action_counts[action] = (
                    action_counts.get(action, 0) + 1
                )

        recurring_machine_ids = sorted(
            machine_id
            for machine_id, count in machine_counts.items()
            if count > 1
        )

        return {
            "status": "historical_memory_available",
            "entry_count": len(memory_entries),
            "type_counts": type_counts,
            "machine_counts": machine_counts,
            "status_counts": status_counts,
            "action_counts": action_counts,
            "recurring_machine_ids": recurring_machine_ids,
        }

    def _analyze_feedback(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        feedback_entries = [
            entry
            for entry in memory_entries
            if isinstance(entry, dict)
            and entry.get("type") == "feedback"
        ]

        if not feedback_entries:
            return {
                "status": "no_feedback",
                "count": 0,
                "reinforce_count": 0,
                "adjust_count": 0,
                "review_count": 0,
                "average_score": None,
            }

        reinforce_count = 0
        adjust_count = 0
        review_count = 0
        scores: list[float] = []

        for entry in feedback_entries:

            data = entry.get("data", {})

            if not isinstance(data, dict):
                data = {}

            signal = data.get("signal")

            if signal is None:
                signal = data.get("action")

            if signal == "reinforce":
                reinforce_count += 1

            elif signal == "adjust":
                adjust_count += 1

            elif signal == "review":
                review_count += 1

            score = data.get("score")

            if isinstance(score, (int, float)):
                scores.append(float(score))

        if adjust_count > 0:
            status = "adjustment_required"
        elif reinforce_count > 0:
            status = "positive_history"
        else:
            status = "feedback_available"

        average_score = (
            sum(scores) / len(scores)
            if scores
            else None
        )

        return {
            "status": status,
            "count": len(feedback_entries),
            "reinforce_count": reinforce_count,
            "adjust_count": adjust_count,
            "review_count": review_count,
            "average_score": average_score,
        }

    def _build_learning_signal(
        self,
        feedback_analysis: dict[str, Any],
        historical_memory_analysis: dict[str, Any],
    ) -> dict[str, Any]:

        if feedback_analysis["status"] == "adjustment_required":

            return {
                "action": "adjust",
                "priority": "high",
                "reason": (
                    "historical feedback indicates "
                    "adjustment is required"
                ),
            }

        if feedback_analysis["status"] == "positive_history":

            return {
                "action": "reinforce",
                "priority": "normal",
                "reason": (
                    "historical feedback contains "
                    "positive signals"
                ),
            }

        recurring_machine_ids = historical_memory_analysis.get(
            "recurring_machine_ids",
            [],
        )

        if recurring_machine_ids:

            return {
                "action": "review",
                "priority": "normal",
                "reason": (
                    "recurring historical machine "
                    "events detected"
                ),
                "machine_ids": recurring_machine_ids,
            }

        return {
            "action": "review",
            "priority": "normal",
            "reason": (
                "insufficient historical signal "
                "for stronger learning action"
            ),
        }

    def _analyze_industrial_state(
        self,
        industrial_fields: dict[str, Any],
    ) -> dict[str, Any]:

        machines = industrial_fields.get("machines", [])
        alarms = industrial_fields.get("alarms", [])

        running_machines = 0
        stopped_machines = 0
        warning_machines = 0

        for machine in machines:

            if not isinstance(machine, dict):
                continue

            status = str(
                machine.get("status", "")
            ).lower()

            if status == "running":
                running_machines += 1

            elif status in {
                "stopped",
                "down",
                "offline",
            }:
                stopped_machines += 1

            elif status in {
                "warning",
                "degraded",
            }:
                warning_machines += 1

        critical_alarms = 0
        warning_alarms = 0

        for alarm in alarms:

            if not isinstance(alarm, dict):
                continue

            severity = str(
                alarm.get("severity", "")
            ).lower()

            if severity in {
                "critical",
                "fatal",
                "emergency",
            }:
                critical_alarms += 1

            elif severity in {
                "warning",
                "medium",
            }:
                warning_alarms += 1

        if critical_alarms > 0:
            operational_signal = "critical_alarm"
        elif stopped_machines > 0:
            operational_signal = "machine_stop_detected"
        elif warning_machines > 0:
            operational_signal = "machine_warning"
        elif warning_alarms > 0:
            operational_signal = "warning_alarm"
        elif running_machines > 0:
            operational_signal = "machines_operational"
        elif machines or alarms:
            operational_signal = "industrial_data_available"
        else:
            operational_signal = "no_industrial_data"

        return {
            "status": "industrial_analysis_completed",
            "factory_available": industrial_fields.get("factory")
            is not None,
            "production_line_count": len(
                industrial_fields.get(
                    "production_lines",
                    [],
                )
            ),
            "machine_count": len(machines),
            "sensor_count": len(
                industrial_fields.get(
                    "sensors",
                    [],
                )
            ),
            "alarm_count": len(alarms),
            "running_machines": running_machines,
            "stopped_machines": stopped_machines,
            "warning_machines": warning_machines,
            "critical_alarms": critical_alarms,
            "warning_alarms": warning_alarms,
            "operational_signal": operational_signal,
        }

    def _analyze_anomalies(
        self,
        industrial_fields: dict[str, Any],
    ) -> dict[str, Any]:

        machines = industrial_fields.get("machines", [])
        sensors = industrial_fields.get("sensors", [])
        production = industrial_fields.get("production")
        energy = industrial_fields.get("energy")
        alarms = industrial_fields.get("alarms", [])

        signals: list[dict[str, Any]] = []

        machine_ids = {
            machine.get("id")
            for machine in machines
            if isinstance(machine, dict)
            and machine.get("id")
        }

        for sensor in sensors:

            if not isinstance(sensor, dict):
                continue

            sensor_type = str(
                sensor.get("type", "")
            ).lower()

            value = sensor.get("value")

            if not isinstance(value, (int, float)):
                continue

            machine_id = sensor.get("machine_id")

            if machine_id and machine_id not in machine_ids:
                continue

            if sensor_type in {
                "temperature",
                "temp",
            } and value >= 80:

                signals.append({
                    "type": "temperature_elevated",
                    "machine_id": machine_id,
                    "sensor_id": sensor.get("id"),
                    "value": value,
                    "unit": sensor.get("unit"),
                    "threshold": 80,
                })

            elif sensor_type in {
                "vibration",
                "vibration_level",
            } and value >= 4:

                signals.append({
                    "type": "vibration_elevated",
                    "machine_id": machine_id,
                    "sensor_id": sensor.get("id"),
                    "value": value,
                    "unit": sensor.get("unit"),
                    "threshold": 4,
                })

        production_output = None
        production_target = None

        if isinstance(production, dict):

            production_output = production.get("output")
            production_target = production.get("target")

            if (
                isinstance(production_output, (int, float))
                and isinstance(production_target, (int, float))
                and production_target > 0
            ):

                production_ratio = (
                    production_output
                    / production_target
                )

                if production_ratio < 0.90:

                    signals.append({
                        "type": "production_decreased",
                        "value": production_output,
                        "target": production_target,
                        "ratio": round(
                            production_ratio,
                            3,
                        ),
                    })

        energy_value = None

        if isinstance(energy, dict):

            energy_value = energy.get("consumption")

            if (
                isinstance(energy_value, (int, float))
                and energy_value >= 480
            ):

                signals.append({
                    "type": "energy_increased",
                    "value": energy_value,
                    "unit": energy.get("unit"),
                    "threshold": 480,
                })

        alarm_signal_count = 0

        for alarm in alarms:

            if not isinstance(alarm, dict):
                continue

            severity = str(
                alarm.get("severity", "")
            ).lower()

            if severity in {
                "critical",
                "fatal",
                "emergency",
            }:

                alarm_signal_count += 1

                signals.append({
                    "type": "critical_alarm",
                    "alarm_id": alarm.get("id"),
                    "machine_id": alarm.get("machine_id"),
                    "severity": severity,
                })

            elif severity in {
                "warning",
                "medium",
            }:

                alarm_signal_count += 1

        signal_types = {
            signal["type"]
            for signal in signals
        }

        machine_signal_counts: dict[str, int] = {}

        for signal in signals:

            machine_id = signal.get("machine_id")

            if machine_id:

                machine_signal_counts[machine_id] = (
                    machine_signal_counts.get(
                        machine_id,
                        0,
                    )
                    + 1
                )

        correlated_machines = sorted(
            machine_id
            for machine_id, count
            in machine_signal_counts.items()
            if count >= 2
        )

        if len(signals) == 0:
            status = "no_anomaly"
            severity = "none"
        elif len(signals) == 1:
            status = "anomaly_signal"
            severity = "low"
        elif len(signals) == 2:
            status = "anomaly_detected"
            severity = "medium"
        else:
            status = "anomaly_detected"
            severity = "high"

        if correlated_machines:
            status = "anomaly_detected"
            severity = "high"

        confidence = min(
            0.99,
            0.50 + (0.10 * len(signals)),
        )

        return {
            "status": status,
            "severity": severity,
            "signal_count": len(signals),
            "signals": signals,
            "signal_types": sorted(signal_types),
            "correlated_machines": correlated_machines,
            "machine_signal_counts": machine_signal_counts,
            "critical_alarm_count": alarm_signal_count,
            "confidence": round(confidence, 2),
            "production_output": production_output,
            "production_target": production_target,
            "energy_value": energy_value,
        }

    def _build_conclusions(
        self,
        state_assessment: dict[str, Any],
        memory_analysis: dict[str, Any],
        historical_memory_analysis: dict[str, Any],
        feedback_analysis: dict[str, Any],
        learning_signal: dict[str, Any],
        industrial_analysis: dict[str, Any],
        anomaly_analysis: dict[str, Any],
    ) -> list[dict[str, Any]]:

        conclusions: list[dict[str, Any]] = []

        if memory_analysis["status"] == "memory_available":

            conclusions.append({
                "type": "memory",
                "status": "historical_context_available",
                "entry_count": memory_analysis["entry_count"],
            })

        if (
            historical_memory_analysis["status"]
            == "historical_memory_available"
        ):

            conclusions.append({
                "type": "historical_memory",
                "status": "historical_patterns_available",
                "entry_count": historical_memory_analysis[
                    "entry_count"
                ],
            })

        recurring_machine_ids = historical_memory_analysis.get(
            "recurring_machine_ids",
            [],
        )

        if recurring_machine_ids:

            conclusions.append({
                "type": "historical_pattern",
                "status": "recurring_historical_machines",
                "machine_ids": recurring_machine_ids,
            })

        if feedback_analysis["status"] == "adjustment_required":

            conclusions.append({
                "type": "learning",
                "status": "adjustment_required",
            })

        elif feedback_analysis["status"] == "positive_history":

            conclusions.append({
                "type": "learning",
                "status": "positive_feedback_history",
            })

        operational_signal = industrial_analysis[
            "operational_signal"
        ]

        if operational_signal == "critical_alarm":

            conclusions.append({
                "type": "industrial",
                "status": "critical_alarm_detected",
            })

        elif operational_signal == "machine_stop_detected":

            conclusions.append({
                "type": "industrial",
                "status": "machine_stop_detected",
            })

        elif operational_signal == "machine_warning":

            conclusions.append({
                "type": "industrial",
                "status": "machine_warning_detected",
            })

        elif operational_signal == "warning_alarm":

            conclusions.append({
                "type": "industrial",
                "status": "warning_alarm_detected",
            })

        elif operational_signal == "machines_operational":

            conclusions.append({
                "type": "industrial",
                "status": "machines_operational",
            })

        if anomaly_analysis["status"] != "no_anomaly":

            conclusions.append({
                "type": "anomaly",
                "status": anomaly_analysis["status"],
                "severity": anomaly_analysis["severity"],
                "signal_count": anomaly_analysis["signal_count"],
                "signal_types": anomaly_analysis["signal_types"],
                "correlated_machines": anomaly_analysis[
                    "correlated_machines"
                ],
            })

        conclusions.append({
            "type": "learning_signal",
            "action": learning_signal["action"],
            "priority": learning_signal["priority"],
        })

        return conclusions

    def get_status(self) -> dict[str, Any]:

        return {
            "component": "reasoning",
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
            "last_analysis_id": (
                self.last_analysis.get("analysis_id")
                if self.last_analysis
                else None
            ),
        }
