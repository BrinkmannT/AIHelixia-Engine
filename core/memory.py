"""
AIHelixia Intelligence Engine
Memory Layer
Version: 0.4.0
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class Memory:
    """
    Deterministische Memory-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - Ereignisse speichern
    - frühere Verarbeitungsergebnisse abrufen
    - Memory-Einträge strukturiert verwalten
    - Grundlage für späteres Langzeitgedächtnis schaffen

    V0.4.0:
    - In-Memory-Speicher
    - deterministisch
    - keine Datenbank
    - keine LLM-Abhängigkeit
    """

    def __init__(self) -> None:
        self.status = "created"
        self.entries: list[dict[str, Any]] = []
        self.memory_count = 0

    def start(self) -> None:
        """Startet die Memory-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Memory-Schicht."""

        self.status = "stopped"

    def store(
        self,
        memory_type: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Speichert einen neuen Memory-Eintrag.
        """

        if self.status != "running":
            raise RuntimeError(
                "Memory ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        if not memory_type:
            raise ValueError(
                "memory_type darf nicht leer sein."
            )

        if not isinstance(data, dict):
            raise TypeError(
                "Memory-Daten müssen ein Dictionary sein."
            )

        self.memory_count += 1

        entry = {
            "id": self.memory_count,
            "timestamp": self._current_timestamp(),
            "type": memory_type,
            "data": data,
        }

        self.entries.append(entry)

        return entry

    def retrieve(
        self,
        memory_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Ruft gespeicherte Memory-Einträge ab.

        Wenn memory_type angegeben wird, werden nur
        Einträge dieses Typs zurückgegeben.
        """

        if self.status != "running":
            raise RuntimeError(
                "Memory ist nicht gestartet."
            )

        if memory_type is None:
            return list(self.entries)

        return [
            entry
            for entry in self.entries
            if entry["type"] == memory_type
        ]

    def latest(
        self,
        limit: int = 1,
    ) -> list[dict[str, Any]]:
        """
        Gibt die zuletzt gespeicherten Memory-Einträge zurück.
        """

        if self.status != "running":
            raise RuntimeError(
                "Memory ist nicht gestartet."
            )

        if limit < 1:
            raise ValueError(
                "limit muss mindestens 1 sein."
            )

        return list(
            reversed(self.entries[-limit:])
        )

    def clear(self) -> None:
        """Löscht alle Memory-Einträge."""

        if self.status != "running":
            raise RuntimeError(
                "Memory ist nicht gestartet."
            )

        self.entries.clear()
        self.memory_count = 0

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Memory-Status zurück."""

        return {
            "component": "memory",
            "status": self.status,
            "memory_count": self.memory_count,
        }

    @staticmethod
    def _current_timestamp() -> str:
        """Erzeugt einen UTC-Zeitstempel."""

        return datetime.now(
            timezone.utc
        ).isoformat()