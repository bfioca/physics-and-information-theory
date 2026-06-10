#!/usr/bin/env python3
"""Write the exact centrifugal conormal-interface certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_conormal_interface_certificate import (  # noqa: E402
    certify_internal_conormal_cancellation,
)
from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
    refine_rational_response_trial,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/centrifugal_conormal_interface_certificate.json"
SOURCES = (
    "qgtoy/centrifugal_conormal_interface_certificate.py",
    "experiments/centrifugal_conormal_interface_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    trials = json.loads(TRIALS.read_text(encoding="ascii"))
    subdivisions = 8
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=subdivisions
    )
    pair = rational_response_trial_pair_from_record(trials["trial_archive"])
    certificates = {}
    for name, trial in (("primal", pair.primal), ("adjoint", pair.adjoint)):
        refined = refine_rational_response_trial(
            trial, subdivisions_per_cell=subdivisions
        )
        certificate = certify_internal_conormal_cancellation(profile, refined)
        certificates[name] = {
            key: value for key, value in certificate.__dict__.items()
        }
    claims = {
        "primal_internal_conormal_jump_is_exactly_zero": certificates["primal"][
            "internal_conormal_jump_is_exactly_zero"
        ],
        "adjoint_internal_conormal_jump_is_exactly_zero": certificates["adjoint"][
            "internal_conormal_jump_is_exactly_zero"
        ],
        "all_344_positive_radius_cells_share_one_partition": (
            certificates["primal"]["interface_count"] == 344
            and certificates["adjoint"]["interface_count"] == 344
        ),
    }
    return {
        "goal": "Exact Centrifugal Conormal Interface Cancellation",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "structural_weak_residual_interface_certificate",
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "subdivisions_per_authenticated_cell": subdivisions,
        "certificates": certificates,
        "proof": (
            "The conormal p=M(x,F,F')^T y+P(x,F,F')y' has identical "
            "one-sided values because the authenticated tube represents one global "
            "C1 profile and each archived rational trial is exactly global C1."
        ),
        "claim_boundary": (
            "This excludes internal delta distributions in the cellwise weak "
            "residual. It does not bound the bulk or wall residual magnitudes."
        ),
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print(OUTPUT)
    if record["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
