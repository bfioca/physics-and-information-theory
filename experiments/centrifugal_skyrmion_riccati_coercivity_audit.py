"""Audit the exact Riccati identity and its floating global candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qgtoy.centrifugal_skyrmion_riccati_coercivity import (
    centrifugal_liouville_coercivity_probe,
    centrifugal_riccati_coercivity_probe,
    exact_riccati_identity_certificate,
)
from qgtoy.validated_centrifugal_global_form import (
    validate_centrifugal_wall_trace,
)
from qgtoy.validated_interval import RationalInterval
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_riccati_coercivity_certificate.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_riccati_coercivity.py",
    "qgtoy/validated_centrifugal_global_form.py",
    "qgtoy/centrifugal_skyrmion_deformation.py",
    "qgtoy/centrifugal_skyrmion_origin.py",
    "qgtoy/massive_skyrmion_worldtube.py",
    "experiments/centrifugal_skyrmion_riccati_coercivity_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    identity = exact_riccati_identity_certificate()
    liouville = centrifugal_liouville_coercivity_probe()
    probe = centrifugal_riccati_coercivity_probe()
    wall = validate_centrifugal_wall_trace(
        RationalInterval(Fraction(-89, 1000), Fraction(-87, 1000))
    )
    if not identity["identity_verified"]:
        raise ValueError("exact Riccati completion identity failed")
    if not probe["candidate_passes_sampled_preflight"]:
        raise ValueError("floating Riccati candidate failed its preflight")
    if not liouville["candidate_passes_sampled_preflight"]:
        raise ValueError("explicit Liouville candidate failed its preflight")
    if liouville["minimum_sampled_completed_potential_eigenvalue"] <= 0.075:
        raise ValueError("explicit Liouville bulk margin lost its buffer")
    if liouville["allowed_wall_trace_margin"] <= 0.21:
        raise ValueError("explicit Liouville wall margin lost its buffer")
    if not wall.wall_trace_positive or wall.wall_trace_margin.lower <= Fraction(1, 5):
        raise ValueError("exact interval wall trace margin failed")
    if probe["minimum_sampled_riccati_residual_eigenvalue"] <= 0.09:
        raise ValueError("floating bulk margin lost the preregistered buffer")
    if probe["allowed_wall_trace_margin"] <= 0.48:
        raise ValueError("floating wall margin lost the preregistered buffer")
    return {
        "result_type": "centrifugal_skyrmion_riccati_coercivity_route_audit",
        "exact_identity": identity,
        "preferred_explicit_candidate": liouville,
        "exact_wall_trace": {
            "wall_slope_interval": {
                "lower": str(wall.wall_profile_derivative.lower),
                "upper": str(wall.wall_profile_derivative.upper),
            },
            "robin_interval": {
                "lower": str(wall.wall_robin_multiplier.lower),
                "upper": str(wall.wall_robin_multiplier.upper),
            },
            "margin_interval": {
                "lower": str(wall.wall_trace_margin.lower),
                "upper": str(wall.wall_trace_margin.upper),
            },
            "positive": wall.wall_trace_positive,
        },
        "floating_candidate": probe,
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "enclose the explicit regular Liouville potential over every "
            "authenticated nonlinear profile-tube jet with a cancellation-"
            "preserving Taylor model; retain the Riccati spline only as a "
            "stronger fallback witness"
        ),
        "claim_boundary": (
            "The exact Picone/Riccati algebra is proved and a high-margin "
            "global candidate is reproducible. The candidate remains floating "
            "and sampled, so no continuum eigenvalue or Friedrichs inverse is "
            "yet certified."
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
