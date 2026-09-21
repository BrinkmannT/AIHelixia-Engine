"""
AIHelixia Intelligence Engine
World State
Version: 0.2.0
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

    def get_state(self) -> dict[str, Any]:
        """Gibt den vollständigen aktuellen World State zurück."""

        return {
            "status": self.status,
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