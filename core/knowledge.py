"""
AIHelixia Intelligence Engine
Knowledge Layer
Version: 0.2.0
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class Knowledge:
    """
    Deterministische Knowledge-Schicht der AIHelixia Engine.

    Verantwortlichkeiten:
    - historische Memory-Einträge analysieren
    - vergleichbare Fälle erkennen
    - wiederkehrende Signal-/Outcome-Muster identifizieren
    - Signal-Outcome-Beziehungen ableiten
    - Evidence strukturiert bereitstellen

    Keine LLM-Abhängigkeit.
    Keine Prediction.
    Keine Decision.
    Keine Action.
    """

    VERSION = "0.2.0"

    def __init__(self) -> None:
        self.status = "created"
        self.analysis_count = 0
        self.last_analysis: dict[str, Any] | None = None

    def start(self) -> None:
        self.status = "running"

    def stop(self) -> None:
        self.status = "stopped"

    def analyze(
        self,
        memory_entries: list[dict[str, Any]],
    ) -> dict[str, Any]:
        self._require_running()

        if not isinstance(memory_entries, list):
            raise TypeError("memory_entries must be a list")

        valid_entries = [
            entry
            for entry in memory_entries
            if isinstance(entry, dict)
        ]

        signal_patterns = self._extract_signal_patterns(
            valid_entries
        )

        outcome_patterns = self._extract_outcome_patterns(
            valid_entries
        )

        machine_patterns = self._extract_machine_patterns(
            valid_entries
        )

        signal_outcome_patterns = (
            self._extract_signal_outcome_patterns(
                valid_entries
            )
        )

        self.analysis_count += 1

        result = {
            "version": self.VERSION,
            "status": (
                "knowledge_available"
                if valid_entries
                else "no_knowledge"
            ),
            "analysis_id": self.analysis_count,
            "memory_entry_count": len(valid_entries),
            "signal_patterns": signal_patterns,
            "outcome_patterns": outcome_patterns,
            "machine_patterns": machine_patterns,
            "signal_outcome_patterns": (
                signal_outcome_patterns
            ),
            "evidence": {
                "pattern_count": (
                    len(signal_patterns)
                    + len(outcome_patterns)
                    + len(machine_patterns)
                    + len(signal_outcome_patterns)
                ),
                "historical_data_available": bool(
                    valid_entries
                ),
                "signal_outcome_evidence_available": bool(
                    signal_outcome_patterns
                ),
            },
        }

        self.last_analysis = result

        return deepcopy(result)

    def query(
        self,
        memory_entries: list[dict[str, Any]],
        signal_types: list[str],
        machine_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Sucht deterministisch nach historischen Fällen,
        die zum aktuellen Signalbild passen.

        Die Query erzeugt keine Vorhersage und keine Entscheidung.
        Sie liefert ausschließlich historische Evidence.
        """

        normalized_signals = sorted(
            {
                str(signal).strip()
                for signal in signal_types
                if str(signal).strip()
            }
        )

        if not normalized_signals:
            return {
                "status": "no_query_signals",
                "query": {
                    "signals": [],
                    "machine_id": machine_id,
                },
                "matched_case_count": 0,
                "outcomes": {},
                "dominant_outcome": None,
                "support_count": 0,
                "evidence_strength": "none",
                "matched_cases": [],
            }

        matched_cases: list[dict[str, Any]] = []

        for entry in memory_entries:
            if not isinstance(entry, dict):
                continue

            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            entry_signals = data.get("signal_types", [])

            if not isinstance(entry_signals, list):
                continue

            normalized_entry_signals = sorted(
                {
                    str(signal).strip()
                    for signal in entry_signals
                    if str(signal).strip()
                }
            )

            if not all(
                signal in normalized_entry_signals
                for signal in normalized_signals
            ):
                continue

            if machine_id is not None:
                if data.get("machine_id") != machine_id:
                    continue

            matched_cases.append(
                {
                    "memory_type": entry.get("type"),
                    "machine_id": data.get("machine_id"),
                    "signals": normalized_entry_signals,
                    "outcome": data.get("outcome"),
                }
            )

        outcomes: dict[str, int] = {}

        for case in matched_cases:
            outcome = case.get("outcome")

            if not isinstance(outcome, str) or not outcome:
                continue

            outcomes[outcome] = outcomes.get(outcome, 0) + 1

        support_count = sum(outcomes.values())

        dominant_outcome = None
        dominant_outcome_count = 0

        if outcomes:
            dominant_outcome, dominant_outcome_count = max(
                outcomes.items(),
                key=lambda item: (item[1], item[0]),
            )

        dominant_outcome_ratio = (
            dominant_outcome_count / support_count
            if support_count > 0
            else None
        )

        if support_count >= 5:
            evidence_strength = "strong"
        elif support_count >= 2:
            evidence_strength = "moderate"
        elif support_count == 1:
            evidence_strength = "limited"
        else:
            evidence_strength = "none"

        return {
            "status": (
                "knowledge_available"
                if matched_cases
                else "no_matching_knowledge"
            ),
            "query": {
                "signals": normalized_signals,
                "machine_id": machine_id,
            },
            "matched_case_count": len(matched_cases),
            "outcomes": outcomes,
            "dominant_outcome": dominant_outcome,
            "dominant_outcome_ratio": dominant_outcome_ratio,
            "support_count": support_count,
            "evidence_strength": evidence_strength,
            "matched_cases": matched_cases,
        }

    def _extract_signal_patterns(
        self,
        entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        patterns: dict[tuple[str, ...], int] = {}

        for entry in entries:
            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            signal_types = data.get("signal_types")

            if not isinstance(signal_types, list):
                continue

            normalized = sorted({
                str(signal)
                for signal in signal_types
                if signal
            })

            if not normalized:
                continue

            key = tuple(normalized)
            patterns[key] = patterns.get(key, 0) + 1

        return [
            {
                "signals": list(signals),
                "support_count": count,
            }
            for signals, count in sorted(
                patterns.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

    def _extract_outcome_patterns(
        self,
        entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        outcomes: dict[str, int] = {}

        for entry in entries:
            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            outcome = data.get("outcome")

            if not outcome:
                continue

            outcome = str(outcome)
            outcomes[outcome] = outcomes.get(outcome, 0) + 1

        return [
            {
                "outcome": outcome,
                "support_count": count,
            }
            for outcome, count in sorted(
                outcomes.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

    def _extract_machine_patterns(
        self,
        entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        machines: dict[str, int] = {}

        for entry in entries:
            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            machine_id = data.get("machine_id")

            if machine_id:
                machine_id = str(machine_id)
                machines[machine_id] = (
                    machines.get(machine_id, 0) + 1
                )

            machine_list = data.get("machines")

            if not isinstance(machine_list, list):
                continue

            for machine in machine_list:
                if not isinstance(machine, dict):
                    continue

                machine_id = machine.get("id")

                if not machine_id:
                    continue

                machine_id = str(machine_id)
                machines[machine_id] = (
                    machines.get(machine_id, 0) + 1
                )

        return [
            {
                "machine_id": machine_id,
                "support_count": count,
            }
            for machine_id, count in sorted(
                machines.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

    def _extract_signal_outcome_patterns(
        self,
        entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Erkennt historische Beziehungen zwischen einer
        Signalkombination und dem anschließend gespeicherten
        Outcome.

        Beispiel:

            vibration_elevated + critical_alarm
                -> degraded
        """

        patterns: dict[
            tuple[str, ...],
            dict[str, int],
        ] = {}

        for entry in entries:
            data = entry.get("data", {})

            if not isinstance(data, dict):
                continue

            signal_types = data.get("signal_types")
            outcome = data.get("outcome")

            if not isinstance(signal_types, list):
                continue

            if not outcome:
                continue

            normalized_signals = sorted({
                str(signal)
                for signal in signal_types
                if signal
            })

            if not normalized_signals:
                continue

            signal_key = tuple(normalized_signals)

            if signal_key not in patterns:
                patterns[signal_key] = {}

            outcome_key = str(outcome)

            patterns[signal_key][outcome_key] = (
                patterns[signal_key].get(
                    outcome_key,
                    0,
                )
                + 1
            )

        result: list[dict[str, Any]] = []

        for signals, outcomes in sorted(
            patterns.items(),
            key=lambda item: (
                -sum(item[1].values()),
                item[0],
            ),
        ):
            support_count = sum(outcomes.values())

            dominant_outcome = max(
                outcomes,
                key=lambda outcome: (
                    outcomes[outcome],
                    outcome,
                ),
            )

            dominant_count = outcomes[
                dominant_outcome
            ]

            if support_count > 0:
                dominant_ratio = round(
                    dominant_count / support_count,
                    3,
                )
            else:
                dominant_ratio = 0.0

            if support_count >= 5:
                evidence_strength = "strong"
            elif support_count >= 2:
                evidence_strength = "moderate"
            else:
                evidence_strength = "limited"

            result.append(
                {
                    "signals": list(signals),
                    "outcomes": dict(
                        sorted(
                            outcomes.items(),
                            key=lambda item: (
                                -item[1],
                                item[0],
                            ),
                        )
                    ),
                    "support_count": support_count,
                    "dominant_outcome": dominant_outcome,
                    "dominant_outcome_count": (
                        dominant_count
                    ),
                    "dominant_outcome_ratio": (
                        dominant_ratio
                    ),
                    "evidence_strength": (
                        evidence_strength
                    ),
                }
            )

        return result

    def get_status(self) -> dict[str, Any]:
        return {
            "component": "knowledge",
            "version": self.VERSION,
            "status": self.status,
            "analysis_count": self.analysis_count,
        }

    def _require_running(self) -> None:
        if self.status != "running":
            raise RuntimeError(
                "Knowledge ist nicht gestartet. "
                "Bitte zuerst start() aufrufen."
            )
