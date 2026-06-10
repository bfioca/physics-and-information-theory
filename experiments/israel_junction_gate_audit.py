"""Write the source-hashed tensorial Israel junction-gate audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qgtoy.israel_junction_gate import (
    de_sitter_kottler_static_shell_benchmark,
    identical_geometry_pure_tension_no_go_record,
    linearized_constant_tension_israel_gate,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/israel_junction_gate_certificate.json"
SOURCES = (
    "qgtoy/israel_junction_gate.py",
    "experiments/israel_junction_gate_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    identical = identical_geometry_pure_tension_no_go_record(
        radius=4.0,
        lapse=24.0 / 25.0,
        lapse_derivative=-1.0 / 50.0,
        surface_tension=0.001931779647,
        gravitational_coupling=1.0,
    )
    benchmark = de_sitter_kottler_static_shell_benchmark(
        radius=4.0,
        compact_radius_ratio_squared=0.5,
        gravitational_coupling=1.0,
    )
    tensorial_false_positive = linearized_constant_tension_israel_gate(
        inner_induced_metric_amplitudes=(0.1, -0.2, 0.0),
        outer_induced_metric_amplitudes=(0.1, -0.2, 0.0),
        inner_mixed_extrinsic_curvature_amplitudes=(0.3, -0.4, 0.0),
        outer_mixed_extrinsic_curvature_amplitudes=(0.3, -0.4, 1.0e-3),
    )
    tensorial_closed = linearized_constant_tension_israel_gate(
        inner_induced_metric_amplitudes=(0.1, -0.2, 0.05),
        outer_induced_metric_amplitudes=(0.1, -0.2, 0.05),
        inner_mixed_extrinsic_curvature_amplitudes=(0.3, -0.4, 0.02),
        outer_mixed_extrinsic_curvature_amplitudes=(0.3, -0.4, 0.02),
    )
    claims = {
        "identical_de_sitter_nonzero_tension_is_obstructed": identical[
            "nonzero_tension_is_obstructed"
        ],
        "de_sitter_kottler_benchmark_closes_both_israel_equations": benchmark[
            "benchmark_closes"
        ],
        "tensorial_gate_accepts_matching_first_and_second_forms": tensorial_closed[
            "tensorial_linearized_israel_matching_closes"
        ],
        "tensorial_gate_rejects_hidden_tracefree_jump": not tensorial_false_positive[
            "tensorial_linearized_israel_matching_closes"
        ],
    }
    return {
        "goal": "Tensorial Israel Junction Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_spherical_no_go_and_linearized_tensorial_gate",
        "certified_claims": claims,
        "identical_geometry_no_go": identical,
        "self_consistent_vacuum_shell_benchmark": benchmark,
        "closed_linearized_tensorial_example": tensorial_closed,
        "scalar_subsystem_false_positive_example": tensorial_false_positive,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "The spherical algebra and tensorial acceptance conditions are exact. "
            "The audit does not reconstruct the six physical-shell amplitudes "
            "from the Skyrmion master solution and therefore does not certify "
            "the Skyrmion Israel junction."
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
