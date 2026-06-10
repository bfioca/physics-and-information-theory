import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_completed_stress_certificate.json"


def test_centrifugal_skyrmion_completed_stress_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == "floating_bulk_conservation_mesh_closure"
    assert record["mesh_records"][-1]["residual_reduction_factor"] < 1.0e-3
    assert max(record["successive_radial_residual_ratios"]) < 0.35
    assert max(record["successive_angular_residual_ratios"]) < 0.35
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
