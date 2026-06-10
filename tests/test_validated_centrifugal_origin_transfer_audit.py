import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_origin_transfer_certificate.json"


def test_validated_centrifugal_origin_transfer_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "exact_conormal_fuchs_origin_transfer_scaffold"
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert float(record["weighted_green_majorant"]["upper"]) < 0.45
    assert record["green_majorant_slope_cells"] == 128
    assert len(record["green_majorant_state_weights"]) == 4
    assert "remains to be checked" in record["degree_two_field_germ"]
    assert "A(t)-A(0)" in record["claim_boundary"]

    dependency = record["validated_profile_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert (
        hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency["sha256"]
    )
    profile = json.loads(dependency_path.read_text(encoding="ascii"))
    assert (
        profile["authenticated_slope_interval"]
        == record["authenticated_slope_interval"]
    )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
