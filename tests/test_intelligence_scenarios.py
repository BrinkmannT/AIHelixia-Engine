"""
AIHelixia Intelligence Engine
Intelligence Scenario Test V0.4
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from engine import AIHelixiaEngine


def build_input(scenario: str) -> dict:
    base = {
        "factory": {
            "id": f"FACTORY-{scenario.upper()}",
            "name": f"Scenario {scenario}",
            "location": "Schwedt",
            "status": "running",
        },
        "production_lines": [
            {
                "id": "LINE-001",
                "name": "Production Line 1",
                "status": "running",
            }
        ],
        "machines": [
            {
                "id": "MACHINE-001",
                "name": "Machine 1",
                "production_line_id": "LINE-001",
                "status": "running",
            }
        ],
        "sensors": [],
        "production": {
            "output": 150,
            "target": 150,
            "status": "running",
        },
        "energy": {
            "consumption": 420,
            "unit": "kWh",
            "status": "normal",
        },
        "maintenance": {
            "machine_id": "MACHINE-001",
            "status": "scheduled",
            "type": "preventive",
        },
        "alarms": [],
    }

    if scenario == "normal":
        base["sensors"] = [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
                "value": 65,
            },
            {
                "id": "SENSOR-VIB-001",
                "machine_id": "MACHINE-001",
                "type": "vibration",
                "unit": "mm/s",
                "value": 2.0,
            },
        ]

    elif scenario == "light_anomaly":
        base["sensors"] = [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
                "value": 82,
            },
            {
                "id": "SENSOR-VIB-001",
                "machine_id": "MACHINE-001",
                "type": "vibration",
                "unit": "mm/s",
                "value": 2.5,
            },
        ]

    elif scenario == "thermal_mechanical":
        base["sensors"] = [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
                "value": 86,
            },
            {
                "id": "SENSOR-VIB-001",
                "machine_id": "MACHINE-001",
                "type": "vibration",
                "unit": "mm/s",
                "value": 4.2,
            },
        ]

    elif scenario == "critical_multi_signal":
        base["sensors"] = [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
                "value": 86,
            },
            {
                "id": "SENSOR-VIB-001",
                "machine_id": "MACHINE-001",
                "type": "vibration",
                "unit": "mm/s",
                "value": 4.2,
            },
        ]

        base["production"] = {
            "output": 128,
            "target": 150,
            "status": "running",
        }

        base["energy"] = {
            "consumption": 490,
            "unit": "kWh",
            "status": "elevated",
        }

    elif scenario == "critical_alarm":
        base["sensors"] = [
            {
                "id": "SENSOR-TEMP-001",
                "machine_id": "MACHINE-001",
                "type": "temperature",
                "unit": "°C",
                "value": 65,
            }
        ]

        base["alarms"] = [
            {
                "id": "ALARM-CRITICAL-001",
                "timestamp": "2026-09-25T10:00:00+00:00",
                "machine_id": "MACHINE-001",
                "severity": "critical",
                "type": "safety",
                "message": "Critical machine alarm",
            }
        ]

    else:
        raise ValueError(
            f"Unbekanntes Szenario: {scenario}"
        )

    return base


def build_observed_state(scenario: str) -> tuple[dict, dict]:
    """
    Erstellt vorherigen und beobachteten Zustand für
    den Outcome-Learning-Test.

    Die Szenarien bilden unterschiedliche Outcomes ab:
    - normal → unchanged
    - light_anomaly → improved
    - thermal_mechanical → improved
    - critical_multi_signal → degraded
    - critical_alarm → unknown
    """

    previous = {
        "temperature": 80,
        "vibration": 4.0,
        "production": 140,
        "energy": 470,
    }

    if scenario == "normal":
        observed = {
            "temperature": 80,
            "vibration": 4.0,
            "production": 140,
            "energy": 470,
        }

    elif scenario == "light_anomaly":
        observed = {
            "temperature": 70,
            "vibration": 2.5,
            "production": 150,
            "energy": 430,
        }

    elif scenario == "thermal_mechanical":
        observed = {
            "temperature": 68,
            "vibration": 2.1,
            "production": 148,
            "energy": 430,
        }

    elif scenario == "critical_multi_signal":
        observed = {
            "temperature": 91,
            "vibration": 5.0,
            "production": 115,
            "energy": 520,
        }

    elif scenario == "critical_alarm":
        observed = {
            "temperature": None,
            "vibration": None,
            "production": None,
            "energy": None,
        }

    else:
        raise ValueError(
            f"Unbekanntes Szenario: {scenario}"
        )

    return previous, observed


SCENARIOS = [
    "normal",
    "light_anomaly",
    "thermal_mechanical",
    "critical_multi_signal",
    "critical_alarm",
]


def run_scenario(scenario: str) -> dict:
    """
    Führt das Szenario mit einer eigenen temporären
    Persistence-Datenbank aus.
    """

    with tempfile.TemporaryDirectory(
        prefix=f"aihelixia_{scenario}_"
    ) as temp_dir:

        database_path = str(
            Path(temp_dir) / "scenario.db"
        )

        engine = AIHelixiaEngine(
            database_path=database_path
        )

        try:
            engine.start()

            result = engine.process(
                build_input(scenario)
            )

            anomaly = result["reasoning"].get(
                "anomaly_analysis",
                {},
            )

            root_cause = result["root_cause"]
            decision = result["decision"]
            evaluation = result["evaluation"]
            feedback = result["feedback"]

            primary = root_cause.get(
                "primary_hypothesis"
            )

            primary_type = (
                primary.get("type")
                if isinstance(primary, dict)
                else None
            )

            primary_priority = (
                primary.get("priority")
                if isinstance(primary, dict)
                else None
            )

            # -----------------------------------------------------
            # Outcome Learning
            # -----------------------------------------------------

            previous_state, observed_state = (
                build_observed_state(scenario)
            )

            action_result = result["action"]

            outcome_result = engine.evaluate_outcome(
                previous_state=previous_state,
                observed_state=observed_state,
                action_result=action_result,
            )

            outcome = outcome_result["outcome"]
            outcome_evaluation = outcome_result["evaluation"]
            outcome_feedback = outcome_result["feedback"]

            return {
                "scenario": scenario,

                "anomaly": anomaly.get(
                    "status"
                ),

                "severity": anomaly.get(
                    "severity"
                ),

                "root_cause": primary_type,

                "priority": primary_priority,

                "decision": decision.get(
                    "decision_type"
                ),

                "action": decision.get(
                    "action"
                ),

                "evaluation": evaluation.get(
                    "evaluation"
                ),

                "outcome": outcome.get(
                    "outcome"
                ),

                "outcome_success": outcome.get(
                    "success"
                ),

                "outcome_confidence": outcome.get(
                    "confidence"
                ),

                "outcome_evaluation": outcome_evaluation.get(
                    "evaluation"
                ),

                "outcome_known": outcome_evaluation.get(
                    "outcome_known"
                ),

                "feedback": feedback.get(
                    "feedback_type"
                ),

                "signal": feedback.get(
                    "signal"
                ),

                "outcome_feedback": outcome_feedback.get(
                    "feedback_type"
                ),

                "outcome_signal": outcome_feedback.get(
                    "signal"
                ),
            }

        finally:
            engine.stop()


if __name__ == "__main__":

    print()
    print("AIHELIXIA INTELLIGENCE SCENARIOS V0.4")
    print("======================================")

    for scenario in SCENARIOS:

        result = run_scenario(scenario)

        print()
        print(result["scenario"])
        print("-" * len(result["scenario"]))

        print(
            "Anomaly:",
            result["anomaly"],
        )

        print(
            "Severity:",
            result["severity"],
        )

        print(
            "Root Cause:",
            result["root_cause"],
        )

        print(
            "Priority:",
            result["priority"],
        )

        print(
            "Decision:",
            result["decision"],
        )

        print(
            "Action:",
            result["action"],
        )

        print(
            "Outcome:",
            result["outcome"],
        )

        print(
            "Outcome Success:",
            result["outcome_success"],
        )

        print(
            "Outcome Confidence:",
            result["outcome_confidence"],
        )

        print(
            "Outcome Evaluation:",
            result["outcome_evaluation"],
        )

        print(
            "Outcome Known:",
            result["outcome_known"],
        )

        print(
            "Feedback:",
            result["outcome_feedback"],
        )

        print(
            "Learning Signal:",
            result["outcome_signal"],
        )

    print()
    print("SCENARIO TEST COMPLETE")
