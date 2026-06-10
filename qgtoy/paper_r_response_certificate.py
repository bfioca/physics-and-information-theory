"""Paper-R response composition and predeclared viability decision."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from .dual_weighted_response_enclosure import (
    DirectedDualWeightedResponseInterval,
    certify_directed_dual_weighted_response_interval,
)
from .paper_r_state_transfer import (
    PaperRStateTransferCertificate,
    certify_paper_r_state_transfer,
)
from .validated_interval import RationalInterval


PaperRDecision = Literal[
    "GO",
    "TECHNICAL_NOTE",
    "REASSESS",
    "INCONCLUSIVE_STOP",
    "PIVOT",
]


@dataclass(frozen=True)
class PaperRResponseCertificate:
    """Fully composed coefficient interval and bounded-sprint decision."""

    dual_weighted: DirectedDualWeightedResponseInterval
    relative_radius: Fraction | None
    state_transfer: PaperRStateTransferCertificate
    interval_wrapping_is_dominant: bool
    physical_ambiguity_is_dominant: bool
    decision: PaperRDecision
    decision_reason: str
    leading_coefficient_theorem_certified: bool
    standalone_paper_margin_certified: bool


def _paper_r_decision(
    *,
    relative_radius: Fraction | None,
    excludes_zero: bool,
    interval_wrapping_is_dominant: bool,
    physical_ambiguity_is_dominant: bool,
) -> tuple[PaperRDecision, str]:
    if physical_ambiguity_is_dominant:
        return "PIVOT", "the dominant uncertainty is a physical-model ambiguity"
    if relative_radius is None:
        return "PIVOT", "the corrected estimator is centered at zero"
    if excludes_zero and relative_radius <= Fraction(3, 4):
        return "GO", "zero is excluded with the predeclared standalone-paper margin"
    if excludes_zero and relative_radius < 1:
        return (
            "TECHNICAL_NOTE",
            "zero is excluded, but the relative radius misses the GO margin",
        )
    if Fraction(1) <= relative_radius <= Fraction(3):
        if interval_wrapping_is_dominant:
            return "REASSESS", "one targeted wrapping refinement is permitted"
        return "PIVOT", "the unresolved width is not demonstrably interval wrapping"
    if Fraction(3) < relative_radius <= Fraction(10):
        return "INCONCLUSIVE_STOP", "the bounded sprint forbids a second general redesign"
    return "PIVOT", "the total radius exceeds ten times the corrected center"


def certify_paper_r_response(
    *,
    corrected_estimator: RationalInterval,
    primal_energy_dual_residual_upper: Fraction,
    adjoint_energy_dual_residual_upper: Fraction,
    interval_wrapping_is_dominant: bool,
    physical_ambiguity_is_dominant: bool = False,
) -> PaperRResponseCertificate:
    """Compose the coefficient theorem and apply the frozen sprint thresholds."""
    if not isinstance(interval_wrapping_is_dominant, bool):
        raise TypeError("interval_wrapping_is_dominant must be boolean")
    if not isinstance(physical_ambiguity_is_dominant, bool):
        raise TypeError("physical_ambiguity_is_dominant must be boolean")
    dual = certify_directed_dual_weighted_response_interval(
        corrected_estimate=corrected_estimator,
        primal_energy_dual_residual_upper=primal_energy_dual_residual_upper,
        adjoint_energy_dual_residual_upper=adjoint_energy_dual_residual_upper,
    )
    relative_radius = (
        dual.total_radius / abs(dual.corrected_center)
        if dual.corrected_center != 0
        else None
    )
    state = certify_paper_r_state_transfer(exterior_amplitude=dual.response)
    decision, reason = _paper_r_decision(
        relative_radius=relative_radius,
        excludes_zero=dual.excludes_zero,
        interval_wrapping_is_dominant=interval_wrapping_is_dominant,
        physical_ambiguity_is_dominant=physical_ambiguity_is_dominant,
    )
    return PaperRResponseCertificate(
        dual_weighted=dual,
        relative_radius=relative_radius,
        state_transfer=state,
        interval_wrapping_is_dominant=interval_wrapping_is_dominant,
        physical_ambiguity_is_dominant=physical_ambiguity_is_dominant,
        decision=decision,
        decision_reason=reason,
        leading_coefficient_theorem_certified=dual.excludes_zero,
        standalone_paper_margin_certified=decision == "GO",
    )
