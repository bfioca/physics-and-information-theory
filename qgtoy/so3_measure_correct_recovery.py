"""Compare global SO(3) orientation risk with spin-1 measure-and-correct error."""

from __future__ import annotations

from math import isfinite, sqrt


def _validate_probability(name: str, value: float) -> None:
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0,1]")


def spin1_measure_correct_error_bounds(
    orientation_risk: float,
) -> dict[str, float | str]:
    """Bound normalized diamond error from unit-range chordal frame risk.

    For the spin-1 rotation representation, an orientation error ``h`` induces
    ``Ad_{U_1(h)}``.  Convexity and ``||U_1(h)-I||<=2 sin(theta/2)`` give the
    upper bound.  The maximally entangled Choi witness and
    ``Tr U_1(h)=chi_1(h)`` give the lower bound.
    """
    _validate_probability("orientation_risk", orientation_risk)
    lower = 8.0 * orientation_risk / 9.0
    upper = min(1.0, 2.0 * sqrt(orientation_risk))
    return {
        "orientation_chordal_risk_R": orientation_risk,
        "normalized_diamond_error_lower_bound": lower,
        "normalized_diamond_error_upper_bound": upper,
        "bound_formula": "(8/9) R <= epsilon_rec <= min(1,2 sqrt(R))",
    }


def sufficient_orientation_risk_for_recovery_error(
    target_recovery_error: float,
) -> float:
    """Risk sufficient for the constructed spin-1 correction channel."""
    _validate_probability("target_recovery_error", target_recovery_error)
    return target_recovery_error**2 / 4.0


def necessary_orientation_risk_ceiling_for_recovery_error(
    achieved_recovery_error: float,
) -> float:
    """Risk ceiling necessary if this measure-and-correct channel has error δ."""
    _validate_probability("achieved_recovery_error", achieved_recovery_error)
    return min(1.0, 9.0 * achieved_recovery_error / 8.0)


def spin1_measure_correct_recovery_certificate() -> dict[str, object]:
    """Audit the comparison over representative risk and error budgets."""
    risks = (0.0, 1.0e-4, 0.01, 0.25, 0.75, 1.0)
    records = tuple(spin1_measure_correct_error_bounds(risk) for risk in risks)
    target_errors = (0.01, 0.05, 0.1, 0.5, 1.0)
    sufficient_records = tuple(
        {
            "target_recovery_error": error,
            "sufficient_orientation_risk": (
                sufficient_orientation_risk_for_recovery_error(error)
            ),
            "certified_constructive_error_upper_bound": (
                spin1_measure_correct_error_bounds(
                    sufficient_orientation_risk_for_recovery_error(error)
                )["normalized_diamond_error_upper_bound"]
            ),
        }
        for error in target_errors
    )
    certified_claims = {
        "bounds_are_ordered": all(
            record["normalized_diamond_error_lower_bound"]
            <= record["normalized_diamond_error_upper_bound"]
            for record in records
        ),
        "zero_risk_gives_zero_error": (
            records[0]["normalized_diamond_error_upper_bound"] == 0.0
        ),
        "sufficient_risk_meets_every_target_error": all(
            record["certified_constructive_error_upper_bound"]
            <= record["target_recovery_error"] + 1.0e-15
            for record in sufficient_records
        ),
    }
    return {
        "goal": "SO(3) Orientation Estimation To Spin-1 Recovery Comparison",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "certified_claims": certified_claims,
        "risk_records": records,
        "sufficient_recovery_records": sufficient_records,
        "scope": (
            "spin-1 target, Haar-prior orientation estimator, and the declared "
            "measure-and-correct random-unitary channel; arbitrary coherent "
            "decoders and higher-spin targets are not covered"
        ),
    }
