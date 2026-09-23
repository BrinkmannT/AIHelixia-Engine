"""
AIHelixia Intelligence Engine
FactoryIQ Input Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class FactoryInput:
    """
    Validiert strukturierte FactoryIQ-Eingaben
    und überführt sie in den bestehenden WorldState.

    Keine fachliche Analyse.
    Keine Prediction.
    Keine Decision.
    Keine LLM-Abhängigkeit.
    """

    VERSION = "0.2.0"

    REQUIRED_FIELDS = {
        "factory",
        "production_lines",
        "machines",
        "sensors",
        "production",
        "energy",
        "maintenance",
        "alarms",
    }

    MACHINE_STATUSES = {
        "running",
        "stopped",
        "offline",
        "down",
        "warning",
        "degraded",
    }

    ALARM_SEVERITIES = {
        "critical",
        "fatal",
        "emergency",
        "warning",
        "medium",
    }

    def __init__(self) -> None:
        self.status = "created"
        self.processed_count = 0

    def start(self) -> None:
        self.status = "running"

    def stop(self) -> None:
        self.status = "stopped"

    def validate(
        self,
        factory_data: dict[str, Any],
    ) -> dict[str, Any]:

        if not isinstance(factory_data, dict):
            raise TypeError(
                "FactoryIQ Input muss ein Dictionary sein."
            )

        unknown_fields = set(factory_data) - self.REQUIRED_FIELDS

        if unknown_fields:
            raise ValueError(
                "Unbekannte FactoryIQ Felder: "
                + ", ".join(sorted(unknown_fields))
            )

        for field in (
            "factory",
            "production",
            "energy",
            "maintenance",
        ):
            if field in factory_data and not isinstance(
                factory_data[field],
                dict,
            ):
                raise TypeError(
                    f"FactoryIQ Feld '{field}' "
                    "muss ein Dictionary sein."
                )

        for field in (
            "production_lines",
            "machines",
            "sensors",
            "alarms",
        ):
            if field in factory_data and not isinstance(
                factory_data[field],
                list,
            ):
                raise TypeError(
                    f"FactoryIQ Feld '{field}' "
                    "muss eine Liste sein."
                )

        self._validate_list_of_dicts(
            factory_data.get("production_lines", []),
            "production_lines",
        )

        self._validate_machines(
            factory_data.get("machines", [])
        )

        self._validate_sensors(
            factory_data.get("sensors", [])
        )

        self._validate_alarms(
            factory_data.get("alarms", [])
        )

        return {
            "valid": True,
            "version": self.VERSION,
            "fields": sorted(factory_data.keys()),
        }

    def _validate_list_of_dicts(
        self,
        items: list[Any],
        field_name: str,
    ) -> None:

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise TypeError(
                    f"FactoryIQ Feld '{field_name}' "
                    f"Eintrag {index} muss ein Dictionary sein."
                )

    def _validate_machines(
        self,
        machines: list[Any],
    ) -> None:

        self._validate_list_of_dicts(
            machines,
            "machines",
        )

        for index, machine in enumerate(machines):

            machine_id = machine.get("id")

            if not isinstance(machine_id, str) or not machine_id.strip():
                raise ValueError(
                    f"Machine {index} benötigt ein gültiges 'id' Feld."
                )

            status = machine.get("status")

            if status is not None:
                normalized_status = str(status).lower()

                if normalized_status not in self.MACHINE_STATUSES:
                    raise ValueError(
                        f"Machine '{machine_id}' "
                        f"hat einen ungültigen Status: {status}"
                    )

    def _validate_sensors(
        self,
        sensors: list[Any],
    ) -> None:

        self._validate_list_of_dicts(
            sensors,
            "sensors",
        )

        for index, sensor in enumerate(sensors):

            sensor_id = sensor.get("id")

            if not isinstance(sensor_id, str) or not sensor_id.strip():
                raise ValueError(
                    f"Sensor {index} benötigt ein gültiges 'id' Feld."
                )

            machine_id = sensor.get("machine_id")

            if machine_id is not None and not isinstance(
                machine_id,
                str,
            ):
                raise TypeError(
                    f"Sensor '{sensor_id}' "
                    "'machine_id' muss ein String sein."
                )

            sensor_type = sensor.get("type")

            if sensor_type is not None and not isinstance(
                sensor_type,
                str,
            ):
                raise TypeError(
                    f"Sensor '{sensor_id}' "
                    "'type' muss ein String sein."
                )

            unit = sensor.get("unit")

            if unit is not None and not isinstance(
                unit,
                str,
            ):
                raise TypeError(
                    f"Sensor '{sensor_id}' "
                    "'unit' muss ein String sein."
                )

    def _validate_alarms(
        self,
        alarms: list[Any],
    ) -> None:

        self._validate_list_of_dicts(
            alarms,
            "alarms",
        )

        for index, alarm in enumerate(alarms):

            alarm_id = alarm.get("id")

            if not isinstance(alarm_id, str) or not alarm_id.strip():
                raise ValueError(
                    f"Alarm {index} benötigt ein gültiges 'id' Feld."
                )

            timestamp = alarm.get("timestamp")

            if not isinstance(timestamp, str) or not timestamp.strip():
                raise ValueError(
                    f"Alarm '{alarm_id}' "
                    "benötigt ein gültiges 'timestamp' Feld."
                )

            machine_id = alarm.get("machine_id")

            if not isinstance(machine_id, str) or not machine_id.strip():
                raise ValueError(
                    f"Alarm '{alarm_id}' "
                    "benötigt ein gültiges 'machine_id' Feld."
                )

            severity = alarm.get("severity")

            if not isinstance(severity, str) or not severity.strip():
                raise ValueError(
                    f"Alarm '{alarm_id}' "
                    "benötigt ein gültiges 'severity' Feld."
                )

            normalized_severity = severity.lower()

            if normalized_severity not in self.ALARM_SEVERITIES:
                raise ValueError(
                    f"Alarm '{alarm_id}' "
                    f"hat eine ungültige severity: {severity}"
                )

            alarm_type = alarm.get("type")

            if alarm_type is not None and not isinstance(
                alarm_type,
                str,
            ):
                raise TypeError(
                    f"Alarm '{alarm_id}' "
                    "'type' muss ein String sein."
                )

            message = alarm.get("message")

            if message is not None and not isinstance(
                message,
                str,
            ):
                raise TypeError(
                    f"Alarm '{alarm_id}' "
                    "'message' muss ein String sein."
                )

    def ingest(
        self,
        factory_data: dict[str, Any],
        world_state: Any,
    ) -> dict[str, Any]:

        if self.status != "running":
            raise RuntimeError(
                "FactoryInput ist nicht gestartet."
            )

        self.validate(factory_data)

        if world_state.status != "running":
            raise RuntimeError(
                "World State ist nicht gestartet."
            )

        processed = {
            "factory": False,
            "production_lines": 0,
            "machines": 0,
            "sensors": 0,
            "production": False,
            "energy": False,
            "maintenance": False,
            "alarms": 0,
        }

        if "factory" in factory_data:
            world_state.set_factory(
                factory_data["factory"]
            )
            processed["factory"] = True

        for production_line in factory_data.get(
            "production_lines",
            [],
        ):
            world_state.add_production_line(
                production_line
            )
            processed["production_lines"] += 1

        for machine in factory_data.get(
            "machines",
            [],
        ):
            world_state.add_machine(machine)
            processed["machines"] += 1

        for sensor in factory_data.get(
            "sensors",
            [],
        ):
            world_state.add_sensor(sensor)
            processed["sensors"] += 1

        if "production" in factory_data:
            world_state.set_production(
                factory_data["production"]
            )
            processed["production"] = True

        if "energy" in factory_data:
            world_state.set_energy(
                factory_data["energy"]
            )
            processed["energy"] = True

        if "maintenance" in factory_data:
            world_state.set_maintenance(
                factory_data["maintenance"]
            )
            processed["maintenance"] = True

        for alarm in factory_data.get(
            "alarms",
            [],
        ):
            world_state.add_alarm(alarm)
            processed["alarms"] += 1

        self.processed_count += 1

        return {
            "status": "processed",
            "version": self.VERSION,
            "processed_count": self.processed_count,
            "processed": processed,
        }

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "factory_input",
            "version": self.VERSION,
            "status": self.status,
            "processed_count": self.processed_count,
        }
