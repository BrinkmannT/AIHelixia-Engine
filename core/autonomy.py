"""
AIHelixia Intelligence Engine
Autonomy Decision Gate
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


class Autonomy:
    """
    Kontrollierte Autonomie-Schicht zwischen Decision und Action.

    Die Autonomy-Schicht entscheidet ausschließlich,
    ob eine von Decision vorgeschlagene Aktion:

        - automatisch ausgeführt werden darf
        - menschliche Freigabe benötigt
        - blockiert werden muss

    Die Komponente führt selbst keine externen Aktionen aus.

    Zustände:

        AUTO
            Die Aktion darf automatisch an Action weitergegeben werden.

        APPROVAL_REQUIRED
            Die Aktion darf ohne Freigabe nicht ausgeführt werden.

        BLOCKED
            Die Aktion darf nicht ausgeführt werden.
    """

    VERSION = "0.1.0"

    AUTO = "auto"
    APPROVAL_REQUIRED = "approval_required"
    BLOCKED = "blocked"

    def __init__(self) -> None:
        self.status = "created"
        self.evaluation_count = 0
        self.last_evaluation: dict[str, Any] | None = None

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(self) -> None:
        if self.status == "running":
            return

        self.status = "running"

    def stop(self) -> None:
        if self.status == "stopped":
            return

        self.status = "stopped"

    # ---------------------------------------------------------
    # Evaluation
    # ---------------------------------------------------------

    def evaluate(
        self,
        decision: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Bewertet eine Decision und bestimmt deren Autonomie-Level.
        """

        if self.status != "running":
            raise RuntimeError(
                "Autonomy ist nicht gestartet."
            )

        if not isinstance(decision, dict):
            raise TypeError(
                "decision must be a dict."
            )

        self.evaluation_count += 1

        action = decision.get(
            "action",
            "observe",
        )

        decision_type = decision.get(
            "decision_type",
        )

        economic = decision.get(
            "economic",
            {},
        )

        value_prioritization = decision.get(
            "value_prioritization",
            {},
        )

        if not isinstance(economic, dict):
            economic = {}

        if not isinstance(
            value_prioritization,
            dict,
        ):
            value_prioritization = {}

        result = self._evaluate_action(
            action=action,
            decision_type=decision_type,
            economic=economic,
            value_prioritization=value_prioritization,
        )

        self.last_evaluation = result

        return result

    # ---------------------------------------------------------
    # Action Policy
    # ---------------------------------------------------------

    def _evaluate_action(
        self,
        action: Any,
        decision_type: Any,
        economic: dict[str, Any],
        value_prioritization: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Deterministische Autonomie-Regeln.

        Aktuell erlaubte automatische Aktionen:

            observe
            continue_monitoring

        review_strategy benötigt menschliche Freigabe.

        Unbekannte Aktionen werden blockiert.
        """

        # -----------------------------------------------------
        # Unknown action
        # -----------------------------------------------------

        if action not in {
            "observe",
            "continue_monitoring",
            "review_strategy",
        }:
            return self._build_result(
                level=self.BLOCKED,
                execution_allowed=False,
                approval_required=False,
                action=action,
                decision_type=decision_type,
                reason="unknown_action",
            )

        # -----------------------------------------------------
        # Safe internal actions
        # -----------------------------------------------------

        if action in {
            "observe",
            "continue_monitoring",
        }:
            return self._build_result(
                level=self.AUTO,
                execution_allowed=True,
                approval_required=False,
                action=action,
                decision_type=decision_type,
                reason="safe_internal_action",
            )

        # -----------------------------------------------------
        # Strategy changes require approval
        # -----------------------------------------------------

        if action == "review_strategy":
            reason = self._determine_approval_reason(
                economic=economic,
                value_prioritization=value_prioritization,
            )

            return self._build_result(
                level=self.APPROVAL_REQUIRED,
                execution_allowed=False,
                approval_required=True,
                action=action,
                decision_type=decision_type,
                reason=reason,
            )

        # -----------------------------------------------------
        # Defensive fallback
        # -----------------------------------------------------

        return self._build_result(
            level=self.BLOCKED,
            execution_allowed=False,
            approval_required=False,
            action=action,
            decision_type=decision_type,
            reason="autonomy_policy_blocked_action",
        )

    # ---------------------------------------------------------
    # Approval Reason
    # ---------------------------------------------------------

    def _determine_approval_reason(
        self,
        economic: dict[str, Any],
        value_prioritization: dict[str, Any],
    ) -> str:
        """
        Ermittelt transparent, warum eine Strategieänderung
        menschliche Freigabe benötigt.
        """

        economic_status = economic.get(
            "status",
        )

        economic_finding_count = self._safe_int(
            economic.get(
                "finding_count",
                0,
            )
        )

        critical_count = self._safe_int(
            economic.get(
                "critical_count",
                0,
            )
        )

        economic_confidence = self._safe_float(
            economic.get(
                "confidence",
                0.0,
            )
        )

        top_finding = value_prioritization.get(
            "top_finding",
            {},
        )

        if not isinstance(
            top_finding,
            dict,
        ):
            top_finding = {}

        value_priority = top_finding.get(
            "value_priority",
            top_finding.get(
                "priority",
            ),
        )

        value_priority_score = self._safe_float(
            top_finding.get(
                "priority_score",
                0.0,
            )
        )

        if economic_finding_count <= 0:
            return "economic_context_not_sufficient"

        if economic_status not in {
            None,
            "analysis_completed",
        }:
            return "economic_context_not_sufficient"

        if critical_count > 0:
            return "critical_economic_finding_requires_approval"

        if value_priority == "critical":
            return "critical_value_priority_requires_approval"

        if value_priority_score >= 85:
            return "high_value_score_requires_approval"

        if economic_confidence < 0.80:
            return "economic_confidence_below_autonomy_threshold"

        if not self._has_verified_economic_evidence(
            economic,
        ):
            return "economic_evidence_not_verified"

        return "strategy_change_requires_approval"

    # ---------------------------------------------------------
    # Evidence
    # ---------------------------------------------------------

    def _has_verified_economic_evidence(
        self,
        economic: dict[str, Any],
    ) -> bool:
        """
        Prüft, ob mindestens ein wirtschaftliches Finding
        explizit verifizierte Evidence enthält.
        """

        findings = economic.get(
            "findings",
            [],
        )

        if not isinstance(
            findings,
            list,
        ):
            return False

        for finding in findings:
            if not isinstance(
                finding,
                dict,
            ):
                continue

            evidence = finding.get(
                "evidence",
                [],
            )

            if not isinstance(
                evidence,
                list,
            ):
                continue

            for item in evidence:
                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                if item.get(
                    "verified"
                ) is True:
                    return True

        return False

    # ---------------------------------------------------------
    # Result
    # ---------------------------------------------------------

    def _build_result(
        self,
        level: str,
        execution_allowed: bool,
        approval_required: bool,
        action: Any,
        decision_type: Any,
        reason: str,
    ) -> dict[str, Any]:
        return {
            "status": "autonomy_evaluated",
            "version": self.VERSION,
            "evaluation_count": self.evaluation_count,
            "autonomy": level,
            "autonomy_level": level,
            "execution_allowed": execution_allowed,
            "approval_required": approval_required,
            "action": action,
            "decision_type": decision_type,
            "reason": reason,
        }

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def get_status(self) -> dict[str, Any]:
        return {
            "name": "Autonomy",
            "version": self.VERSION,
            "status": self.status,
            "evaluation_count": self.evaluation_count,
            "last_evaluation": self.last_evaluation,
        }

    # ---------------------------------------------------------
    # Safe parsing
    # ---------------------------------------------------------

    @staticmethod
    def _safe_int(
        value: Any,
    ) -> int:
        try:
            return int(value)
        except (
            TypeError,
            ValueError,
        ):
            return 0

    @staticmethod
    def _safe_float(
        value: Any,
    ) -> float:
        try:
            return float(value)
        except (
            TypeError,
            ValueError,
        ):
            return 0.0
