from engine import AIHelixiaEngine


def test_energy_economic_outcome():
    engine = AIHelixiaEngine()

    previous_state = {
        "actual_cost_per_kwh": 0.18,
    }

    observed_state = {
        "actual_cost_per_kwh": 0.15,
    }

    economic_context = {
        "findings": [
            {
                "type": "energy_cost",
                "annual_kwh": 1_000_000,
                "benchmark_cost_per_kwh": 0.12,
                "economic_impact": 60_000.0,
                "savings_potential": 60_000.0,
            }
        ]
    }

    result = engine._calculate_economic_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        economic_context=economic_context,
    )

    assert result["status"] == "calculated"
    assert result["calculation_status"] == "realized"
    assert result["economic_type"] == "energy_cost"

    # (0.18 - 0.15) * 1,000,000 = 30,000
    assert result["realized_savings"] == 30_000.0

    # (0.15 - 0.12) * 1,000,000 = 30,000
    assert result["remaining_gap"] == 30_000.0

    assert result["savings_potential"] == 60_000.0
    assert result["realization_rate"] == 0.5


def test_maintenance_economic_outcome():
    engine = AIHelixiaEngine()

    previous_state = {
        "annual_maintenance_cost": 500_000.0,
    }

    observed_state = {
        "annual_maintenance_cost": 380_000.0,
    }

    economic_context = {
        "findings": [
            {
                "type": "maintenance_cost",
                "benchmark_maintenance_cost": 300_000.0,
                "economic_impact": 200_000.0,
                "savings_potential": 200_000.0,
            }
        ]
    }

    result = engine._calculate_economic_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        economic_context=economic_context,
    )

    assert result["status"] == "calculated"
    assert result["calculation_status"] == "realized"
    assert result["economic_type"] == "maintenance_cost"

    # 500,000 - 380,000 = 120,000
    assert result["realized_savings"] == 120_000.0

    # 380,000 - 300,000 = 80,000
    assert result["remaining_gap"] == 80_000.0

    assert result["savings_potential"] == 200_000.0
    assert result["realization_rate"] == 0.6


def test_inventory_economic_outcome():
    engine = AIHelixiaEngine()

    previous_state = {
        "average_inventory_value": 2_000_000.0,
    }

    observed_state = {
        "average_inventory_value": 1_600_000.0,
    }

    economic_context = {
        "findings": [
            {
                "type": "inventory_value",
                "target_inventory_value": 1_200_000.0,
                "carrying_cost_rate": 0.20,
                "economic_impact": 160_000.0,
                "savings_potential": 160_000.0,
            }
        ]
    }

    result = engine._calculate_economic_outcome(
        previous_state=previous_state,
        observed_state=observed_state,
        economic_context=economic_context,
    )

    assert result["status"] == "calculated"
    assert result["calculation_status"] == "realized"
    assert result["economic_type"] == "inventory_value"

    # Inventory reduction: 400,000
    # Economic value at 20% carrying cost = 80,000
    assert result["realized_savings"] == 80_000.0

    # Remaining excess inventory: 400,000
    # Remaining economic gap = 80,000
    assert result["remaining_gap"] == 80_000.0

    assert result["savings_potential"] == 160_000.0
    assert result["realization_rate"] == 0.5
