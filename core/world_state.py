"""
AIHelixia Intelligence Engine
World State
Version: 0.5.0
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class WorldState:
    """
    Verwaltet den aktuellen internen Zustand der Engine.

    Verantwortlichkeiten:
    - Wahrnehmungen speichern
    - Beobachtungen verwalten
    - aktuellen Zustand bereitstellen
    - Zustandsänderungen nachvollziehbar machen

    V0.2.0:
    - deterministische Zustandsverwaltung
    - keine LLM-Abhängigkeit
    - keine fachliche Interpretation
    """

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
        """Startet den World State."""

        self.status = "running"
        self._update_timestamp()

    def stop(self) -> None:
        """Stoppt den World State."""

        self.status = "stopped"
        self._update_timestamp()

    def add_observation(
        self,
        perception: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Fügt eine Wahrnehmung als Beobachtung hinzu.
        """

        if self.status != "running":
            raise RuntimeError(
                "World State ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not isinstance(perception, dict):
            raise TypeError(
                "Perception muss ein Dictionary sein."
            )

        observation = {
            "id": len(self.observations) + 1,
            "timestamp": self._current_timestamp(),
            "data": perception,
        }

        self.observations.append(observation)
        self._update_timestamp()

        return observation

    def add_entity(
        self,
        entity: dict[str, Any],
    ) -> dict[str, Any]:
        """Fügt eine Entität zum World State hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "World State ist nicht gestartet."
            )

        if not isinstance(entity, dict):
            raise TypeError(
                "Entity muss ein Dictionary sein."
            )

        self.entities.append(entity)
        self._update_timestamp()

        return entity

    def add_condition(
        self,
        condition: dict[str, Any],
    ) -> dict[str, Any]:
        """Fügt eine Bedingung zum World State hinzu."""

        if self.status != "running":
            raise RuntimeError(
                "World State ist nicht gestartet."
            )

        if not isinstance(condition, dict):
            raise TypeError(
                "Condition muss ein Dictionary sein."
            )

        self.conditions.append(condition)
        self._update_timestamp()

        return condition

    def set_factory(self, factory: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(factory, dict):
            raise TypeError("Factory muss ein Dictionary sein.")
        self.factory = factory
        self._update_timestamp()
        return factory

    def add_production_line(self, production_line: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(production_line, dict):
            raise TypeError("Production Line muss ein Dictionary sein.")
        self.production_lines.append(production_line)
        self._update_timestamp()
        return production_line

    def add_machine(self, machine: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(machine, dict):
            raise TypeError("Machine muss ein Dictionary sein.")
        self.machines.append(machine)
        self._update_timestamp()
        return machine

    def add_sensor(self, sensor: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(sensor, dict):
            raise TypeError("Sensor muss ein Dictionary sein.")
        self.sensors.append(sensor)
        self._update_timestamp()
        return sensor

    def set_production(self, production: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(production, dict):
            raise TypeError("Production muss ein Dictionary sein.")
        self.production = production
        self._update_timestamp()
        return production

    def set_energy(self, energy: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(energy, dict):
            raise TypeError("Energy muss ein Dictionary sein.")
        self.energy = energy
        self._update_timestamp()
        return energy

    def set_maintenance(self, maintenance: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(maintenance, dict):
            raise TypeError("Maintenance muss ein Dictionary sein.")
        self.maintenance = maintenance
        self._update_timestamp()
        return maintenance

    def add_alarm(self, alarm: dict[str, Any]) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError("World State ist nicht gestartet.")
        if not isinstance(alarm, dict):
            raise TypeError("Alarm muss ein Dictionary sein.")
        self.alarms.append(alarm)
        self._update_timestamp()
        return alarm

    def get_state(self) -> dict[str, Any]:
        """Gibt den vollständigen aktuellen World State zurück."""

        return {
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

    def clear(self) -> None:
        """Setzt den World State zurück."""

        self.observations.clear()
        self.entities.clear()
        self.conditions.clear()
        self._update_timestamp()

    def get_status(self) -> dict[str, Any]:
        """Gibt den Status des World State zurück."""

        return {
            "component": "world_state",
            "status": self.status,
            "observation_count": len(self.observations),
            "entity_count": len(self.entities),
            "condition_count": len(self.conditions),
            "updated_at": self.updated_at,
        }

    def _update_timestamp(self) -> None:
        """Aktualisiert den Zeitstempel."""

        self.updated_at = self._current_timestamp()

    @staticmethod
    def _current_timestamp() -> str:
        """Erzeugt einen UTC-Zeitstempel."""

        return datetime.now(
            timezone.utc
        ).isoformat()