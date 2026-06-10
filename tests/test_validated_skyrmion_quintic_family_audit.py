import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_skyrmion_quintic_family_certificate.json"


def test_validated_skyrmion_quintic_family_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == (
        "validated_uniform_skyrmion_quintic_origin_family"
    )
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert float(record["maximum_contraction_bound"]["upper"]) < 0.6
    assert float(record["radii_left_side"]["upper"]) < 0.9
    assert float(record["minimum_volterra_denominator"]["lower"]) > 20
    assert float(record["derivative_at_cutoff"]["upper"]) < 0

    dependency = record["authenticated_profile_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency[
        "sha256"
    ]
    snapshot = json.loads(dependency_path.read_text(encoding="ascii"))
    assert snapshot["sharp_profile_recipe"]["shooting_slope_interval"] == record[
        "authenticated_slope_interval"
    ]
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
