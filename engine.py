"""
AIHelixia Intelligence Engine
Core Engine
Version: 0.5.3
"""

from __future__ import annotations

from typing import Any

from core.action import Action
from core.decision import Decision
from core.economic_discovery import EconomicDiscovery
from core.value_prioritization import ValuePrioritization
from core.evaluation import Evaluation
from core.factory_input import FactoryInput
from core.feedback import Feedback
from core.knowledge import Knowledge
from core.memory import Memory
from core.outcome import Outcome
from core.perception import Perception
from core.persistence import Persistence
from core.prediction import Prediction
from core.reasoning import Reasoning
from core.root_cause import RootCause
from core.world_state import WorldState
from providers.model_provider import ModelProvider


class AIHelixiaEngine:
    """
    Zentrale Orchestrierung der AIHelixia Intelligence Engine.

    Pipeline:

    Input
        ↓
    Perception
        ↓
    World State
        ↓
    Persistence
        ↓
    Memory Retrieval
        ↓
    Knowledge
        ↓
    Reasoning
        ↓
    Prediction
        ↓
    Root Cause
        ↓
    Economic Discovery
        ↓
    Decision
        ↓
    Action
        ↓
    Evaluation
        ↓
    Feedback
        ↓
    Memory
        ↓
    Persistence
        ↺
    """

    VERSION = "0.5.3"

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        model_device: str = "auto",
        database_path: str = "data/factoryiq.db",
    ) -> None:
        self.name = "AIHelixia Intelligence Engine"
        self.status = "created"

        self.model_provider = ModelProvider(
            model_name=model_name,
            device=model_device,
        )

        self.perception = Perception()
        self.factory_input = FactoryInput()
        self.world_state = WorldState()

        self.persistence = Persistence(
            database_path=database_path,
        )

        self.memory = Memory()
        self.knowledge = Knowledge()
        self.reasoning = Reasoning()
        self.prediction = Prediction()
        self.root_cause = RootCause()
        self.economic_discovery = EconomicDiscovery()
        self.value_prioritization = ValuePrioritization()
        self.decision = Decision()
        self.action = Action()
        self.evaluation = Evaluation()
        self.feedback = Feedback()
        self.outcome = Outcome()

        self.components = [
            "model_provider",
            "perception",
            "factory_input",
            "world_state",
            "persistence",
            "memory",
            "knowledge",
            "reasoning",
            "prediction",
            "root_cause",
            "economic_discovery",
            "value_prioritization",
            "decision",
            "action",
            "evaluation",
            "feedback",
            "outcome",
        ]

    def start(self) -> None:
        if self.status == "running":
            return

        self.persistence.start()

        self.perception.start()
        self.factory_input.start()
        self.world_state.start()

        restore_result = self._restore_latest_factory_state()

        self.memory.start()
        self.knowledge.start()
        self.reasoning.start()
        self.prediction.start()
        self.root_cause.start()
        self.economic_discovery.start()
        self.value_prioritization.start()
        self.decision.start()
        self.action.start()
        self.evaluation.start()
        self.feedback.start()
        self.outcome.start()

        if self.model_provider.status != "loaded":
            self.model_provider.load()

        self.status = "running"

        self.persistence.save_engine_event(
            "engine_started",
            {
                "engine_version": self.VERSION,
                "components": self.components,
                "factory_restore": restore_result,
            },
        )

    def _restore_latest_factory_state(self) -> dict[str, object]:
        """
        Stellt den zuletzt gespeicherten FactoryIQ-Zustand
        im WorldState wieder her.
        """

        history = self.persistence.get_history(
            "factory_states",
            limit=1,
        )

        if not history:
            return {
                "status": "no_persisted_factory_state",
                "restored": False,
            }

        latest = history[0]

        if not isinstance(latest, dict):
            return {
                "status": "invalid_persisted_factory_state",
                "restored": False,
            }

        persisted_data = latest.get(
            "data",
            {},
        )

        if not isinstance(
            persisted_data,
            dict,
        ):
            return {
                "status": "invalid_persisted_factory_data",
                "restored": False,
            }

        factory_data = {
            field: persisted_data[field]
            for field in (
                "factory",
                "production_lines",
                "machines",
                "sensors",
                "production",
                "energy",
                "maintenance",
                "alarms",
            )
            if field in persisted_data
        }

        if not factory_data:
            return {
                "status": "empty_persisted_factory_data",
                "restored": False,
            }

        restore_result = self.factory_input.ingest(
            factory_data=factory_data,
            world_state=self.world_state,
        )

        return {
            "status": "restored",
            "restored": True,
            "source_id": latest.get("id"),
            "factory_id": (
                persisted_data.get(
                    "factory",
                    {},
                ).get("id")
                if isinstance(
                    persisted_data.get("factory"),
                    dict,
                )
                else None
            ),
            "processed": restore_result.get(
                "processed",
                {},
            ),
        }

    def stop(self) -> None:
        if self.status == "stopped":
            return

        if self.persistence.status == "running":
            self.persistence.save_engine_event(
                "engine_stopped",
                {
                    "engine_version": self.VERSION,
                },
            )

        self.feedback.stop()
        self.outcome.stop()
        self.evaluation.stop()
        self.action.stop()
        self.decision.stop()
        self.value_prioritization.stop()
        self.economic_discovery.stop()
        self.root_cause.stop()
        self.prediction.stop()
        self.reasoning.stop()
        self.knowledge.stop()
        self.memory.stop()
        self.world_state.stop()
        self.factory_input.stop()
        self.perception.stop()
        self.persistence.stop()

        self.status = "stopped"

    def ingest_factory_data(
        self,
        factory_data: dict[str, object],
    ) -> dict[str, object]:
        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        result = self.factory_input.ingest(
            factory_data=factory_data,
            world_state=self.world_state,
        )

        factory_state = self.world_state.get_state()

        self.persistence.save_factory_state(
            factory_state,
        )

        for alarm in factory_state.get(
            "alarms",
            [],
        ):
            if isinstance(
                alarm,
                dict,
            ):
                self.persistence.save_alarm(
                    alarm,
                )

        self.persistence.save_engine_event(
            "factory_data_ingested",
            {
                "factory_input": result,
                "world_state": self.world_state.get_status(),
            },
        )

        return result

    def process(
        self,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        if self.status != "running":
            raise RuntimeError(
                "AIHelixia Engine ist nicht gestartet."
            )

        # ---------------------------------------------------------
        # 1. Factory Input Detection
        # ---------------------------------------------------------

        is_factory_input = (
            isinstance(input_data, dict)
            and "factory" in input_data
            and "machines" in input_data
            and "sensors" in input_data
            and "alarms" in input_data
        )

        factory_ingest_result = None

        if is_factory_input:
            factory_ingest_result = (
                self.ingest_factory_data(
                    input_data
                )
            )

        # ---------------------------------------------------------
        # 2. Perception
        # ---------------------------------------------------------

        perception_result = self.perception.perceive(
            input_data,
        )

        # ---------------------------------------------------------
        # 3. World State
        # ---------------------------------------------------------

        if is_factory_input:
            world_state = self.world_state.get_state()

        else:
            observation = perception_result.get(
                "observation",
                input_data,
            )

            if isinstance(
                observation,
                dict,
            ):
                self.world_state.add_observation(
                    observation,
                )

            world_state = self.world_state.get_state()

        # ---------------------------------------------------------
        # 4. Persistence
        # ---------------------------------------------------------

        self.persistence.save_factory_state(
            world_state,
        )

        self.persistence.save_engine_event(
            "observation_received",
            {
                "input": input_data,
                "perception": perception_result,
                "factory_ingest": factory_ingest_result,
            },
        )

        # ---------------------------------------------------------
        # 5. Memory
        # ---------------------------------------------------------

        if is_factory_input:
            memory_type = "factory_state"
            memory_data = world_state

        else:
            memory_type = "observation"
            memory_data = perception_result.get(
                "observation",
                input_data,
            )

        self.memory.store(
            memory_type,
            memory_data,
        )

        memory_result = self.memory.retrieve()

        # ---------------------------------------------------------
        # 6. Knowledge
        # ---------------------------------------------------------

        knowledge_result = self.knowledge.analyze(
            memory_result,
        )

        # ---------------------------------------------------------
        # 7. Reasoning
        # ---------------------------------------------------------

        reasoning_result = self.reasoning.analyze(
            world_state,
            memory_result,
        )

        # ---------------------------------------------------------
        # 8. Knowledge Query
        # ---------------------------------------------------------

        anomaly_analysis = reasoning_result.get(
            "anomaly_analysis",
            {},
        )

        signal_types = anomaly_analysis.get(
            "signal_types",
            [],
        )

        if not isinstance(
            signal_types,
            list,
        ):
            signal_types = []

        knowledge_query_result = self.knowledge.query(
            memory_entries=memory_result,
            signal_types=signal_types,
        )

        # ---------------------------------------------------------
        # 9. Prediction
        # ---------------------------------------------------------

        prediction_result = self.prediction.predict(
            world_state,
            reasoning_result,
        )

        # ---------------------------------------------------------
        # 10. Root Cause Analysis
        # ---------------------------------------------------------

        root_cause_result = self.root_cause.analyze(
            reasoning=reasoning_result,
            prediction=prediction_result,
            knowledge=knowledge_query_result,
        )

        # ---------------------------------------------------------
        # 11. Economic Discovery
        # ---------------------------------------------------------

        economic_discovery_input = input_data.get(
            "economic_discovery"
        )

        economic_discovery_result = None

        if isinstance(
            economic_discovery_input,
            dict,
        ):
            economic_discovery_result = (
                self.economic_discovery.analyze(
                    economic_discovery_input,
                )
            )

        # ---------------------------------------------------------
        # 11a. Value Prioritization
        # ---------------------------------------------------------

        value_prioritization_result = None

        if economic_discovery_result is not None:
            value_prioritization_result = (
                self.value_prioritization.prioritize(
                    economic_discovery_result,
                )
            )

        # ---------------------------------------------------------
        # 12. Decision
        # ---------------------------------------------------------

        decision_result = self.decision.decide(
            reasoning_result,
            prediction_result,
            root_cause_result,
            economic_discovery_result,
        )

        # ---------------------------------------------------------
        # 13. Memory
        # ---------------------------------------------------------

        self.memory.store(
            "decision",
            decision_result,
        )

        if economic_discovery_result is not None:
            self.memory.store(
                "economic_discovery",
                economic_discovery_result,
            )

        if value_prioritization_result is not None:
            self.memory.store(
                "value_prioritization",
                value_prioritization_result,
            )

        # ---------------------------------------------------------
        # 14. Action
        # ---------------------------------------------------------

        action_result = self.action.execute(
            decision_result,
        )

        # ---------------------------------------------------------
        # 15. Evaluation
        # ---------------------------------------------------------

        evaluation_result = self.evaluation.evaluate(
            action_result=action_result,
        )

        # ---------------------------------------------------------
        # 16. Feedback
        # ---------------------------------------------------------

        feedback_result = self.feedback.process(
            evaluation_result,
        )

        # ---------------------------------------------------------
        # 17. Memory
        # ---------------------------------------------------------

        self.memory.store(
            "evaluation",
            evaluation_result,
        )

        self.memory.store(
            "feedback",
            feedback_result,
        )

        # ---------------------------------------------------------
        # 18. Persistence
        # ---------------------------------------------------------

        self.persistence.save_ai_result(
            "reasoning",
            reasoning_result,
        )

        self.persistence.save_ai_result(
            "prediction",
            prediction_result,
        )

        self.persistence.save_ai_result(
            "root_cause",
            root_cause_result,
        )

        if economic_discovery_result is not None:
            self.persistence.save_ai_result(
                "economic_discovery",
                economic_discovery_result,
            )

        if value_prioritization_result is not None:
            self.persistence.save_ai_result(
                "value_prioritization",
                value_prioritization_result,
            )

        self.persistence.save_ai_result(
            "decision",
            decision_result,
        )

        self.persistence.save_ai_result(
            "action",
            action_result,
        )

        self.persistence.save_ai_result(
            "evaluation",
            evaluation_result,
        )

        self.persistence.save_ai_result(
            "feedback",
            feedback_result,
        )

        # ---------------------------------------------------------
        # 19. Closed Loop Event
        # ---------------------------------------------------------

        self.persistence.save_engine_event(
            "closed_loop_completed",
            {
                "reasoning": reasoning_result,
                "prediction": prediction_result,
                "root_cause": root_cause_result,
                "economic_discovery": (
                    economic_discovery_result
                ),
                "value_prioritization": (
                    value_prioritization_result
                ),
                "decision": decision_result,
                "action": action_result,
                "evaluation": evaluation_result,
                "feedback": feedback_result,
            },
        )

        # ---------------------------------------------------------
        # Final Result
        # ---------------------------------------------------------

        return {
            "status": "completed",
            "factory_ingest": factory_ingest_result,
            "perception": perception_result,
            "world_state": world_state,
            "memory": memory_result,
            "knowledge": knowledge_result,
            "knowledge_query": knowledge_query_result,
            "reasoning": reasoning_result,
            "prediction": prediction_result,
            "root_cause": root_cause_result,
            "economic_discovery": (
                economic_discovery_result
            ),
            "value_prioritization": (
                value_prioritization_result
            ),
            "decision": decision_result,
            "action": action_result,
            "evaluation": evaluation_result,
            "feedback": feedback_result,
        }

    def evaluate_outcome(
        self,
        previous_state: dict,
        observed_state: dict,
        action_result: dict,
        economic_context: dict | None = None,
    ) -> dict:
        """
        Verarbeitet einen beobachteten Outcome nach einer Action.

        Pipeline:

        previous_state
            ↓
        observed_state
            ↓
        Outcome
            ↓
        Evaluation
            ↓
        Feedback
            ↓
        Learning Memory
        """

        outcome_result = self.outcome.evaluate(
            previous_state=previous_state,
            observed_state=observed_state,
        )

        evaluation_result = self.evaluation.evaluate(
            action_result=action_result,
            outcome_result=outcome_result,
        )

        feedback_result = self.feedback.process(
            evaluation_result,
        )

        # ---------------------------------------------------------
        # Economic Outcome
        # ---------------------------------------------------------

        economic_outcome = self._calculate_economic_outcome(
            previous_state=previous_state,
            observed_state=observed_state,
            economic_context=economic_context,
        )

        # ---------------------------------------------------------
        # Outcome Learning Memory
        # ---------------------------------------------------------

        learning_memory = {
            "type": "outcome_learning",
            "outcome": outcome_result.get(
                "outcome"
            ),
            "outcome_success": outcome_result.get(
                "success"
            ),
            "outcome_confidence": outcome_result.get(
                "confidence"
            ),
            "evaluation": evaluation_result.get(
                "evaluation"
            ),
            "evaluation_score": evaluation_result.get(
                "score"
            ),
            "feedback_type": feedback_result.get(
                "feedback_type"
            ),
            "learning_signal": feedback_result.get(
                "signal"
            ),
            "recommendation": feedback_result.get(
                "recommendation"
            ),
            "economic_outcome": economic_outcome,
        }

        self.memory.store(
            "outcome_learning",
            learning_memory,
        )

        return {
            "outcome": outcome_result,
            "economic_outcome": economic_outcome,
            "evaluation": evaluation_result,
            "feedback": feedback_result,
            "learning_memory": learning_memory,
        }

    @staticmethod
    def _calculate_economic_outcome(
        previous_state: dict,
        observed_state: dict,
        economic_context: dict | None,
    ) -> dict:
        """
        Berechnet den tatsächlich realisierten wirtschaftlichen Outcome.

        Regeln:
        - Economic Impact != Savings Potential
        - Savings Potential != Realized Savings
        - Realized Savings werden ausschließlich aus beobachteten
          Zustandsdaten berechnet.
        - ROI wird nur berechnet, wenn echte Implementierungskosten
          vorliegen.
        - Ohne Economic Context wird kein wirtschaftlicher Wert erfunden.
        """

        if not isinstance(economic_context, dict):
            return {
                "status": "not_available",
                "calculation_status": "no_economic_context",
                "economic_impact": None,
                "savings_potential": None,
                "realized_savings": None,
                "realization_rate": None,
                "remaining_gap": None,
                "implementation_cost": None,
                "roi": None,
            }

        findings = economic_context.get("findings", [])

        if not isinstance(findings, list) or not findings:
            return {
                "status": "not_available",
                "calculation_status": "no_economic_finding",
                "economic_impact": None,
                "savings_potential": None,
                "realized_savings": None,
                "realization_rate": None,
                "remaining_gap": None,
                "implementation_cost": None,
                "roi": None,
            }

        finding = findings[0]

        if not isinstance(finding, dict):
            return {
                "status": "not_available",
                "calculation_status": "invalid_economic_finding",
                "economic_impact": None,
                "savings_potential": None,
                "realized_savings": None,
                "realization_rate": None,
                "remaining_gap": None,
                "implementation_cost": None,
                "roi": None,
            }

        finding_type = finding.get("type")

        # ---------------------------------------------------------
        # Economic Outcome Model
        # ---------------------------------------------------------
        # Jeder Economic-Type definiert:
        # - welche Zustandswerte benötigt werden
        # - wie Realized Savings berechnet werden
        # - wie die verbleibende wirtschaftliche Lücke berechnet wird
        #
        # Die Engine bleibt dabei branchenneutral.
        # ---------------------------------------------------------

        if finding_type == "procurement_cost":
            annual_volume = finding.get("annual_volume")
            benchmark_cost = finding.get("benchmark_cost")
            previous_cost = previous_state.get("actual_cost")
            observed_cost = observed_state.get("actual_cost")

            numeric_values = (
                annual_volume,
                benchmark_cost,
                previous_cost,
                observed_cost,
            )

            if not all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                for value in numeric_values
            ):
                return {
                    "status": "not_available",
                    "calculation_status": "insufficient_observed_data",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            if annual_volume < 0:
                return {
                    "status": "not_available",
                    "calculation_status": "invalid_annual_volume",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            realized_savings = round(
                (previous_cost - observed_cost) * annual_volume,
                2,
            )

            remaining_gap = round(
                (observed_cost - benchmark_cost) * annual_volume,
                2,
            )

        elif finding_type == "energy_cost":
            annual_kwh = finding.get("annual_kwh")
            benchmark_cost_per_kwh = finding.get(
                "benchmark_cost_per_kwh"
            )
            previous_cost_per_kwh = previous_state.get(
                "actual_cost_per_kwh"
            )
            observed_cost_per_kwh = observed_state.get(
                "actual_cost_per_kwh"
            )

            numeric_values = (
                annual_kwh,
                benchmark_cost_per_kwh,
                previous_cost_per_kwh,
                observed_cost_per_kwh,
            )

            if not all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                for value in numeric_values
            ):
                return {
                    "status": "not_available",
                    "calculation_status": "insufficient_observed_data",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            if annual_kwh < 0:
                return {
                    "status": "not_available",
                    "calculation_status": "invalid_annual_volume",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            realized_savings = round(
                (
                    previous_cost_per_kwh
                    - observed_cost_per_kwh
                ) * annual_kwh,
                2,
            )

            remaining_gap = round(
                (
                    observed_cost_per_kwh
                    - benchmark_cost_per_kwh
                ) * annual_kwh,
                2,
            )

        elif finding_type == "maintenance_cost":
            benchmark_maintenance_cost = finding.get(
                "benchmark_maintenance_cost"
            )
            previous_maintenance_cost = previous_state.get(
                "annual_maintenance_cost"
            )
            observed_maintenance_cost = observed_state.get(
                "annual_maintenance_cost"
            )

            numeric_values = (
                benchmark_maintenance_cost,
                previous_maintenance_cost,
                observed_maintenance_cost,
            )

            if not all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                for value in numeric_values
            ):
                return {
                    "status": "not_available",
                    "calculation_status": "insufficient_observed_data",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            realized_savings = round(
                previous_maintenance_cost
                - observed_maintenance_cost,
                2,
            )

            remaining_gap = round(
                observed_maintenance_cost
                - benchmark_maintenance_cost,
                2,
            )

        elif finding_type == "inventory_value":
            target_inventory_value = finding.get(
                "target_inventory_value"
            )
            carrying_cost_rate = finding.get(
                "carrying_cost_rate"
            )
            previous_inventory_value = previous_state.get(
                "average_inventory_value"
            )
            observed_inventory_value = observed_state.get(
                "average_inventory_value"
            )

            numeric_values = (
                target_inventory_value,
                carrying_cost_rate,
                previous_inventory_value,
                observed_inventory_value,
            )

            if not all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                for value in numeric_values
            ):
                return {
                    "status": "not_available",
                    "calculation_status": "insufficient_observed_data",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            if carrying_cost_rate < 0:
                return {
                    "status": "not_available",
                    "calculation_status": "invalid_carrying_cost_rate",
                    "economic_type": finding_type,
                    "economic_impact": finding.get("economic_impact"),
                    "savings_potential": finding.get("savings_potential"),
                    "realized_savings": None,
                    "realization_rate": None,
                    "remaining_gap": None,
                    "implementation_cost": None,
                    "roi": None,
                }

            realized_savings = round(
                (
                    previous_inventory_value
                    - observed_inventory_value
                ) * carrying_cost_rate,
                2,
            )

            remaining_gap = round(
                (
                    observed_inventory_value
                    - target_inventory_value
                ) * carrying_cost_rate,
                2,
            )

        else:
            return {
                "status": "not_available",
                "calculation_status": "unsupported_economic_type",
                "economic_type": finding_type,
                "economic_impact": finding.get("economic_impact"),
                "savings_potential": finding.get("savings_potential"),
                "realized_savings": None,
                "realization_rate": None,
                "remaining_gap": None,
                "implementation_cost": None,
                "roi": None,
            }

        savings_potential = finding.get(
            "savings_potential"
        )

        # Einheitliche Outcome-Darstellung über alle
        # Economic-Outcome-Typen hinweg.
        if finding_type == "procurement_cost":
            baseline_value = previous_cost
            observed_value = observed_cost
            benchmark_value = benchmark_cost
            volume_value = annual_volume
            metric_name = "actual_cost"

        elif finding_type == "energy_cost":
            baseline_value = previous_cost_per_kwh
            observed_value = observed_cost_per_kwh
            benchmark_value = benchmark_cost_per_kwh
            volume_value = annual_kwh
            metric_name = "actual_cost_per_kwh"

        elif finding_type == "maintenance_cost":
            baseline_value = previous_maintenance_cost
            observed_value = observed_maintenance_cost
            benchmark_value = benchmark_maintenance_cost
            volume_value = None
            metric_name = "annual_maintenance_cost"

        elif finding_type == "inventory_value":
            baseline_value = previous_inventory_value
            observed_value = observed_inventory_value
            benchmark_value = target_inventory_value
            volume_value = None
            metric_name = "average_inventory_value"

        else:
            baseline_value = None
            observed_value = None
            benchmark_value = None
            volume_value = None
            metric_name = None

        realization_rate = None

        if (
            isinstance(savings_potential, (int, float))
            and not isinstance(savings_potential, bool)
            and savings_potential > 0
        ):
            realization_rate = (
                realized_savings / savings_potential
            )

        implementation_cost = finding.get(
            "implementation_cost"
        )

        roi = None

        if (
            isinstance(implementation_cost, (int, float))
            and not isinstance(implementation_cost, bool)
            and implementation_cost > 0
        ):
            roi = (
                realized_savings - implementation_cost
            ) / implementation_cost

        return {
            "status": "calculated",
            "calculation_status": "realized",
            "economic_type": finding_type,
            "economic_impact": finding.get(
                "economic_impact"
            ),
            "savings_potential": savings_potential,
            "realized_savings": realized_savings,
            "realization_rate": realization_rate,
            "remaining_gap": remaining_gap,
            "implementation_cost": implementation_cost,
            "roi": roi,
            "baseline": {
                metric_name: baseline_value,
            },
            "observed": {
                metric_name: observed_value,
            },
            "benchmark": {
                metric_name: benchmark_value,
            },
            "volume": volume_value,
        }

    def get_status(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.VERSION,
            "status": self.status,
            "components": self.components,
            "economic_discovery": (
                self.economic_discovery.get_status()
            ),
        }
