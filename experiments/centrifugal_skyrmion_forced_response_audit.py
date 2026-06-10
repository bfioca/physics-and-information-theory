"""Compose the exact nonzero centrifugal weak-response certificate."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_forced_response import (
    certify_centrifugal_weak_response,
)


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = ROOT / "experiments/centrifugal_skyrmion_liouville_origin_certificate.json"
FORM = ROOT / "experiments/centrifugal_skyrmion_friedrichs_form_certificate.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_forced_response_certificate.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_forced_response.py",
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/centrifugal_skyrmion_deformation.py",
    "experiments/centrifugal_skyrmion_forced_response_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    origin = json.loads(ORIGIN.read_text(encoding="ascii"))
    form = json.loads(FORM.read_text(encoding="ascii"))
    if not origin["summary"]["coercivity_verified"]:
        raise ValueError("origin profile family is not authenticated")
    if (
        not form["theorem"]["closed"]
        or not form["theorem"]["two_sided_inverse_exists"]
        or not form["theorem"]["form_norm_equivalent_to_weighted_sobolev_norm"]
    ):
        raise ValueError("global weak form is not coercive on the form domain")
    slopes = origin["origin_family"]["shooting_slopes"]
    result = certify_centrifugal_weak_response(
        shooting_slope_lower=Fraction(slopes["lower"]),
        shooting_slope_upper=Fraction(slopes["upper"]),
        form_coercivity_lower_bound=Fraction(
            form["theorem"]["coercivity_lower_bound"]
        ),
    )
    return {
        "result_type": "centrifugal_skyrmion_nonzero_weak_response_audit",
        "input_artifacts": {
            str(ORIGIN.relative_to(ROOT)): _sha256(ORIGIN),
            str(FORM.relative_to(ROOT)): _sha256(FORM),
        },
        "theorem": {
            "shooting_slope_lower": str(result.shooting_slope_lower),
            "shooting_slope_upper": str(result.shooting_slope_upper),
            "tangential_source_leading_lower": str(
                result.tangential_source_leading_lower
            ),
            "tangential_source_leading_lower_decimal": float(
                result.tangential_source_leading_lower
            ),
            "source_asymptotic": "s_g(x)=c(b)*x^3+O(x^5)",
            "source_space": result.source_space,
            "source_is_continuous": result.source_is_continuous,
            "source_is_nonzero": result.source_is_nonzero,
            "unique_weak_solution_exists": result.unique_weak_solution_exists,
            "weak_solution_is_nonzero": result.weak_solution_is_nonzero,
            "source_conjugate_susceptibility_positive": (
                result.source_conjugate_susceptibility_positive
            ),
            "derivative_source_vanishes_at_endpoints": (
                result.derivative_source_vanishes_at_endpoints
            ),
            "l2_inverse_bound_applies_directly": (
                result.l2_inverse_bound_applies_directly
            ),
            "master_or_weyl_response_certified": (
                result.master_or_weyl_response_certified
            ),
            "conclusion_scope": result.conclusion_scope,
        },
        "proof": (
            "The regular kernel formula gives lim_(x->0) s_g/x^3="
            "b(4b^2-1)/30. This is uniformly positive on the authenticated "
            "slope interval, so the source is nonzero. The derivative-load "
            "coefficient is O(x^4) at the origin and contains sin(F)^2, so "
            "it vanishes at both the origin and the F(a)=0 wall. Integration "
            "by parts gives the L2 source s=s0-s1' with no endpoint load. "
            "Coercivity gives a unique weak solution y; y=0 would imply the "
            "source vanishes. Testing the weak equation with y gives "
            "ell(y)=q(y)>0."
        ),
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "construct a quantitative primal-adjoint residual enclosure and prove "
            "that an off-wall Zerilli/Weyl response functional excludes zero"
        ),
        "claim_boundary": (
            "This proves a unique nonzero fixed-background matter deformation "
            "and positive source-conjugate susceptibility. It does not bound "
            "the field norm or certify a nonzero master/Weyl observable."
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
