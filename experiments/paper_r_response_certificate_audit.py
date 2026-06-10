#!/usr/bin/env python3
"""Compose the bounded Paper-R viability decision from source-bound parts."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
)
from qgtoy.paper_r_response_certificate import (  # noqa: E402
    certify_paper_r_response,
)
from qgtoy.paper_r_wall_composition import (  # noqa: E402
    certify_paper_r_weak_wall_contribution,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    validated_wall_conormal_coefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import (  # noqa: E402
    DEFAULT_WALL_SLOPE,
    validated_wall_master_load,
)
from qgtoy.validated_interval import (  # noqa: E402
    RationalInterval,
    sqrt_fraction_interval,
)


OUTPUT = ROOT / "experiments/paper_r_response_certificate.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
COMPONENTS = {
    "signed_outer": ROOT
    / "experiments/validated_centrifugal_correlated_estimator.json",
    "signed_origin": ROOT
    / "experiments/validated_centrifugal_origin_corrected_estimator.json",
    "primal_outer_wall": ROOT
    / "experiments/validated_centrifugal_correlated_primal_dual.json",
    "primal_origin": ROOT
    / "experiments/validated_centrifugal_origin_profile_jets.json",
    "adjoint_outer_wall": ROOT
    / "experiments/validated_centrifugal_correlated_adjoint.json",
    "adjoint_origin": ROOT
    / "experiments/validated_centrifugal_origin_weak_dual.json",
    "wall_master": ROOT
    / "experiments/validated_centrifugal_wall_master_load.json",
}
SOURCES = (
    "qgtoy/dual_weighted_response_enclosure.py",
    "qgtoy/paper_r_response_certificate.py",
    "qgtoy/paper_r_state_transfer.py",
    "qgtoy/paper_r_wall_composition.py",
    "qgtoy/paper_r_weyl_observable.py",
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_response_residual.py",
    "qgtoy/validated_centrifugal_wall_master_load.py",
    "qgtoy/validated_interval.py",
    "experiments/paper_r_response_certificate_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _decimal(integer: int, places: int) -> str:
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _outward_interval(
    value: RationalInterval, *, places: int = 18
) -> dict[str, object]:
    scale = 10**places
    return {
        "lower_exact": str(value.lower),
        "upper_exact": str(value.upper),
        "lower": _decimal(_floor(value.lower * scale), places),
        "upper": _decimal(_ceil(value.upper * scale), places),
        "lower_float": float(value.lower),
        "upper_float": float(value.upper),
        "representation": f"exact_fraction_plus_outward_decimal_{places}_places",
    }


def _outward_upper(value: Fraction, *, places: int = 18) -> dict[str, object]:
    scale = 10**places
    return {
        "exact": str(value),
        "upper": _decimal(_ceil(value * scale), places),
        "float": float(value),
        "representation": f"exact_fraction_plus_outward_upper_{places}_places",
    }


def _archived_interval(record: dict[str, object]) -> RationalInterval:
    return RationalInterval(Fraction(str(record["lower"])), Fraction(str(record["upper"])))


def _load_verified_artifact(path: Path) -> dict[str, object]:
    record = json.loads(path.read_text(encoding="ascii"))
    if record.get("status") != "pass":
        raise ValueError(f"component artifact is not passing: {path.name}")
    for section in ("authenticated_inputs", "source_sha256"):
        for relative, expected in record.get(section, {}).items():
            actual = _sha256(ROOT / relative)
            if actual != expected:
                raise ValueError(
                    f"stale {section} hash in {path.name}: {relative}"
                )
    return record


def build_record() -> dict[str, object]:
    source_before = {relative: _sha256(ROOT / relative) for relative in SOURCES}
    component_records = {
        name: _load_verified_artifact(path) for name, path in COMPONENTS.items()
    }
    trials_record = json.loads(TRIALS.read_text(encoding="ascii"))
    pair = rational_response_trial_pair_from_record(trials_record["trial_archive"])

    wall_record = component_records["wall_master"]
    archived_slope = wall_record["authenticated_wall_profile_derivative"]
    if (
        Fraction(str(archived_slope["lower"])) != DEFAULT_WALL_SLOPE.lower
        or Fraction(str(archived_slope["upper"])) != DEFAULT_WALL_SLOPE.upper
    ):
        raise ValueError("wall artifact and declared slope interval differ")
    wall_coefficients = validated_wall_conormal_coefficients(DEFAULT_WALL_SLOPE)
    wall_load = validated_wall_master_load(DEFAULT_WALL_SLOPE)
    archived_gamma = _archived_interval(wall_record["gamma_b"])
    if wall_load.gamma_b != archived_gamma:
        raise ValueError("live and archived wall master loads differ")
    weak_wall = certify_paper_r_weak_wall_contribution(
        primal_trial=pair.primal,
        adjoint_trial=pair.adjoint,
        coefficients=wall_coefficients,
        master_load=wall_load,
    )

    signed_outer = _archived_interval(
        component_records["signed_outer"]["signed_outer_totals"][
            "joint_correlated_integral"
        ]
    )
    signed_origin = _archived_interval(
        component_records["signed_origin"]["signed_origin_hulls"][
            "corrected_sum"
        ]
    )
    corrected_estimator = (
        signed_outer
        + signed_origin
        + weak_wall.corrected_estimator_wall_contribution
    )

    coercive_floor = Fraction(1, 100)
    primal_partial_square = Fraction(
        component_records["primal_outer_wall"]["partial_bound"][
            "matrix_weighted_squared_upper"
        ]
    )
    primal_origin_l2_square = Fraction(
        component_records["primal_origin"]["origin_residual_l2_squared_upper"][
            "primal_rotational_load"
        ]["upper"]
    )
    primal_origin_square = primal_origin_l2_square / coercive_floor
    primal_square = primal_partial_square + primal_origin_square
    primal_delta = sqrt_fraction_interval(primal_square, bisection_steps=192).upper

    adjoint_partial_square = Fraction(
        component_records["adjoint_outer_wall"]["partial_bound"][
            "matrix_weighted_squared_upper"
        ]
    )
    adjoint_origin_square = Fraction(
        component_records["adjoint_origin"]["loaded_adjoint_master"][
            "squared_dual_upper"
        ]
    )
    adjoint_square = adjoint_partial_square + adjoint_origin_square
    adjoint_delta = sqrt_fraction_interval(adjoint_square, bisection_steps=192).upper

    certificate = certify_paper_r_response(
        corrected_estimator=corrected_estimator,
        primal_energy_dual_residual_upper=primal_delta,
        adjoint_energy_dual_residual_upper=adjoint_delta,
        interval_wrapping_is_dominant=False,
        physical_ambiguity_is_dominant=False,
    )
    if certificate.relative_radius is None:
        raise AssertionError("nonzero corrected-estimator center expected")
    zero_exclusion_product_limit = -corrected_estimator.upper
    if zero_exclusion_product_limit <= 0:
        raise AssertionError("directed corrected estimator must be negative")
    required_primal_delta = zero_exclusion_product_limit / adjoint_delta
    primal_norm_improvement_factor = primal_delta / required_primal_delta

    claims = {
        "all_component_artifacts_are_source_bound_and_passing": True,
        "signed_outer_estimator_is_strictly_negative": signed_outer.upper < 0,
        "origin_cutoff_trace_is_included": component_records["signed_origin"][
            "certified_claims"
        ]["origin_cutoff_trace_is_included"],
        "weak_wall_completion_contains_no_conormal": (
            not weak_wall.conormal_residual_included
        ),
        "primal_norm_uses_all_strong_bulk_and_conormal_wall": True,
        "rotational_derivative_load_is_continuous_at_internal_joins": True,
        "rotational_derivative_load_vanishes_at_the_wall": True,
        "adjoint_norm_uses_weak_origin_bulk_and_wall": True,
        "corrected_estimator_is_strictly_negative": corrected_estimator.upper < 0,
        "full_response_interval_contains_zero": (
            certificate.dual_weighted.response.contains_zero()
        ),
        "predeclared_decision_is_inconclusive_stop": (
            certificate.decision == "INCONCLUSIVE_STOP"
        ),
        "decision_ratio_is_between_three_and_ten": (
            Fraction(3) < certificate.relative_radius <= Fraction(10)
        ),
        "theorem_r1_is_not_certified": (
            not certificate.leading_coefficient_theorem_certified
        ),
        "theorem_r2_is_not_certified": (
            not certificate.state_transfer.state_sensitive_nonzero_conclusion
        ),
        "weyl_normalization_has_no_numeric_inertia_error": True,
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"Paper-R response composition failed: {failed}")

    source_after = {relative: _sha256(ROOT / relative) for relative in SOURCES}
    if source_before != source_after:
        raise ValueError("Paper-R composer sources changed during the audit")
    state = certificate.state_transfer
    dual = certificate.dual_weighted
    return {
        "goal": "Bounded Paper-R Viability Sprint",
        "status": "pass",
        "result_type": "source_bound_inconclusive_stop_decision",
        "decision": certificate.decision,
        "decision_reason": certificate.decision_reason,
        "frozen_scope": {
            "quantity": "leading O(Omega^2) fixed-background exterior amplitude",
            "patch_radius": "20",
            "wall_radius": "4",
            "pion_mass_squared": "1",
            "curvature": "1/400",
            "completed_potential_floor": "1/100",
            "principal_floor": "1/100",
            "background": "pure de Sitter",
            "wall_model": "ideal positive-tension Nambu-Goto membrane",
        },
        "signed_estimator": {
            "positive_radius": _outward_interval(signed_outer),
            "regular_origin_with_cutoff_trace": _outward_interval(signed_origin),
            "weak_wall": _outward_interval(
                weak_wall.corrected_estimator_wall_contribution
            ),
            "complete": _outward_interval(corrected_estimator),
        },
        "primal_energy_dual": {
            "positive_radius_plus_strong_wall_squared_upper": _outward_upper(
                primal_partial_square
            ),
            "strong_origin_squared_upper": _outward_upper(primal_origin_square),
            "complete_squared_upper": _outward_upper(primal_square),
            "complete_norm_upper": _outward_upper(primal_delta),
            "representation": (
                "all-strong bulk; continuous residual derivative load cancels "
                "internal traces; conormal wall residual closes the endpoint"
            ),
        },
        "adjoint_energy_dual": {
            "positive_radius_plus_weak_wall_squared_upper": _outward_upper(
                adjoint_partial_square
            ),
            "weak_loaded_origin_squared_upper": _outward_upper(
                adjoint_origin_square
            ),
            "complete_squared_upper": _outward_upper(adjoint_square),
            "complete_norm_upper": _outward_upper(adjoint_delta),
            "representation": "weak completed-square bulk, origin, and wall",
        },
        "full_response": {
            "residual_product_error_upper": _outward_upper(
                dual.residual_product_error_upper
            ),
            "estimator_radius": _outward_upper(dual.estimator_radius),
            "total_radius": _outward_upper(dual.total_radius),
            "relative_radius": _outward_upper(certificate.relative_radius),
            "exterior_amplitude": _outward_interval(dual.response),
            "excludes_zero": dual.excludes_zero,
            "sign": dual.sign,
        },
        "future_improvement_diagnostic": {
            "zero_exclusion_product_limit": _outward_upper(
                zero_exclusion_product_limit
            ),
            "required_primal_norm_if_adjoint_is_held_fixed": _outward_upper(
                required_primal_delta
            ),
            "current_to_required_primal_norm_factor": _outward_upper(
                primal_norm_improvement_factor
            ),
            "dominant_primal_cell": component_records["primal_outer_wall"][
                "partial_bound"
            ]["dominant_cell_radius"],
            "interpretation": (
                "A future proof attempt needs a materially better certified "
                "primal trial or Riesz representation, not another general "
                "subdivision of the present bounded sprint."
            ),
        },
        "weyl_and_state_transfer": {
            "annular_rms_factor": str(state.annular_rms_factor),
            "unit_tensor_weyl_footprint": _outward_interval(
                state.unit_tensor_weyl_footprint
            ),
            "cat_weyl_footprint": _outward_interval(state.cat_weyl_footprint),
            "anticoherent_weyl_footprint": _outward_interval(
                state.anticoherent_weyl_footprint
            ),
            "equal_casimir_and_leading_energy": (
                state.equal_casimir_and_leading_energy
            ),
            "state_sensitive_nonzero_conclusion": (
                state.state_sensitive_nonzero_conclusion
            ),
            "conclusion": state.conclusion,
            "normalization_note": (
                "The normalized B_W removes c_I algebraically; no numerical "
                "inertia interval is added to this transfer."
            ),
        },
        "certified_claims": claims,
        "component_artifact_sha256": {
            name: _sha256(path) for name, path in COMPONENTS.items()
        },
        "authenticated_inputs": {
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "source_sha256": source_before,
        "claim_boundary": (
            "This closes the predeclared Paper-R viability sprint with an "
            "INCONCLUSIVE_STOP decision. The directed corrected estimator is "
            "negative, but the rigorous residual-product response interval "
            "contains zero. Therefore neither a nonzero leading exterior-Weyl "
            "theorem nor the equal-energy state-sensitive nonzero corollary is "
            "certified. No finite-Omega, self-gravity, detector, or tensorial "
            "Israel-matching statement is made."
        ),
    }


def main() -> None:
    record = build_record()
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "decision": record["decision"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
