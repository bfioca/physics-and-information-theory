import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_conormal_blocks_certificate.json"


def test_centrifugal_skyrmion_conormal_blocks_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == (
        "exact_regular_conormal_blocks_and_residual_divisibility"
    )
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert all(record["conormal_residual_checks"].values())
    assert record["fuchs_variation_order"] == "A(t)-A(0)=O(t)"
    assert "- Euler residual / x" in record["residual_transfer_identity"]
    assert "Quantitative interval bounds" in record["claim_boundary"]

    for dependency_key in (
        "validated_transfer_dependency",
        "validated_profile_dependency",
    ):
        dependency = record[dependency_key]
        dependency_path = ROOT / dependency["path"]
        assert (
            hashlib.sha256(dependency_path.read_bytes()).hexdigest()
            == dependency["sha256"]
        )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
