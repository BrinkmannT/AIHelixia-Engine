"""
AIHelixia Intelligence Engine
Core Engine
Version: 0.1.1
"""

from providers.model_provider import ModelProvider


ENGINE_NAME = "AIHelixia Intelligence Engine"
ENGINE_VERSION = "0.1.1"


class AIHelixiaEngine:
    """
    Zentrale Engine von AIHelixia.

    V0.1.1:
    - Engine initialisieren
    - Status verwalten
    - Health Check
    - Model Provider integrieren
    """

    def __init__(self) -> None:

        self.name = ENGINE_NAME
        self.version = ENGINE_VERSION
        self.status = "created"

        self.model_provider = ModelProvider()

    def start(self) -> dict[str, str]:
        """Startet die Engine und lädt den Model Provider."""

        self.model_provider.load()

        self.status = "running"

        return self.get_status()

    def stop(self) -> dict[str, str]:
        """Stoppt die Engine."""

        self.status = "stopped"

        return self.get_status()

    def get_status(self) -> dict[str, str]:
        """Gibt den aktuellen Engine-Status zurück."""

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "model": self.model_provider.model_name,
            "device": self.model_provider.device,
            "model_status": self.model_provider.status,
        }

    def health(self) -> dict[str, str]:
        """Führt einen Health Check durch."""

        return {
            "engine": self.name,
            "version": self.version,
            "status": "healthy",
            "model_provider": self.model_provider.status,
        }

    def ask(
        self,
        prompt: str,
        max_new_tokens: int = 64,
    ) -> str:
        """Verarbeitet eine Anfrage über den Model Provider."""

        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )

        return self.model_provider.generate(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
        )


if __name__ == "__main__":

    engine = AIHelixiaEngine()

    print("=" * 60)
    print("AIHELIXIA INTELLIGENCE ENGINE")
    print("=" * 60)

    print("Starting engine...")

    status = engine.start()

    print(status)

    print()
    print("Health check:")

    print(engine.health())

    print()
    print("AI test:")

    response = engine.ask(
        "What is 125 * 8 + 50? Answer with only the number."
    )

    print(response)

    print("=" * 60)
    print("AIHELIXIA V0.1.1 READY")
    print("=" * 60)
