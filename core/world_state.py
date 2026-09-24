"""
AIHelixia Intelligence Engine
World State
Version: 0.8.0
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


class WorldState:
    """
    Verwaltet den aktuellen internen Zustand der Engine.

    V0.8.0:
    - deterministische Zustandsverwaltung
    - keine LLM-Abhängigkeit
    - Upsert-Verhalten für industrielle Komponenten
    - keine Duplikate bei wiederholtem Factory-Ingest
    - sichere State-Snapshots
    - gezielte Objektabfragen
    - gezieltes Entfernen industrieller Objekte
    """

    VERSION = "0.8.0"

    def __init__(self) -> None:
        self.status = "created"

        self.observations: list[dict[str, Any]] = []
        self.entities: list[dict[str, Any]] = []
        self.conditions: list[dict[str, Any]] = []

        self.factory: dict[str, Any] = {}
        self.production_lines: list[dict[str, Any]] = []
        self.machines: list[dict[str, Any]] = []
        self.sensors: list[dict[str, Any]] = []
        self.production: dict[str, Any] = {}
        self.energy: dict[str, Any] = {}
        self.maintenance: dict[str, Any] = {}
        self.alarms: list[dict[str, Any]] = []

        self.updated_at: str | None = None

    def start(self) -> None:
        self.status = "running"
        self._update_timestamp()

    def stop(self) -> None:
        self.status = "stopped"
        self._update_timestamp()

    def add_observation(
        self,
        perception: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(perception, dict):
            raise TypeError("Perception muss ein Dictionary sein.")

        observation = {
            "id": len(self.observations) + 1,
            "timestamp": self._current_timestamp(),
            "data": deepcopy(perception),
        }

        self.observations.append(observation)
        self._update_timestamp()

        return deepcopy(observation)

    def add_entity(
        self,
        entity: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(entity, dict):
            raise TypeError("Entity muss ein Dictionary sein.")

        entity_copy = deepcopy(entity)

        self.entities.append(entity_copy)
        self._update_timestamp()

        return deepcopy(entity_copy)

    def add_condition(
        self,
        condition: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(condition, dict):
            raise TypeError("Condition muss ein Dictionary sein.")

        condition_copy = deepcopy(condition)

        self.conditions.append(condition_copy)
        self._update_timestamp()

        return deepcopy(condition_copy)

    def set_factory(
        self,
        factory: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(factory, dict):
            raise TypeError("Factory muss ein Dictionary sein.")

        self.factory = deepcopy(factory)
        self._update_timestamp()

        return deepcopy(self.factory)

    def add_production_line(
        self,
        production_line: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(production_line, dict):
            raise TypeError(
                "Production Line muss ein Dictionary sein."
            )

        production_line_copy = deepcopy(production_line)

        self._upsert_by_id(
            self.production_lines,
            production_line_copy,
        )

        self._update_timestamp()

        return deepcopy(production_line_copy)

    def add_machine(
        self,
        machine: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(machine, dict):
            raise TypeError("Machine muss ein Dictionary sein.")

        machine_copy = deepcopy(machine)

        self._upsert_by_id(
            self.machines,
            machine_copy,
        )

        self._update_timestamp()

        return deepcopy(machine_copy)

    def add_sensor(
        self,
        sensor: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(sensor, dict):
            raise TypeError("Sensor muss ein Dictionary sein.")

        sensor_copy = deepcopy(sensor)

        self._upsert_by_id(
            self.sensors,
            sensor_copy,
        )

        self._update_timestamp()

        return deepcopy(sensor_copy)

    def set_production(
        self,
        production: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(production, dict):
            raise TypeError("Production muss ein Dictionary sein.")

        self.production = deepcopy(production)
        self._update_timestamp()

        return deepcopy(self.production)

    def set_energy(
        self,
        energy: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(energy, dict):
            raise TypeError("Energy muss ein Dictionary sein.")

        self.energy = deepcopy(energy)
        self._update_timestamp()

        return deepcopy(self.energy)

    def set_maintenance(
        self,
        maintenance: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(maintenance, dict):
            raise TypeError("Maintenance muss ein Dictionary sein.")

        self.maintenance = deepcopy(maintenance)
        self._update_timestamp()

        return deepcopy(self.maintenance)

    def add_alarm(
        self,
        alarm: dict[str, Any],
    ) -> dict[str, Any]:

        self._require_running()

        if not isinstance(alarm, dict):
            raise TypeError("Alarm muss ein Dictionary sein.")

        alarm_copy = deepcopy(alarm)

        self._upsert_by_id(
            self.alarms,
            alarm_copy,
        )

        self._update_timestamp()

        return deepcopy(alarm_copy)

    def get_state(self) -> dict[str, Any]:
        """
        Liefert einen sicheren Snapshot des aktuellen World State.

        Der zurückgegebene Zustand enthält keine direkten Referenzen
        auf die internen Datenstrukturen.
        """

        return deepcopy(
            {
                "status": self.status,
                "factory": self.factory,
                "production_lines": self.production_lines,
                "machines": self.machines,
                "sensors": self.sensors,
                "production": self.production,
                "energy": self.energy,
                "maintenance": self.maintenance,
                "alarms": self.alarms,
                "observations": self.observations,
                "entities": self.entities,
                "conditions": self.conditions,
                "updated_at": self.updated_at,
            }
        )

    def get_snapshot(self) -> dict[str, Any]:
        """
        Explizite Snapshot-API für andere Engine-Komponenten.
        """

        return self.get_state()

    def get_factory(self) -> dict[str, Any] | None:
        return self._find_by_id(
            self.factory,
            None,
        )

    def get_production_line(
        self,
        production_line_id: str,
    ) -> dict[str, Any] | None:

        return self._find_by_id(
            self.production_lines,
            production_line_id,
        )

    def get_machine(
        self,
        machine_id: str,
    ) -> dict[str, Any] | None:

        return self._find_by_id(
            self.machines,
            machine_id,
        )

    def get_sensor(
        self,
        sensor_id: str,
    ) -> dict[str, Any] | None:

        return self._find_by_id(
            self.sensors,
            sensor_id,
        )

    def get_alarm(
        self,
        alarm_id: str,
    ) -> dict[str, Any] | None:

        return self._find_by_id(
            self.alarms,
            alarm_id,
        )

    def remove_production_line(
        self,
        production_line_id: str,
    ) -> bool:

        return self._remove_by_id(
            self.production_lines,
            production_line_id,
        )

    def remove_machine(
        self,
        machine_id: str,
    ) -> bool:

        return self._remove_by_id(
            self.machines,
            machine_id,
        )

    def remove_sensor(
        self,
        sensor_id: str,
    ) -> bool:

        return self._remove_by_id(
            self.sensors,
            sensor_id,
        )

    def remove_alarm(
        self,
        alarm_id: str,
    ) -> bool:

        return self._remove_by_id(
            self.alarms,
            alarm_id,
        )

    def clear(self) -> None:

        self.observations.clear()
        self.entities.clear()
        self.conditions.clear()

        self.factory = {}
        self.production_lines.clear()
        self.machines.clear()
        self.sensors.clear()
        self.production = {}
        self.energy = {}
        self.maintenance = {}
        self.alarms.clear()

        self._update_timestamp()

    def get_status(self) -> dict[str, Any]:

        return {
            "component": "world_state",
            "version": self.VERSION,
            "status": self.status,
            "observation_count": len(self.observations),
            "entity_count": len(self.entities),
            "condition_count": len(self.conditions),
            "factory_available": bool(self.factory),
            "production_line_count": len(self.production_lines),
            "machine_count": len(self.machines),
            "sensor_count": len(self.sensors),
            "production_available": bool(self.production),
            "energy_available": bool(self.energy),
            "maintenance_available": bool(self.maintenance),
            "alarm_count": len(self.alarms),
            "updated_at": self.updated_at,
        }

    def _upsert_by_id(
        self,
        collection: list[dict[str, Any]],
        item: dict[str, Any],
    ) -> None:

        item_id = item.get("id")

        if item_id is None:
            collection.append(item)
            return

        for index, existing in enumerate(collection):
            if existing.get("id") == item_id:
                collection[index] = item
                return

        collection.append(item)

    @staticmethod
    def _find_by_id(
        collection: dict[str, Any] | list[dict[str, Any]],
        item_id: str | None,
    ) -> dict[str, Any] | None:

        if isinstance(collection, dict):
            if item_id is None:
                return deepcopy(collection) if collection else None

            if collection.get("id") == item_id:
                return deepcopy(collection)

            return None

        for item in collection:
            if item.get("id") == item_id:
                return deepcopy(item)

        return None

    def _remove_by_id(
        self,
        collection: list[dict[str, Any]],
        item_id: str,
    ) -> bool:

        self._require_running()

        for index, item in enumerate(collection):
            if item.get("id") == item_id:
                collection.pop(index)
                self._update_timestamp()
                return True

        return False

    def _require_running(self) -> None:

        if self.status != "running":
            raise RuntimeError(
                "World State ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

    def _update_timestamp(self) -> None:
        self.updated_at = self._current_timestamp()

    @staticmethod
    def _current_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()
