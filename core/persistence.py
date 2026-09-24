"""
AIHelixia Intelligence Engine
Persistence Layer
Version: 0.3.0
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

    V0.3.0:
    - Factory-Zustände
    - Messwerte
    - Alarme
    - Engine-Events
    - AI-Ergebnisse
    - Historie
    - Latest-Abfragen
    - ID-Abfragen
    - Zeitbereichsabfragen
    """

    VERSION = "0.3.0"

    ALLOWED_TABLES = {
        "factory_states",
        "measurements",
        "alarms",
        "engine_events",
        "ai_results",
    }

    def __init__(
        self,
        database_path: str | Path = "data/factoryiq.db",
    ) -> None:
        self.database_path = Path(database_path)
        self.status = "created"
        self.connection: sqlite3.Connection | None = None

    def start(self) -> None:
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
        self.status = "running"

        self._create_schema()

    def stop(self) -> None:
        if self.connection is not None:
            self.connection.close()

        self.connection = None
        self.status = "stopped"

    def _require_connection(self) -> sqlite3.Connection:
        if (
            self.status != "running"
            or self.connection is None
        ):
            raise RuntimeError(
                "Persistence ist nicht gestartet."
            )

        return self.connection

    def _create_schema(self) -> None:
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
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _json(data: Any) -> str:
        return json.dumps(
            data,
            ensure_ascii=False,
            default=str,
        )

    @staticmethod
    def _decode_row(
        row: sqlite3.Row,
    ) -> dict[str, Any]:
        result = dict(row)

        raw_data = result.get("data")

        if isinstance(raw_data, str):
            try:
                result["data"] = json.loads(raw_data)
            except json.JSONDecodeError:
                pass

        return result

    def _validate_table(
        self,
        table: str,
    ) -> None:
        if table not in self.ALLOWED_TABLES:
            raise ValueError(
                f"Unbekannte Persistence-Tabelle: {table}"
            )

    @staticmethod
    def _validate_limit(
        limit: int,
    ) -> None:
        if limit < 1:
            raise ValueError(
                "limit muss größer als 0 sein."
            )

    @staticmethod
    def _validate_timestamp(
        timestamp: str,
    ) -> None:
        try:
            datetime.fromisoformat(timestamp)
        except ValueError as exc:
            raise ValueError(
                f"Ungültiger ISO-8601-Zeitstempel: {timestamp}"
            ) from exc

    def save_factory_state(
        self,
        factory_state: dict[str, Any],
    ) -> int:
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
        connection = self._require_connection()

        self._validate_table(table)
        self._validate_limit(limit)

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
            self._decode_row(row)
            for row in rows
        ]

    def get_latest(
        self,
        table: str,
    ) -> dict[str, Any] | None:
        connection = self._require_connection()

        self._validate_table(table)

        row = connection.execute(
            f"""
            SELECT *
            FROM {table}
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

        if row is None:
            return None

        return self._decode_row(row)

    def get_by_id(
        self,
        table: str,
        record_id: int,
    ) -> dict[str, Any] | None:
        connection = self._require_connection()

        self._validate_table(table)

        if record_id < 1:
            raise ValueError(
                "record_id muss größer als 0 sein."
            )

        row = connection.execute(
            f"""
            SELECT *
            FROM {table}
            WHERE id = ?
            LIMIT 1
            """,
            (record_id,),
        ).fetchone()

        if row is None:
            return None

        return self._decode_row(row)

    def get_history_by_time(
        self,
        table: str,
        start_time: str,
        end_time: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        connection = self._require_connection()

        self._validate_table(table)
        self._validate_limit(limit)

        self._validate_timestamp(start_time)
        self._validate_timestamp(end_time)

        if start_time > end_time:
            raise ValueError(
                "start_time darf nicht nach end_time liegen."
            )

        rows = connection.execute(
            f"""
            SELECT *
            FROM {table}
            WHERE timestamp >= ?
              AND timestamp <= ?
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            (
                start_time,
                end_time,
                limit,
            ),
        ).fetchall()

        return [
            self._decode_row(row)
            for row in rows
        ]

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "persistence",
            "version": self.VERSION,
            "status": self.status,
            "database_path": str(
                self.database_path
            ),
            "tables": sorted(
                self.ALLOWED_TABLES
            ),
        }
