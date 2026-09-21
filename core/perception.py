"""
AIHelixia Intelligence Engine
Perception Layer
Version: 0.2.0
"""

from __future__ import annotations

from typing import Any


class Perception:
    """
    Nimmt rohe Eingaben entgegen und wandelt sie
    in eine strukturierte Wahrnehmung der Engine um.

    V0.2.0:
    - Eingabevalidierung
    - Normalisierung
    - strukturierte Perception
    - keine LLM-Abhängigkeit
    """

    def __init__(self) -> None:
        self.status = "created"

    def start(self) -> None:
        """Startet die Perception-Schicht."""

        self.status = "running"

    def stop(self) -> None:
        """Stoppt die Perception-Schicht."""

        self.status = "stopped"

    def perceive(
        self,
        input_data: Any,
    ) -> dict[str, Any]:
        """
        Verarbeitet eine rohe Eingabe.

        Die Perception-Schicht interpretiert die Eingabe
        noch nicht fachlich. Sie strukturiert sie lediglich.
        """

        if input_data is None:
            raise ValueError(
                "Perception benötigt eine Eingabe."
            )

        if isinstance(input_data, str):
            normalized_input = input_data.strip()

            if not normalized_input:
                raise ValueError(
                    "Die Eingabe darf nicht leer sein."
                )

            input_type = "text"

        elif isinstance(input_data, dict):
            normalized_input = input_data.copy()
            input_type = "structured"

        else:
            normalized_input = input_data
            input_type = type(input_data).__name__

        return {
            "input": normalized_input,
            "input_type": input_type,
            "status": "perceived",
        }

    def get_status(self) -> dict[str, Any]:
        """Gibt den aktuellen Status zurück."""

        return {
            "component": "perception",
            "status": self.status,
        }