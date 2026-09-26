"""
AIHelixia Intelligence Engine
Intelligence Scenario Regression Tests
Version: 1.0.0
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

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
    Erstellt vorherigen und beobachteten Zustand
    für den Outcome-Learning-Test.
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


EXPECTED = {
    "normal": {
        "outcome": "unchanged",
        "outcome_success": False,
        "outcome_evaluation": "unchanged",
        "outcome_known": True,
        "feedback": "neutral",
        "signal": "review",
    },
    "light_anomaly": {
        "outcome": "improved",
        "outcome_success": True,
        "outcome_evaluation": "successful",
        "outcome_known": True,
        "feedback": "positive",
        "signal": "reinforce",
    },
    "thermal_mechanical": {
        "outcome": "improved",
        "outcome_success": True,
        "outcome_evaluation": "successful",
        "outcome_known": True,
        "feedback": "positive",
        "signal": "reinforce",
    },
    "critical_multi_signal": {
        "outcome": "degraded",
        "outcome_success": False,
        "outcome_evaluation": "unsuccessful",
        "outcome_known": True,
        "feedback": "negative",
        "signal": "adjust",
    },
    "critical_alarm": {
        "outcome": "unknown",
        "outcome_success": None,
        "outcome_evaluation": "execution_success_outcome_unknown",
        "outcome_known": False,
        "feedback": "pending",
        "signal": "review",
    },
}


def run_scenario(scenario: str) -> dict:
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
            action = result["action"]

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

            previous_state, observed_state = (
                build_observed_state(scenario)
            )

            outcome_result = engine.evaluate_outcome(
                previous_state=previous_state,
                observed_state=observed_state,
                action_result=action,
            )

            outcome = outcome_result["outcome"]
            outcome_evaluation = outcome_result["evaluation"]
            outcome_feedback = outcome_result["feedback"]
            learning_memory = outcome_result["learning_memory"]

            return {
                "scenario": scenario,
                "anomaly": anomaly.get("status"),
                "severity": anomaly.get("severity"),
                "root_cause": primary_type,
                "priority": primary_priority,
                "decision": decision.get("decision_type"),
                "action": action.get("action"),
                "evaluation": evaluation.get("evaluation"),
                "outcome": outcome.get("outcome"),
                "outcome_success": outcome.get("success"),
                "outcome_confidence": outcome.get("confidence"),
                "outcome_evaluation": outcome_evaluation.get(
                    "evaluation"
                ),
                "outcome_known": outcome_evaluation.get(
                    "outcome_known"
                ),
                "feedback": outcome_feedback.get(
                    "feedback_type"
                ),
                "signal": outcome_feedback.get(
                    "signal"
                ),
                "learning_memory_type": learning_memory.get(
                    "type"
                ),
            }

        finally:
            engine.stop()


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_intelligence_scenario_regression(scenario: str) -> None:
    result = run_scenario(scenario)
    expected = EXPECTED[scenario]

    assert result["outcome"] == expected["outcome"]
    assert (
        result["outcome_success"]
        == expected["outcome_success"]
    )
    assert (
        result["outcome_evaluation"]
        == expected["outcome_evaluation"]
    )
    assert (
        result["outcome_known"]
        == expected["outcome_known"]
    )
    assert result["feedback"] == expected["feedback"]
    assert result["signal"] == expected["signal"]

    assert result["outcome_confidence"] >= 0.0
    assert result["learning_memory_type"] == "outcome_learning"


def test_all_regression_scenarios_execute() -> None:
    results = [
        run_scenario(scenario)
        for scenario in SCENARIOS
    ]

    assert len(results) == 5
    assert {
        result["scenario"]
        for result in results
    } == set(SCENARIOS)
