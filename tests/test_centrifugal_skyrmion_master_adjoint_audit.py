import json
from pathlib import Path

from experiments.centrifugal_skyrmion_master_adjoint_audit import build_record


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_master_adjoint_feasibility.json"


def test_floating_master_adjoint_audit_artifact() -> None:
    expected = json.loads(ARTIFACT.read_text())
    record = build_record()
    assert json.loads(json.dumps(record)) == expected
    assert record["status"] == "pass"
    assert all(record["verified_numerical_properties"].values())
    assert (
        record["dual_weighted_estimator"][
            "floating_distance_from_zero_after_product_bound"
        ]
        > 0.0
    )
    assert "Floating evidence only" in record["claim_boundary"]
