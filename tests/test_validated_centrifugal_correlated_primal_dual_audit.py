import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_correlated_primal_dual.json"


def test_correlated_primal_dual_artifact_is_source_bound_and_diagnostic() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    bound = record["partial_bound"]
    assert 0.75 < bound["matrix_weighted_energy_dual_upper_float"] < 0.8
    assert bound["local_potential_inverse_cell_count"] >= 25
    assert "negative diagnostic" in record["claim_boundary"]
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
