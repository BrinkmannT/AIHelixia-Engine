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

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "factoryiq_pilot",
            "version": self.VERSION,
            "status": "ready",
        }
