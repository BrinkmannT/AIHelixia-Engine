"""
AIHelixia Intelligence Engine
Memory Layer
Version: 0.5.0
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


class Memory:
    """
    Deterministische Memory-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - Ereignisse speichern
    - frühere Verarbeitungsergebnisse abrufen
    - Memory-Einträge strukturiert verwalten
    - gezielte historische Abfragen ermöglichen
    - Grundlage für späteres Langzeitgedächtnis schaffen

    V0.5.0:
    - In-Memory-Speicher
    - deterministisch
    - keine Datenbank
    - keine LLM-Abhängigkeit
    - sichere Datenkopien
    - limitierte Retrieval-Abfragen
    - Typfilter
    - ID-Abfragen
    - Zeitbereichsabfragen
    - einfache Schlüssel-/Wert-Relevanzfilterung
    """

    VERSION = "0.5.0"

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

        self._require_running()

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
            "data": deepcopy(data),
        }

        self.entries.append(entry)

        return deepcopy(entry)

    def retrieve(
        self,
        memory_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Ruft gespeicherte Memory-Einträge ab.

        Wenn memory_type angegeben wird, werden nur
        Einträge dieses Typs zurückgegeben.

        Wenn limit angegeben wird, werden maximal
        limit Einträge zurückgegeben.
        """

        self._require_running()

        self._validate_limit(limit)

        entries = self.entries

        if memory_type is not None:
            entries = [
                entry
                for entry in entries
                if entry["type"] == memory_type
            ]

        if limit is not None:
            entries = entries[-limit:]

        return deepcopy(entries)

    def retrieve_recent(
        self,
        limit: int = 10,
        memory_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Gibt die neuesten Memory-Einträge zurück.

        Neueste Einträge stehen zuerst.
        """

        self._require_running()

        self._validate_limit(limit)

        entries = self.entries

        if memory_type is not None:
            entries = [
                entry
                for entry in entries
                if entry["type"] == memory_type
            ]

        return deepcopy(
            list(reversed(entries[-limit:]))
        )

    def retrieve_by_type(
        self,
        memory_type: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Ruft Memory-Einträge eines bestimmten Typs ab.
        """

        if not memory_type:
            raise ValueError(
                "memory_type darf nicht leer sein."
            )

        return self.retrieve(
            memory_type=memory_type,
            limit=limit,
        )

    def retrieve_by_id(
        self,
        memory_id: int,
    ) -> dict[str, Any] | None:
        """
        Ruft einen einzelnen Memory-Eintrag über seine ID ab.
        """

        self._require_running()

        if memory_id < 1:
            raise ValueError(
                "memory_id muss größer als 0 sein."
            )

        for entry in self.entries:
            if entry["id"] == memory_id:
                return deepcopy(entry)

        return None

    def retrieve_by_time(
        self,
        start_time: str,
        end_time: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Ruft Memory-Einträge innerhalb eines Zeitbereichs ab.
        """

        self._require_running()

        self._validate_limit(limit)

        start = self._parse_timestamp(start_time)
        end = self._parse_timestamp(end_time)

        if start > end:
            raise ValueError(
                "start_time darf nicht nach end_time liegen."
            )

        entries = []

        for entry in self.entries:
            timestamp = self._parse_timestamp(
                entry["timestamp"]
            )

            if start <= timestamp <= end:
                entries.append(entry)

        if limit is not None:
            entries = entries[-limit:]

        return deepcopy(entries)

    def retrieve_relevant(
        self,
        criteria: dict[str, Any],
        limit: int = 10,
        memory_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Führt eine einfache deterministische Relevanzsuche durch.

        Ein Eintrag ist relevant, wenn alle angegebenen Kriterien
        in den gespeicherten Daten übereinstimmen.

        Beispiel:

            criteria={
                "machine_id": "MACHINE-001",
                "status": "warning",
            }
        """

        self._require_running()

        if not isinstance(criteria, dict):
            raise TypeError(
                "criteria muss ein Dictionary sein."
            )

        self._validate_limit(limit)

        matches: list[dict[str, Any]] = []

        for entry in reversed(self.entries):

            if (
                memory_type is not None
                and entry["type"] != memory_type
            ):
                continue

            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            if self._matches_criteria(
                data,
                criteria,
            ):
                matches.append(entry)

            if len(matches) >= limit:
                break

        return deepcopy(matches)

    def latest(
        self,
        limit: int = 1,
    ) -> list[dict[str, Any]]:
        """
        Gibt die zuletzt gespeicherten Memory-Einträge zurück.
        """

        return self.retrieve_recent(
            limit=limit,
        )

    def clear(self) -> None:
        """Löscht alle Memory-Einträge."""

        self._require_running()

        self.entries.clear()
        self.memory_count = 0

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Memory-Status zurück."""

        return {
            "component": "memory",
            "version": self.VERSION,
            "status": self.status,
            "memory_count": self.memory_count,
        }

    def _require_running(self) -> None:

        if self.status != "running":
            raise RuntimeError(
                "Memory ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

    @staticmethod
    def _validate_limit(
        limit: int | None,
    ) -> None:

        if limit is not None and limit < 1:
            raise ValueError(
                "limit muss mindestens 1 sein."
            )

    @staticmethod
    def _parse_timestamp(
        timestamp: str,
    ) -> datetime:

        try:
            return datetime.fromisoformat(timestamp)
        except ValueError as exc:
            raise ValueError(
                f"Ungültiger ISO-8601-Zeitstempel: {timestamp}"
            ) from exc

    @staticmethod
    def _matches_criteria(
        data: dict[str, Any],
        criteria: dict[str, Any],
    ) -> bool:

        for key, expected_value in criteria.items():

            if key not in data:
                return False

            if data[key] != expected_value:
                return False

        return True

    @staticmethod
    def _current_timestamp() -> str:
        """Erzeugt einen UTC-Zeitstempel."""

        return datetime.now(
            timezone.utc
        ).isoformat()
