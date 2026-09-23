"""
AIHelixia Intelligence Engine
Persistence Layer
Version: 0.1.0
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Persistence:
    """
    Dauerhafte Speicherung für FactoryIQ und AIHelixia.

    Verantwortlichkeiten:
    - Factory-Zustände speichern
    - Messwerte speichern
    - Alarme speichern
    - Engine-Events speichern
    - AI-Ergebnisse speichern
    - Historische Daten abrufen

    Keine fachliche Analyse.
    Keine Prediction.
    Keine Decision.
    Keine LLM-Abhängigkeit.
    """

    VERSION = "0.2.0"

    def __init__(
        self,
        database_path: str | Path = "data/factoryiq.db",
    ) -> None:
        self.database_path = Path(database_path)
        self.status = "created"
        self.connection: sqlite3.Connection | None = None

    def start(self) -> None:
        """
        Startet die Persistence-Schicht und initialisiert
        die SQLite-Datenbank inklusive Schema.
        """
        if self.status == "running":
            return

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path,
        )

        self.connection.row_factory = sqlite3.Row

        # Wichtig:
        # _create_schema() benötigt eine aktive Persistence.
        self.status = "running"

        self._create_schema()

    def stop(self) -> None:
        """
        Beendet die Datenbankverbindung.
        """
        if self.connection is not None:
            self.connection.close()

        self.connection = None
        self.status = "stopped"

    def _require_connection(self) -> sqlite3.Connection:
        """
        Stellt sicher, dass Persistence aktiv ist.
        """
        if self.status != "running" or self.connection is None:
            raise RuntimeError(
                "Persistence ist nicht gestartet."
            )

        return self.connection

    def _create_schema(self) -> None:
        """
        Erstellt das Datenbankschema, falls es noch nicht existiert.
        """
        connection = self._require_connection()

        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS factory_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factory_id TEXT,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT,
                machine_id TEXT,
                timestamp TEXT NOT NULL,
                value REAL,
                unit TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alarm_id TEXT,
                machine_id TEXT,
                timestamp TEXT NOT NULL,
                severity TEXT,
                alarm_type TEXT,
                message TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS engine_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ai_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                result_type TEXT NOT NULL,
                data TEXT NOT NULL
            );
            """
        )

        connection.commit()

    @staticmethod
    def _timestamp() -> str:
        """
        Liefert einen UTC-Zeitstempel im ISO-8601-Format.
        """
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _json(data: Any) -> str:
        """
        Serialisiert Daten sicher als JSON.
        """
        return json.dumps(
            data,
            ensure_ascii=False,
            default=str,
        )

    def save_factory_state(
        self,
        factory_state: dict[str, Any],
    ) -> int:
        """
        Speichert einen vollständigen Factory-Zustand.
        """
        connection = self._require_connection()

        factory = factory_state.get(
            "factory",
            {},
        )

        factory_id = None

        if isinstance(factory, dict):
            factory_id = factory.get("id")

        cursor = connection.execute(
            """
            INSERT INTO factory_states (
                factory_id,
                timestamp,
                data
            )
            VALUES (?, ?, ?)
            """,
            (
                factory_id,
                self._timestamp(),
                self._json(factory_state),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    def save_measurement(
        self,
        measurement: dict[str, Any],
    ) -> int:
        """
        Speichert einen einzelnen Messwert.
        """
        connection = self._require_connection()

        cursor = connection.execute(
            """
            INSERT INTO measurements (
                sensor_id,
                machine_id,
                timestamp,
                value,
                unit,
                data
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                measurement.get("sensor_id"),
                measurement.get("machine_id"),
                measurement.get(
                    "timestamp",
                    self._timestamp(),
                ),
                measurement.get("value"),
                measurement.get("unit"),
                self._json(measurement),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    def save_alarm(
        self,
        alarm: dict[str, Any],
    ) -> int:
        """
        Speichert einen Alarm.
        """
        connection = self._require_connection()

        cursor = connection.execute(
            """
            INSERT INTO alarms (
                alarm_id,
                machine_id,
                timestamp,
                severity,
                alarm_type,
                message,
                data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                alarm.get("id"),
                alarm.get("machine_id"),
                alarm.get(
                    "timestamp",
                    self._timestamp(),
                ),
                alarm.get("severity"),
                alarm.get("type"),
                alarm.get("message"),
                self._json(alarm),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    def save_engine_event(
        self,
        event_type: str,
        data: dict[str, Any],
    ) -> int:
        """
        Speichert ein Engine-Ereignis.
        """
        connection = self._require_connection()

        cursor = connection.execute(
            """
            INSERT INTO engine_events (
                timestamp,
                event_type,
                data
            )
            VALUES (?, ?, ?)
            """,
            (
                self._timestamp(),
                event_type,
                self._json(data),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    def save_ai_result(
        self,
        result_type: str,
        data: dict[str, Any],
    ) -> int:
        """
        Speichert ein Ergebnis der AI-Pipeline.
        """
        connection = self._require_connection()

        cursor = connection.execute(
            """
            INSERT INTO ai_results (
                timestamp,
                result_type,
                data
            )
            VALUES (?, ?, ?)
            """,
            (
                self._timestamp(),
                result_type,
                self._json(data),
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)

    def get_history(
        self,
        table: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Gibt historische Datensätze einer erlaubten Tabelle zurück.
        """
        connection = self._require_connection()

        allowed_tables = {
            "factory_states",
            "measurements",
            "alarms",
            "engine_events",
            "ai_results",
        }

        if table not in allowed_tables:
            raise ValueError(
                f"Unbekannte Persistence-Tabelle: {table}"
            )

        if limit < 1:
            raise ValueError(
                "limit muss größer als 0 sein."
            )

        rows = connection.execute(
            f"""
            SELECT *
            FROM {table}
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    def get_status(self) -> dict[str, Any]:
        """
        Gibt den aktuellen Zustand der Persistence-Schicht zurück.
        """
        return {
            "component": "persistence",
            "version": self.VERSION,
            "status": self.status,
            "database_path": str(
                self.database_path
            ),
        }
