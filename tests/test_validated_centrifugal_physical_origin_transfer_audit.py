import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT / "experiments/validated_centrifugal_physical_origin_transfer_certificate.json"
)


def test_validated_centrifugal_physical_origin_transfer_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == ("validated_physical_centrifugal_origin_transfer")
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert float(record["maximum_field_interval_width"]["upper"]) < 0.06
    assert float(record["maximum_derivative_interval_width"]["upper"]) < 1.5
    assert "absolute" in record["affine_combination_rule"]
    assert "Friedrichs" in record["claim_boundary"]

    dependency = record["validated_conormal_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert (
        hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency["sha256"]
    )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
