"""
AIHelixia Intelligence Engine
Intelligence Scenario Test V0.1
"""

from __future__ import annotations

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


SCENARIOS = [
    "normal",
    "light_anomaly",
    "thermal_mechanical",
    "critical_multi_signal",
    "critical_alarm",
]


def main() -> None:

    engine = AIHelixiaEngine()
    engine.start()

    print()
    print("========================================")
    print(" AIHELIXIA INTELLIGENCE SCENARIO TEST")
    print("========================================")

    results = []

    for scenario in SCENARIOS:

        result = engine.process(
            build_input(scenario)
        )

        anomaly = result["reasoning"].get(
            "anomaly_analysis",
            {},
        )

        root_cause = result["root_cause"]
        decision = result["decision"]

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

        row = {
            "scenario": scenario,
            "anomaly": anomaly.get("status"),
            "severity": anomaly.get("severity"),
            "root_cause": primary_type,
            "priority": primary_priority,
            "decision": decision.get(
                "decision_type"
            ),
            "action": decision.get(
                "action"
            ),
        }

        results.append(row)

        print()
        print("----------------------------------------")
        print("SCENARIO:", scenario)
        print("----------------------------------------")
        print("Anomaly:", row["anomaly"])
        print("Severity:", row["severity"])
        print("Root Cause:", row["root_cause"])
        print("Priority:", row["priority"])
        print("Decision:", row["decision"])
        print("Action:", row["action"])

    engine.stop()

    print()
    print("========================================")
    print(" SCENARIO SUMMARY")
    print("========================================")

    print()

    for row in results:
        print(
            f"{row['scenario']:22} | "
            f"{str(row['anomaly']):18} | "
            f"{str(row['priority']):8} | "
            f"{str(row['decision']):20} | "
            f"{str(row['action'])}"
        )

    print()
    print("========================================")
    print(" TEST COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()
