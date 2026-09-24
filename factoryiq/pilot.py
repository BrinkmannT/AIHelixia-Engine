from __future__ import annotations

from copy import deepcopy
from typing import Any


class FactoryIQPilot:
    """
    FactoryIQ Pilot V0.1.

    Read-only aggregation layer over the AIHelixia Engine.
    The pilot layer does not modify the engine core or persistence data.
    """

    VERSION = "0.1.0"

    def __init__(self, engine: Any) -> None:
        self.engine = engine

    def build_overview(self) -> dict[str, Any]:
        """
        Build a customer-facing FactoryIQ pilot overview
        from the current engine state.
        """

        world_state = deepcopy(
            self.engine.world_state.get_state()
        )

        factory = deepcopy(
            world_state.get("factory", {})
        )

        production_lines = deepcopy(
            world_state.get("production_lines", [])
        )

        machines = deepcopy(
            world_state.get("machines", [])
        )

        sensors = deepcopy(
            world_state.get("sensors", [])
        )

        production = deepcopy(
            world_state.get("production", {})
        )

        energy = deepcopy(
            world_state.get("energy", {})
        )

        maintenance = deepcopy(
            world_state.get("maintenance", {})
        )

        alarms = deepcopy(
            world_state.get("alarms", [])
        )

        return {
            "status": "ready",
            "version": self.VERSION,
            "factory": {
                "id": factory.get("id"),
                "name": factory.get("name"),
                "location": factory.get("location"),
                "status": world_state.get("status"),
            },
            "operations": {
                "production_lines": production_lines,
                "machines": machines,
                "sensors": sensors,
                "production": production,
                "energy": energy,
                "maintenance": maintenance,
            },
            "alerts": {
                "count": len(alarms),
                "alarms": alarms,
            },
            "ai_intelligence": {
                "status": "available",
            },
            "history": {
                "available": True,
            },
        }

    def build_intelligence(self) -> dict[str, Any]:
        """
        Build a customer-facing intelligence summary
        from the latest persisted AI results.
        """

        rows = self.engine.persistence.get_history("ai_results")

        latest: dict[str, dict[str, Any]] = {}

        for row in rows:
            result_type = row.get("result_type")

            if not result_type:
                continue

            latest[result_type] = deepcopy(row)

        return {
            "status": "available",
            "version": self.VERSION,
            "results": {
                "reasoning": latest.get("reasoning"),
                "prediction": latest.get("prediction"),
                "decision": latest.get("decision"),
                "action": latest.get("action"),
                "evaluation": latest.get("evaluation"),
                "feedback": latest.get("feedback"),
            },
            "available_types": sorted(latest.keys()),
        }

    def build_dashboard(self) -> dict[str, Any]:
        """
        Build a compact FactoryIQ dashboard data model
        from current engine state and persisted intelligence.
        """

        overview = self.build_overview()
        intelligence = self.build_intelligence()

        machines = overview["operations"]["machines"]
        alarms = overview["alerts"]["alarms"]
        production = overview["operations"]["production"]
        energy = overview["operations"]["energy"]
        maintenance = overview["operations"]["maintenance"]

        machine_status_counts: dict[str, int] = {}

        for machine in machines:
            if not isinstance(machine, dict):
                continue

            status = machine.get("status", "unknown")
            machine_status_counts[status] = (
                machine_status_counts.get(status, 0) + 1
            )

        alarm_severity_counts: dict[str, int] = {}

        for alarm in alarms:
            if not isinstance(alarm, dict):
                continue

            severity = alarm.get("severity", "unknown")
            alarm_severity_counts[severity] = (
                alarm_severity_counts.get(severity, 0) + 1
            )

        reasoning = intelligence["results"].get("reasoning")
        reasoning_data = (
            reasoning.get("data", {})
            if isinstance(reasoning, dict)
            else {}
        )

        historical_analysis = reasoning_data.get(
            "historical_memory_analysis",
            {},
        )

        industrial_analysis = reasoning_data.get(
            "industrial_analysis",
            {},
        )

        learning_signal = reasoning_data.get(
            "learning_signal",
            {},
        )

        prediction = intelligence["results"].get("prediction")
        prediction_data = (
            prediction.get("data", {})
            if isinstance(prediction, dict)
            else {}
        )

        decision = intelligence["results"].get("decision")
        decision_data = (
            decision.get("data", {})
            if isinstance(decision, dict)
            else {}
        )

        evaluation = intelligence["results"].get("evaluation")
        evaluation_data = (
            evaluation.get("data", {})
            if isinstance(evaluation, dict)
            else {}
        )

        historical_rows = self.engine.persistence.get_history(
            "factory_states"
        )

        historical_machine_counts: dict[str, int] = {}
        historical_status_counts: dict[str, int] = {}

        for row in historical_rows:
            if not isinstance(row, dict):
                continue

            data = row.get("data", {})
            if not isinstance(data, dict):
                continue

            machines_history = data.get("machines", [])

            if isinstance(machines_history, list):
                for machine in machines_history:
                    if not isinstance(machine, dict):
                        continue

                    machine_id = machine.get("id")
                    if machine_id:
                        historical_machine_counts[machine_id] = (
                            historical_machine_counts.get(machine_id, 0) + 1
                        )

                    status = machine.get("status")
                    if status:
                        historical_status_counts[status] = (
                            historical_status_counts.get(status, 0) + 1
                        )

        recurring_machine_ids = sorted(
            machine_id
            for machine_id, count in historical_machine_counts.items()
            if count > 1
        )

        return {
            "status": "ready",
            "version": self.VERSION,
            "factory": overview["factory"],
            "kpis": {
                "machine_count": len(machines),
                "alarm_count": len(alarms),
                "production_output": production.get("output"),
                "production_target": production.get("target"),
                "energy_consumption": energy.get("consumption"),
                "energy_unit": energy.get("unit"),
            },
            "machines": {
                "status_counts": machine_status_counts,
                "machines": machines,
            },
            "alarms": {
                "severity_counts": alarm_severity_counts,
                "alarms": alarms,
            },
            "production": production,
            "energy": energy,
            "maintenance": maintenance,
            "ai": {
                "operational_signal": industrial_analysis.get(
                    "operational_signal"
                ),
                "learning_signal": learning_signal,
                "prediction": prediction_data,
                "decision": decision_data,
                "evaluation": evaluation_data,
            },
            "historical_patterns": {
                "recurring_machine_ids": recurring_machine_ids,
                "machine_counts": historical_machine_counts,
                "status_counts": historical_status_counts,
                "entry_count": len(historical_rows),
            },
        }

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "factoryiq_pilot",
            "version": self.VERSION,
            "status": "ready",
        }
