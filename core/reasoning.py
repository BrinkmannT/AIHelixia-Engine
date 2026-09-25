"""
AIHelixia Intelligence Engine
Reasoning Layer
Version: 0.8.0
"""

from __future__ import annotations

from typing import Any


class Reasoning:
    VERSION = "0.8.0"

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
            "production_lines": world_state.get(
                "production_lines",
                [],
            ),
            "machines": world_state.get(
                "machines",
                [],
            ),
            "sensors": world_state.get(
                "sensors",
                [],
            ),
            "production": world_state.get(
                "production"
            ),
            "energy": world_state.get(
                "energy"
            ),
            "maintenance": world_state.get(
                "maintenance"
            ),
            "alarms": world_state.get(
                "alarms",
                [],
            ),
        }

        state_assessment = self._assess_state(
            observations,
            entities,
            conditions,
            industrial_fields,
        )

        memory_analysis = self._analyze_memory(
            memory_entries
        )

        historical_memory_analysis = (
            self._analyze_historical_memory(
                memory_entries
            )
        )

        historical_outcome_analysis = (
            self._analyze_historical_outcomes(
                memory_entries
            )
        )

        feedback_analysis = self._analyze_feedback(
            memory_entries
        )

        learning_signal = self._build_learning_signal(
            feedback_analysis,
            historical_memory_analysis,
            historical_outcome_analysis,
        )

        industrial_analysis = (
            self._analyze_industrial_state(
                industrial_fields
            )
        )

        anomaly_analysis = self._analyze_anomalies(
            industrial_fields
        )

        conclusions = self._build_conclusions(
            state_assessment,
            memory_analysis,
            historical_memory_analysis,
            historical_outcome_analysis,
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
            "historical_memory_analysis": (
                historical_memory_analysis
            ),
            "historical_outcome_analysis": (
                historical_outcome_analysis
            ),
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

        observation_count = (
            len(observations)
            if isinstance(observations, list)
            else 0
        )

        entity_count = (
            len(entities)
            if isinstance(entities, list)
            else 0
        )

        condition_count = (
            len(conditions)
            if isinstance(conditions, list)
            else 0
        )

        industrial_data_available = any([
            industrial_fields.get("factory") is not None,
            bool(industrial_fields.get("production_lines")),
            bool(industrial_fields.get("machines")),
            bool(industrial_fields.get("sensors")),
            industrial_fields.get("production") is not None,
            industrial_fields.get("energy") is not None,
            industrial_fields.get("maintenance") is not None,
            bool(industrial_fields.get("alarms")),
        ])

        if (
            observation_count == 0
            and entity_count == 0
            and condition_count == 0
            and not industrial_data_available
        ):
            status = "no_state_data"
        else:
            status = "state_available"

        return {
            "status": status,
            "observation_count": observation_count,
            "entity_count": entity_count,
            "condition_count": condition_count,
            "industrial_data_available": (
                industrial_data_available
            ),
        }

    def _analyze_memory(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not memory_entries:
            return {
                "status": "no_memory",
                "count": 0,
                "types": [],
            }

        types = sorted({
            entry.get("type")
            for entry in memory_entries
            if isinstance(entry, dict)
            and entry.get("type")
        })

        return {
            "status": "memory_available",
            "count": len(memory_entries),
            "entry_count": len(memory_entries),
            "types": types,
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

            memory_type = entry.get("type")

            if memory_type:
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

                    machine_id = machine.get("id")

                    if machine_id:
                        machine_counts[machine_id] = (
                            machine_counts.get(
                                machine_id,
                                0,
                            )
                            + 1
                        )

                    machine_status = machine.get(
                        "status"
                    )

                    if machine_status:
                        status_counts[
                            machine_status
                        ] = (
                            status_counts.get(
                                machine_status,
                                0,
                            )
                            + 1
                        )

            entry_status = data.get("status")

            if entry_status:
                status_counts[entry_status] = (
                    status_counts.get(entry_status, 0) + 1
                )

            action = data.get("action")

            if action:
                action_counts[action] = (
                    action_counts.get(action, 0) + 1
                )

        recurring_machine_ids = sorted(
            machine_id
            for machine_id, count
            in machine_counts.items()
            if count > 1
        )

        return {
            "status": "historical_memory_available",
            "entry_count": len(memory_entries),
            "type_counts": type_counts,
            "machine_counts": machine_counts,
            "status_counts": status_counts,
            "action_counts": action_counts,
            "recurring_machine_ids": (
                recurring_machine_ids
            ),
        }

    def _analyze_historical_outcomes(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        outcome_entries = [
            entry
            for entry in memory_entries
            if isinstance(entry, dict)
            and entry.get("type") == "outcome_learning"
        ]

        if not outcome_entries:
            return {
                "status": "no_historical_outcomes",
                "count": 0,
                "improved_count": 0,
                "degraded_count": 0,
                "unchanged_count": 0,
                "unknown_count": 0,
                "successful_count": 0,
                "unsuccessful_count": 0,
                "review_count": 0,
                "known_outcome_count": 0,
                "success_rate": None,
                "average_confidence": None,
                "average_evaluation_score": None,
                "dominant_outcome": None,
            }

        improved_count = 0
        degraded_count = 0
        unchanged_count = 0
        unknown_count = 0

        successful_count = 0
        unsuccessful_count = 0
        review_count = 0

        confidences: list[float] = []
        evaluation_scores: list[float] = []

        for entry in outcome_entries:

            data = entry.get("data", {})

            if not isinstance(data, dict):
                data = {}

            outcome = data.get("outcome")

            if outcome == "improved":
                improved_count += 1
            elif outcome == "degraded":
                degraded_count += 1
            elif outcome == "unchanged":
                unchanged_count += 1
            else:
                unknown_count += 1

            outcome_success = data.get(
                "outcome_success"
            )

            if outcome_success is True:
                successful_count += 1
            elif outcome_success is False:
                unsuccessful_count += 1

            learning_signal = data.get(
                "learning_signal"
            )

            if learning_signal == "review":
                review_count += 1

            confidence = data.get(
                "outcome_confidence"
            )

            if isinstance(confidence, (int, float)):
                confidences.append(
                    float(confidence)
                )

            evaluation_score = data.get(
                "evaluation_score"
            )

            if isinstance(
                evaluation_score,
                (int, float),
            ):
                evaluation_scores.append(
                    float(evaluation_score)
                )

        known_outcome_count = (
            improved_count
            + degraded_count
            + unchanged_count
        )

        success_rate = None

        if known_outcome_count > 0:
            success_rate = (
                improved_count
                / known_outcome_count
            )

        average_confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else None
        )

        average_evaluation_score = (
            sum(evaluation_scores)
            / len(evaluation_scores)
            if evaluation_scores
            else None
        )

        if known_outcome_count == 0:
            dominant_outcome = None
        else:
            outcome_counts = {
                "improved": improved_count,
                "degraded": degraded_count,
                "unchanged": unchanged_count,
            }

            dominant_outcome = max(
                outcome_counts,
                key=outcome_counts.get,
            )

        if (
            degraded_count > improved_count
            and degraded_count > unchanged_count
        ):
            status = "degraded_history"
        elif (
            improved_count > degraded_count
            and improved_count > unchanged_count
        ):
            status = "positive_history"
        elif known_outcome_count > 0:
            status = "mixed_history"
        else:
            status = "unknown_history"

        return {
            "status": status,
            "count": len(outcome_entries),
            "improved_count": improved_count,
            "degraded_count": degraded_count,
            "unchanged_count": unchanged_count,
            "unknown_count": unknown_count,
            "successful_count": successful_count,
            "unsuccessful_count": unsuccessful_count,
            "review_count": review_count,
            "known_outcome_count": known_outcome_count,
            "success_rate": (
                round(success_rate, 3)
                if success_rate is not None
                else None
            ),
            "average_confidence": (
                round(average_confidence, 3)
                if average_confidence is not None
                else None
            ),
            "average_evaluation_score": (
                round(average_evaluation_score, 3)
                if average_evaluation_score is not None
                else None
            ),
            "dominant_outcome": dominant_outcome,
        }

    def _analyze_feedback(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:

        feedback_entries = [
            entry
            for entry in memory_entries
            if isinstance(entry, dict)
            and entry.get("type") in {
                "feedback",
                "outcome_learning",
            }
        ]

        if not feedback_entries:
            return {
                "status": "no_feedback",
                "count": 0,
                "feedback_count": 0,
                "outcome_learning_count": 0,
                "reinforce_count": 0,
                "adjust_count": 0,
                "review_count": 0,
                "average_score": None,
            }

        reinforce_count = 0
        adjust_count = 0
        review_count = 0
        feedback_count = 0
        outcome_learning_count = 0
        scores: list[float] = []

        for entry in feedback_entries:

            memory_type = entry.get("type")
            data = entry.get("data", {})

            if not isinstance(data, dict):
                data = {}

            if memory_type == "feedback":
                feedback_count += 1
                signal = data.get("signal")

                if signal is None:
                    signal = data.get("action")

                score = data.get("score")

            else:
                outcome_learning_count += 1
                signal = data.get(
                    "learning_signal"
                )
                score = data.get(
                    "evaluation_score"
                )

            if signal == "reinforce":
                reinforce_count += 1
            elif signal == "adjust":
                adjust_count += 1
            elif signal == "review":
                review_count += 1

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
            "feedback_count": feedback_count,
            "outcome_learning_count": (
                outcome_learning_count
            ),
            "reinforce_count": reinforce_count,
            "adjust_count": adjust_count,
            "review_count": review_count,
            "average_score": average_score,
        }

    def _build_learning_signal(
        self,
        feedback_analysis: dict[str, Any],
        historical_memory_analysis: dict[str, Any],
        historical_outcome_analysis: dict[str, Any],
    ) -> dict[str, Any]:

        outcome_count = historical_outcome_analysis.get(
            "known_outcome_count",
            0,
        )

        average_confidence = (
            historical_outcome_analysis.get(
                "average_confidence"
            )
        )

        improved_count = historical_outcome_analysis.get(
            "improved_count",
            0,
        )

        degraded_count = historical_outcome_analysis.get(
            "degraded_count",
            0,
        )

        unchanged_count = historical_outcome_analysis.get(
            "unchanged_count",
            0,
        )

        # Aggregated historical outcome evidence has priority
        # once enough known outcomes are available.
        if (
            outcome_count >= 3
            and average_confidence is not None
            and average_confidence >= 0.75
        ):

            if improved_count > degraded_count:
                return {
                    "action": "reinforce",
                    "priority": "normal",
                    "reason": (
                        "historical outcomes show a "
                        "repeated positive pattern"
                    ),
                    "historical_outcome_count": (
                        outcome_count
                    ),
                    "historical_degraded_count": (
                        degraded_count
                    ),
                    "historical_improved_count": (
                        improved_count
                    ),
                    "historical_unchanged_count": (
                        unchanged_count
                    ),
                    "historical_average_confidence": (
                        average_confidence
                    ),
                }

            if degraded_count > improved_count:
                return {
                    "action": "adjust",
                    "priority": "high",
                    "reason": (
                        "historical outcomes show a "
                        "repeated degraded pattern"
                    ),
                    "historical_outcome_count": (
                        outcome_count
                    ),
                    "historical_degraded_count": (
                        degraded_count
                    ),
                    "historical_improved_count": (
                        improved_count
                    ),
                    "historical_unchanged_count": (
                        unchanged_count
                    ),
                    "historical_average_confidence": (
                        average_confidence
                    ),
                }

        # Fall back to explicit feedback when aggregated
        # historical outcomes are not yet strong enough.
        if (
            feedback_analysis["status"]
            == "adjustment_required"
        ):
            return {
                "action": "adjust",
                "priority": "high",
                "reason": (
                    "historical feedback indicates "
                    "adjustment is required"
                ),
            }

        if (
            feedback_analysis["status"]
            == "positive_history"
        ):
            return {
                "action": "reinforce",
                "priority": "normal",
                "reason": (
                    "historical feedback contains "
                    "positive signals"
                ),
            }

        recurring_machine_ids = (
            historical_memory_analysis.get(
                "recurring_machine_ids",
                [],
            )
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

        machines = industrial_fields.get(
            "machines",
            []
        )
        alarms = industrial_fields.get(
            "alarms",
            []
        )

        running_machines = 0
        stopped_machines = 0
        warning_machines = 0
        critical_alarms = 0
        warning_alarms = 0

        for machine in machines:

            if not isinstance(machine, dict):
                continue

            status = str(
                machine.get("status", "")
            ).lower()

            if status in {
                "running",
                "active",
                "operational",
            }:
                running_machines += 1

            elif status in {
                "stopped",
                "offline",
                "down",
            }:
                stopped_machines += 1

            elif status in {
                "warning",
                "degraded",
                "attention",
            }:
                warning_machines += 1

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
            "factory_available": (
                industrial_fields.get("factory")
                is not None
            ),
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

        machines = industrial_fields.get(
            "machines",
            []
        )
        sensors = industrial_fields.get(
            "sensors",
            []
        )
        production = industrial_fields.get(
            "production"
        )
        energy = industrial_fields.get(
            "energy"
        )
        alarms = industrial_fields.get(
            "alarms",
            []
        )

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

            machine_id = sensor.get(
                "machine_id"
            )

            if (
                machine_id
                and machine_id not in machine_ids
            ):
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

            production_output = production.get(
                "output"
            )
            production_target = production.get(
                "target"
            )

            if (
                isinstance(
                    production_output,
                    (int, float),
                )
                and isinstance(
                    production_target,
                    (int, float),
                )
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

            energy_value = energy.get(
                "consumption"
            )

            if (
                isinstance(
                    energy_value,
                    (int, float),
                )
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
                    "machine_id": alarm.get(
                        "machine_id"
                    ),
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

            machine_id = signal.get(
                "machine_id"
            )

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
            "signal_types": sorted(
                signal_types
            ),
            "correlated_machines": (
                correlated_machines
            ),
            "machine_signal_counts": (
                machine_signal_counts
            ),
            "critical_alarm_count": (
                alarm_signal_count
            ),
            "confidence": round(
                confidence,
                2,
            ),
            "production_output": (
                production_output
            ),
            "production_target": (
                production_target
            ),
            "energy_value": energy_value,
        }

    def _build_conclusions(
        self,
        state_assessment: dict[str, Any],
        memory_analysis: dict[str, Any],
        historical_memory_analysis: dict[str, Any],
        historical_outcome_analysis: dict[str, Any],
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
                "entry_count": memory_analysis[
                    "entry_count"
                ],
            })

        if (
            historical_memory_analysis["status"]
            == "historical_memory_available"
        ):

            conclusions.append({
                "type": "historical_memory",
                "status": (
                    "historical_patterns_available"
                ),
                "entry_count": (
                    historical_memory_analysis[
                        "entry_count"
                    ]
                ),
            })

        recurring_machine_ids = (
            historical_memory_analysis.get(
                "recurring_machine_ids",
                [],
            )
        )

        if recurring_machine_ids:

            conclusions.append({
                "type": "historical_pattern",
                "status": (
                    "recurring_historical_machines"
                ),
                "machine_ids": recurring_machine_ids,
            })

        if (
            historical_outcome_analysis["status"]
            != "no_historical_outcomes"
        ):

            conclusions.append({
                "type": "historical_outcome",
                "status": (
                    historical_outcome_analysis[
                        "status"
                    ]
                ),
                "count": (
                    historical_outcome_analysis[
                        "count"
                    ]
                ),
                "dominant_outcome": (
                    historical_outcome_analysis[
                        "dominant_outcome"
                    ]
                ),
                "success_rate": (
                    historical_outcome_analysis[
                        "success_rate"
                    ]
                ),
            })

        if (
            feedback_analysis["status"]
            == "adjustment_required"
        ):

            conclusions.append({
                "type": "learning",
                "status": "adjustment_required",
            })

        elif (
            feedback_analysis["status"]
            == "positive_history"
        ):

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

        elif (
            operational_signal
            == "machine_stop_detected"
        ):

            conclusions.append({
                "type": "industrial",
                "status": "machine_stop_detected",
            })

        elif (
            operational_signal
            == "machine_warning"
        ):

            conclusions.append({
                "type": "industrial",
                "status": "machine_warning_detected",
            })

        elif (
            operational_signal
            == "warning_alarm"
        ):

            conclusions.append({
                "type": "industrial",
                "status": "warning_alarm_detected",
            })

        elif (
            operational_signal
            == "machines_operational"
        ):

            conclusions.append({
                "type": "industrial",
                "status": "machines_operational",
            })

        if anomaly_analysis["status"] != "no_anomaly":

            conclusions.append({
                "type": "anomaly",
                "status": anomaly_analysis[
                    "status"
                ],
                "severity": anomaly_analysis[
                    "severity"
                ],
                "signal_count": anomaly_analysis[
                    "signal_count"
                ],
                "signal_types": anomaly_analysis[
                    "signal_types"
                ],
                "correlated_machines": (
                    anomaly_analysis[
                        "correlated_machines"
                    ]
                ),
            })

        conclusions.append({
            "type": "learning_signal",
            "action": learning_signal["action"],
            "priority": learning_signal["priority"],
        })

        return conclusions

    def get_status(self) -> dict[str, Any]:

        return {
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
            "last_analysis_available": (
                self.last_analysis is not None
            ),
        }
