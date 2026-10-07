import pytest

from core.economic_discovery import EconomicDiscovery


def test_procurement_economic_impact():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 12.0,
                "benchmark_cost": 10.0,
                "benchmark_source": "validated_market_benchmark",
                "period": "2026",
                "supplier_count": 4,
                "comparable_volume": True,
                "verified": True,
            }
        }
    )

    assert result["finding_count"] == 1
    assert result["critical_count"] == 1
    assert result["total_economic_impact"] == 200000.0
    assert result["total_savings_potential"] is None

    finding = result["findings"][0]

    assert finding["economic_impact"] == 200000.0
    assert finding["savings_potential"] is None
    assert finding["realized_savings"] == 0.0
    assert finding["priority"] == "critical"
    assert finding["confidence"] == 99.0


def test_validated_realization_factor():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 12.0,
                "benchmark_cost": 10.0,
                "benchmark_source": "validated_market_benchmark",
                "period": "2026",
                "supplier_count": 4,
                "comparable_volume": True,
                "verified": True,
                "realization_factor": 0.75,
            }
        }
    )

    finding = result["findings"][0]

    assert finding["economic_impact"] == 200000.0
    assert finding["savings_potential"] == 150000.0
    assert finding["savings_status"] == (
        "estimated_from_validated_factor"
    )


def test_no_finding_when_benchmark_is_not_exceeded():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 10.0,
                "benchmark_cost": 10.0,
            }
        }
    )

    assert result["finding_count"] == 0
    assert result["total_economic_impact"] == 0.0
    assert result["total_savings_potential"] is None


def test_missing_data_does_not_invent_economic_impact():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 12.0,
            }
        }
    )

    finding = result["findings"][0]

    assert finding["calculation_status"] == (
        "insufficient_data"
    )
    assert finding["economic_impact"] is None
    assert finding["savings_potential"] is None


def test_invalid_realization_factor_is_not_used():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 12.0,
                "benchmark_cost": 10.0,
                "realization_factor": 1.5,
            }
        }
    )

    finding = result["findings"][0]

    assert finding["economic_impact"] == 200000.0
    assert finding["savings_potential"] is None
    assert finding["savings_status"] == "not_estimated"


def test_energy_economic_impact():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "energy": {
                "annual_kwh": 1000000,
                "actual_cost_per_kwh": 0.20,
                "benchmark_cost_per_kwh": 0.15,
                "benchmark_source": "validated_energy_benchmark",
                "period": "2026",
                "verified": True,
            }
        }
    )

    assert result["finding_count"] == 1
    assert result["total_economic_impact"] == pytest.approx(50000.0)

    finding = result["findings"][0]

    assert finding["type"] == "energy_cost"
    assert finding["economic_impact"] == pytest.approx(50000.0)
    assert finding["priority"] == "critical"
    assert finding["calculation_status"] == "calculated"


def test_maintenance_economic_impact():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "maintenance": {
                "annual_maintenance_cost": 500000,
                "benchmark_maintenance_cost": 400000,
                "benchmark_source": "validated_maintenance_benchmark",
                "period": "2026",
                "verified": True,
            }
        }
    )

    assert result["finding_count"] == 1
    assert result["total_economic_impact"] == 100000.0

    finding = result["findings"][0]

    assert finding["type"] == "maintenance_cost"
    assert finding["economic_impact"] == 100000.0
    assert finding["priority"] == "critical"
    assert finding["calculation_status"] == "calculated"


def test_inventory_carrying_cost():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "inventory": {
                "average_inventory_value": 2000000,
                "target_inventory_value": 1500000,
                "carrying_cost_rate": 0.12,
                "benchmark_source": "validated_inventory_model",
                "period": "2026",
                "verified": True,
            }
        }
    )

    assert result["finding_count"] == 1
    assert result["total_economic_impact"] == 60000.0

    finding = result["findings"][0]

    assert finding["type"] == "inventory_carrying_cost"
    assert finding["economic_impact"] == 60000.0
    assert finding["priority"] == "critical"
    assert finding["calculation_status"] == "calculated"


def test_multiple_economic_sources_are_aggregated():
    discovery = EconomicDiscovery()
    discovery.start()

    result = discovery.analyze(
        {
            "procurement": {
                "annual_volume": 100000,
                "actual_cost": 12.0,
                "benchmark_cost": 10.0,
            },
            "energy": {
                "annual_kwh": 1000000,
                "actual_cost_per_kwh": 0.20,
                "benchmark_cost_per_kwh": 0.15,
            },
            "maintenance": {
                "annual_maintenance_cost": 500000,
                "benchmark_maintenance_cost": 400000,
            },
            "inventory": {
                "average_inventory_value": 2000000,
                "target_inventory_value": 1500000,
                "carrying_cost_rate": 0.12,
            },
        }
    )

    assert result["finding_count"] == 4
    assert result["critical_count"] == 4
    assert result["total_economic_impact"] == 410000.0
    assert result["total_savings_potential"] is None

    finding_types = {
        finding["type"]
        for finding in result["findings"]
    }

    assert finding_types == {
        "procurement_cost",
        "energy_cost",
        "maintenance_cost",
        "inventory_carrying_cost",
    }
