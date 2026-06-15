#!/usr/bin/env python3
"""Authenticate and certify the fixed-wall radial Skyrmion mode gap."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from qgtoy.validated_skyrmion_radial_gap import (  # noqa: E402
    validate_skyrmion_fixed_wall_radial_gap,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


DEFAULT_AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_SNAPSHOT = (
    ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
)
DEFAULT_OUTPUT = ROOT / "experiments/skyrmion_full_radial_gap_exact_certificate.json"
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)
EXPECTED_SNAPSHOT_SHA256 = (
    "1781a2ff357f3b165d23e290eb403552d77d099a72b9e90920735e6a80b30431"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_full_radial_gap_audit.py",
        ROOT / "qgtoy/validated_skyrmion_radial_gap.py",
        ROOT / "qgtoy/validated_skyrmion_sharp_profile.py",
        ROOT / "qgtoy/validated_rational_text.py",
        ROOT / "qgtoy/validated_interval.py",
        ROOT / "qgtoy/validated_skyrmion_bvp.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _verify_snapshot_provenance(snapshot: dict[str, object]) -> None:
    archived = snapshot.get("source_sha256")
    if not isinstance(archived, dict):
        raise ValueError("sharp snapshot is missing source hashes")
    for name, expected in archived.items():
        if not isinstance(name, str) or not isinstance(expected, str):
            raise ValueError("sharp snapshot source hashes are malformed")
        path = ROOT / name
        if _sha256(path) != expected:
            raise ValueError(f"sharp snapshot source hash mismatch: {name}")


def _cell_record(cell: object) -> dict[str, object]:
    return {
        "source_cell_index": cell.source_cell_index,
        "depth": cell.depth,
        "normalized_left": str(cell.normalized_left),
        "normalized_right": str(cell.normalized_right),
        "radius": {
            "lower": str(cell.jet.radius.lower),
            "upper": str(cell.jet.radius.upper),
        },
        "principal_lower_bound": str(cell.coefficients.principal.lower),
        "barta_quotient_lower_bound": str(cell.quotient.lower),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--au2", type=Path, default=DEFAULT_AU2)
    parser.add_argument("--sharp-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--maximum-refinement-depth", type=int, default=6)
    args = parser.parse_args()

    au2_path = args.au2.resolve()
    snapshot_path = args.sharp_snapshot.resolve()
    au2_sha = _sha256(au2_path)
    snapshot_sha = _sha256(snapshot_path)
    if au2_sha != EXPECTED_AU2_SHA256:
        raise ValueError(f"canonical AU.2 hash mismatch: {au2_sha}")
    if snapshot_sha != EXPECTED_SNAPSHOT_SHA256:
        raise ValueError(f"sharp snapshot hash mismatch: {snapshot_sha}")
    au2 = json.loads(au2_path.read_text(encoding="ascii"))
    snapshot = json.loads(snapshot_path.read_text(encoding="ascii"))
    if snapshot.get("canonical_au2_sha256") != au2_sha:
        raise ValueError("sharp snapshot does not reference the canonical AU.2 archive")
    if snapshot.get("canonical_mathematical_outputs_reproduced_exactly") is not True:
        raise ValueError("sharp snapshot did not exactly reproduce canonical AU.2")
    _verify_snapshot_provenance(snapshot)

    tube = reconstruct_validated_skyrmion_sharp_profile(
        au2,
        snapshot,
        subdivisions_per_parent=1,
    )
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    result = validate_skyrmion_fixed_wall_radial_gap(
        tube,
        origin,
        maximum_refinement_depth=args.maximum_refinement_depth,
    )
    record = {
        "result_type": "authenticated_full_fixed_wall_skyrmion_radial_gap",
        "canonical_au2_archive": str(au2_path.relative_to(ROOT)),
        "canonical_au2_sha256": au2_sha,
        "sharp_tube_snapshot": str(snapshot_path.relative_to(ROOT)),
        "sharp_tube_snapshot_sha256": snapshot_sha,
        "source_sha256": _source_hashes(),
        "certificate_id": result.certificate_id,
        "parameters": {
            "origin_cutoff": str(tube.origin_cutoff),
            "wall_radius": str(tube.wall_radius),
            "curvature": str(tube.curvature),
            "pion_mass_squared": str(tube.pion_mass_squared),
            "maximum_refinement_depth": args.maximum_refinement_depth,
        },
        "exact_outputs": {
            "static_form_gap": str(result.static_form_gap),
            "kinetic_weight_upper_bound": str(result.kinetic_weight_upper_bound),
            "dimensionless_frequency_squared_lower_bound": str(
                result.dimensionless_frequency_squared_lower_bound
            ),
            "dimensionless_frequency_lower_bound": "1/5",
            "positive_radius_leaf_count": len(result.positive_radius.cells),
            "positive_radius_maximum_depth_used": (
                result.positive_radius.maximum_depth_used
            ),
            "positive_radius_barta_lower_bound": str(
                result.positive_radius.recomputed_lower_bound
            ),
            "origin_barta_lower_bound": str(result.origin.quotient.lower),
            "origin_boundary_term_vanishes": (
                result.origin.regular_mode_boundary_term_vanishes
            ),
            "wall_boundary_term_vanishes": (
                result.fixed_wall_dirichlet_boundary_term_vanishes
            ),
        },
        "positive_radius_cells": tuple(
            _cell_record(cell) for cell in result.positive_radius.cells
        ),
        "form_domain": (
            "Regular radial fluctuations eta=O(x) with eta(0)=eta(4)=0. "
            "Since P=O(x^2), the origin ground-state-transform boundary term "
            "is O(x^4); the fixed-wall term vanishes by Dirichlet data."
        ),
        "central_result": (
            "The exact AU.1 solution has L_Jacobi>=1 on the complete physical "
            "regular-origin-to-fixed-wall radial form domain. Since W<=25, "
            "omega_hat_rad^2>=1/25 and omega_K>=e f_pi/5."
        ),
        "claim_boundary": result.conclusion_scope,
    }
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "positive_radius_leaf_count": len(result.positive_radius.cells),
                "maximum_depth_used": result.positive_radius.maximum_depth_used,
                "positive_radius_barta_lower_bound_decimal": float(
                    result.positive_radius.recomputed_lower_bound
                ),
                "origin_barta_lower_bound_decimal": float(
                    result.origin.quotient.lower
                ),
                "dimensionless_frequency_lower_bound": 0.2,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
