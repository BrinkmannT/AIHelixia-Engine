"""
AIHelixia Intelligence Engine
Engine Core
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class EngineCore:
    """
    Zentrale Laufzeitverwaltung der AIHelixia Engine.

    Verantwortlichkeiten:
    - Engine initialisieren
    - Komponenten registrieren
    - Engine-Status verwalten
    - Komponentenstatus bereitstellen
    """

    def __init__(self) -> None:
        self.status = "created"
        self.components: dict[str, Any] = {}

    def register_component(
        self,
        name: str,
        component: Any,
    ) -> None:
        """Registriert eine Engine-Komponente."""

        if not name:
            raise ValueError(
                "Komponentenname darf nicht leer sein."
            )

        self.components[name] = component

    def start(self) -> None:
        """Startet den Engine Core."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt den Engine Core."""

        self.status = "stopped"

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Core-Status zurück."""

        return {
            "status": self.status,
            "components": list(self.components.keys()),
            "component_count": len(self.components),
        }

    def get_component(
        self,
        name: str,
    ) -> Any:
        """Gibt eine registrierte Komponente zurück."""

        if name not in self.components:
            raise KeyError(
                f"Komponente nicht registriert: {name}"
            )

        return self.components[name]