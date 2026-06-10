import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_origin_weak_dual.json"


def test_origin_weak_dual_artifact_is_source_bound() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["loaded_adjoint_master"]["energy_dual_upper_float"] < 0.001
    assert "without a cutoff conormal trace" in record["claim_boundary"]
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected

