"""Compose the global centrifugal Friedrichs-form certificate."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_friedrichs_form import (
    certify_centrifugal_friedrichs_form,
)


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = ROOT / "experiments/centrifugal_skyrmion_liouville_origin_certificate.json"
OUTER = ROOT / "experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_friedrichs_form_certificate.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_friedrichs_form.py",
    "qgtoy/centrifugal_skyrmion_riccati_coercivity.py",
    "qgtoy/centrifugal_skyrmion_variational.py",
    "qgtoy/validated_centrifugal_global_form.py",
    "experiments/centrifugal_skyrmion_friedrichs_form_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    origin = json.loads(ORIGIN.read_text(encoding="ascii"))
    outer = json.loads(OUTER.read_text(encoding="ascii"))
    if not origin["summary"]["coercivity_verified"]:
        raise ValueError("origin coefficient certificate is not closed")
    if not outer["summary"]["coercivity_verified"]:
        raise ValueError("outer coefficient certificate is not closed")
    origin_target = Fraction(origin["parameters"]["target_lower_bound"])
    outer_target = Fraction(outer["parameters"]["target_lower_bound"])
    origin_split = Fraction(origin["parameters"]["origin_split_radius"])
    outer_split = Fraction(outer["parameters"]["origin_split_radius"])
    if origin_split != outer_split:
        raise ValueError("origin and outer coefficient domains do not join")
    wall_margin = Fraction(origin["wall_trace"]["margin"]["lower"])
    result = certify_centrifugal_friedrichs_form(
        wall_radius=Fraction(4),
        coefficient_split_radius=origin_split,
        origin_coercivity_lower_bound=origin_target,
        outer_coercivity_lower_bound=outer_target,
        origin_principal_lower_bound=min(
            Fraction(origin["summary"]["minimum_principal_radial"]),
            Fraction(origin["summary"]["minimum_principal_tangential"]),
        ),
        outer_principal_lower_bound=min(
            Fraction(outer["summary"]["minimum_principal_radial"]),
            Fraction(outer["summary"]["minimum_principal_tangential"]),
        ),
        wall_trace_margin_lower_bound=wall_margin,
    )
    return {
        "result_type": "centrifugal_skyrmion_global_friedrichs_form_audit",
        "input_artifacts": {
            str(ORIGIN.relative_to(ROOT)): _sha256(ORIGIN),
            str(OUTER.relative_to(ROOT)): _sha256(OUTER),
        },
        "theorem": {
            "wall_radius": str(result.wall_radius),
            "coefficient_split_radius": str(result.coefficient_split_radius),
            "coercivity_lower_bound": str(result.coercivity_lower_bound),
            "inverse_norm_upper_bound": str(result.inverse_norm_upper_bound),
            "hilbert_space": result.hilbert_space,
            "form_domain": result.form_domain,
            "half_line_domain": result.half_line_domain,
            "smooth_core": result.smooth_core,
            "origin_boundary_condition": result.origin_boundary_condition,
            "wall_boundary_conditions": result.wall_boundary_conditions,
            "coefficient_join_verified": result.coefficient_join_verified,
            "wall_trace_positive": result.wall_trace_positive,
            "form_norm_equivalent_to_weighted_sobolev_norm": (
                result.form_norm_equivalent_to_weighted_sobolev_norm
            ),
            "densely_defined": result.densely_defined,
            "symmetric": result.symmetric,
            "closed": result.closed,
            "self_adjoint_operator_exists": result.self_adjoint_operator_exists,
            "zero_in_resolvent": result.zero_in_resolvent,
            "two_sided_inverse_exists": result.two_sided_inverse_exists,
            "compact_resolvent_claimed": result.compact_resolvent_claimed,
            "kinetic_mode_gap_claimed": result.kinetic_mode_gap_claimed,
            "dual_space_source_response_certified": (
                result.dual_space_source_response_certified
            ),
            "conclusion_scope": result.conclusion_scope,
        },
        "proof_obligations_discharged": (
            "finite weighted-energy coefficient continuity on V",
            "density of the smooth wall-constrained core by origin cutoff and mollification",
            "unitary logarithmic identification with a half-line H1 space",
            "vanishing origin completion trace because sqrt(x)y tends to zero and K=x*Kbar",
            "no trace defect at the artificial coefficient split",
            "equivalence of the completed-square norm with ||y||2+||x*y'||2",
            "positive allowed wall trace remainder",
            "first representation theorem and spectral inverse bound",
        ),
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "construct a validated Galerkin/Green enclosure for A^{-1}s and "
            "prove that one physical matter-wall/master response functional "
            "has an interval excluding zero"
        ),
        "claim_boundary": (
            "This is the closed self-adjoint Friedrichs realization and an "
            "L2 inverse norm bound for the declared fixed-background weak "
            "form. It does not imply compact resolvent or a kinetic mode gap, "
            "and does not certify a V-star derivative source response, "
            "tensorial Israel matching, or a backreacted Einstein-matter solution."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
