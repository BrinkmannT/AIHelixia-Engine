"""
AIHelixia Intelligence Engine
FactoryIQ Input Layer
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


class FactoryInput:
    """
    Strukturiert industrielle FactoryIQ-Eingaben
    und überführt sie in den bestehenden WorldState.
    """

    VERSION = "0.1.0"

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
                    f"FactoryIQ Feld '{field}' muss ein Dictionary sein."
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
                    f"FactoryIQ Feld '{field}' muss eine Liste sein."
                )

        return {
            "valid": True,
            "fields": sorted(factory_data.keys()),
        }

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
